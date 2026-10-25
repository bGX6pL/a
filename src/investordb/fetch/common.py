"""Shared plumbing for fetch scripts: a logged run, polite HTTP, raw file storage, text extraction."""

import datetime as dt
import hashlib
import html
import io
import json
import mimetypes
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import truststore

from investordb.db import PROJECT_ROOT, connect, settings

# Verify TLS against the operating system's trust store: it completes chains that some Czech and
# Slovak sites serve without intermediates, which Python's bundled verification rejects.
truststore.inject_into_ssl()

RAW_DIR = PROJECT_ROOT / "data" / "raw"
DEFAULT_UA = "Mozilla/5.0 (compatible; investor-db/0.1; public-data research)"


@dataclass
class Fetched:
    url: str
    final_url: str
    status: int | None
    content_type: str | None
    body: bytes
    path: Path | None
    fetched_file_id: int | None
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.status is not None and 200 <= self.status < 300

    def text(self, encoding: str | None = None) -> str:
        enc = encoding or _charset(self.content_type, self.body) or "utf-8"
        return self.body.decode(enc, errors="replace")

    def json(self):
        return json.loads(self.body.decode("utf-8"))


def _charset(content_type: str | None, body: bytes) -> str | None:
    m = re.search(r"charset=([\w-]+)", content_type or "", re.I) or re.search(rb'charset=["\']?([\w-]+)', body[:2048], re.I)
    if not m:
        return None
    value = m.group(1)
    return value.decode() if isinstance(value, bytes) else value


class FetchRun:
    """One logged execution of a fetch script (meta.fetch_run) with every download in meta.fetched_file.

    Uses its own autocommit connection so the log survives a failure of the caller's transaction.
    """

    def __init__(self, source_slug: str, script: str, params: dict | None = None, min_interval: float = 0.5):
        self.source_slug, self.script, self.params = source_slug, script, params or {}
        self.min_interval = min_interval
        self.user_agent = settings().get("HTTP_USER_AGENT") or DEFAULT_UA
        self.rows = 0
        self._last_hit: dict[str, float] = {}

    def __enter__(self) -> "FetchRun":
        self.log = connect(autocommit=True)
        self.id = self.log.execute(
            "insert into meta.fetch_run (source_slug, script, params) values (%s, %s, %s) returning fetch_run_id",
            (self.source_slug, self.script, json.dumps(self.params)),
        ).fetchone()[0]
        self.day_dir = RAW_DIR / self.source_slug / dt.date.today().isoformat()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.log.execute(
            "update meta.fetch_run set finished_at = now(), status = %s, rows_fetched = %s, error = %s where fetch_run_id = %s",
            ("failed" if exc else "ok", self.rows, repr(exc)[:2000] if exc else None, self.id),
        )
        self.log.close()

    def _wait(self, url: str) -> None:
        host = urllib.parse.urlsplit(url).netloc
        wait = self._last_hit.get(host, 0) + self.min_interval - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        self._last_hit[host] = time.monotonic()

    def get(self, url: str, *, data: bytes | dict | None = None, headers: dict | None = None,
            name: str | None = None, timeout: int = 60, retries: int = 3, save: bool = True) -> Fetched:
        if isinstance(data, dict):
            data = urllib.parse.urlencode(data).encode()
        hdrs = {"User-Agent": self.user_agent, "Accept": "*/*", "Accept-Language": "cs,sk,en;q=0.8", **(headers or {})}
        status = content_type = error = None
        body, final_url = b"", url
        for attempt in range(retries):
            self._wait(url)
            try:
                with urllib.request.urlopen(urllib.request.Request(url, data=data, headers=hdrs), timeout=timeout) as r:
                    status, content_type, final_url, body = r.status, r.headers.get("Content-Type"), r.geturl(), r.read()
                error = None
                break
            except urllib.error.HTTPError as e:
                status, content_type, final_url = e.code, e.headers.get("Content-Type"), e.geturl()
                body, error = e.read() or b"", None
                if e.code < 500 and e.code != 429:
                    break
            except Exception as e:  # timeouts, DNS, TLS
                status, error = None, f"{type(e).__name__}: {e}"[:500]
            time.sleep(2 ** attempt)

        path = None
        if save and body:
            digest = hashlib.sha256(body).hexdigest()
            ext = Path(urllib.parse.urlsplit(final_url).path).suffix.lower()
            if not ext or len(ext) > 6:
                ext = mimetypes.guess_extension((content_type or "").split(";")[0].strip()) or ".bin"
            path = self.day_dir / (name or digest[:20] + ext)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
        fetched_file_id = self.log.execute(
            """insert into meta.fetched_file (fetch_run_id, url, http_status, content_type, sha256, bytes, local_path)
               values (%s, %s, %s, %s, %s, %s, %s) returning fetched_file_id""",
            (self.id, url, status, content_type, hashlib.sha256(body).hexdigest() if body else None, len(body),
             path.relative_to(PROJECT_ROOT).as_posix() if path else error),
        ).fetchone()[0]
        return Fetched(url, final_url, status, content_type, body, path, fetched_file_id, error)

    def adopt(self, url: str, source: Path, content_type: str = "text/html; charset=utf-8") -> Fetched:
        """Log a page that a person downloaded in a browser (e.g. behind a CAPTCHA) as part of this run."""
        body = source.read_bytes()
        path = self.day_dir / source.name
        path.parent.mkdir(parents=True, exist_ok=True)
        if source.resolve() != path.resolve():
            path.write_bytes(body)
        fetched_file_id = self.log.execute(
            """insert into meta.fetched_file (fetch_run_id, url, http_status, content_type, sha256, bytes, local_path)
               values (%s, %s, 200, %s, %s, %s, %s) returning fetched_file_id""",
            (self.id, url, content_type, hashlib.sha256(body).hexdigest(), len(body), path.relative_to(PROJECT_ROOT).as_posix()),
        ).fetchone()[0]
        return Fetched(url, url, 200, content_type, body, path, fetched_file_id)


# ------------------------------------------------------------------ text helpers

def html_to_text(markup: str) -> str:
    markup = re.sub(r"(?is)<(script|style|noscript|svg|template)\b.*?</\1>", " ", markup)
    markup = re.sub(r"(?i)<br\s*/?>|</(p|div|li|h\d|tr|td|th|section|article)>", "\n", markup)
    text = html.unescape(re.sub(r"(?s)<[^>]+>", " ", markup))
    return re.sub(r"[ \t\r\f\v ]+", " ", text)


def pdf_to_text(body: bytes) -> str:
    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(body))
    return "\n".join((page.extract_text() or "") for page in reader.pages)


def table_rows(markup: str) -> list[list[str]]:
    """Cells of every <tr> as plain text."""
    rows = []
    for row in re.findall(r"(?is)<tr[^>]*>(.*?)</tr>", markup):
        cells = [re.sub(r"\s+", " ", html.unescape(re.sub(r"(?s)<[^>]+>", " ", c))).strip()
                 for c in re.findall(r"(?is)<t[dh][^>]*>(.*?)</t[dh]>", row)]
        rows.append(cells)
    return rows
