"""Fetch the NBS register of financial-market entities (daily export) into raw.nbs_entity.

    uv run python -m investordb.fetch.nbs

Source: https://subjekty.nbs.sk/info ("Databáza na stiahnutie"), a zipped JSON of every entity with
at least one licence effective today.
"""

import datetime as dt
import io
import json
import sys
import zipfile

from psycopg.types.json import Jsonb

from investordb.db import connect
from investordb.fetch.common import FetchRun

URL = "https://subjekty.nbs.sk/api/json"


def scopes(node):
    if isinstance(node, dict):
        if "scope" in node:
            yield node["scope"]
        for value in node.values():
            yield from scopes(value)
    elif isinstance(node, list):
        for value in node:
            yield from scopes(value)


def main() -> int:
    with FetchRun("nbs-register", "investordb.fetch.nbs") as run, connect() as conn:
        f = run.get(URL, name="subjekty-nbs-sk.zip", timeout=180)
        if not f.ok:
            raise RuntimeError(f"NBS export returned {f.status} {f.error or ''}")
        archive = zipfile.ZipFile(io.BytesIO(f.body))
        data = json.loads(archive.read(archive.namelist()[0]).decode("utf-8"))
        snapshot = dt.date.fromisoformat(str(data.get("updated", dt.date.today().isoformat()))[:10])
        records = [
            (snapshot, str(it["id"]), it["name"], it.get("address"), it.get("country"),
             sorted(set(scopes(it.get("licenses")))), Jsonb(it.get("licenses")), run.id)
            for it in data["institutions"]
        ]
        with conn.transaction():
            conn.execute("delete from raw.nbs_entity where snapshot_date = %s", (snapshot,))
            with conn.cursor() as cur:
                cur.executemany(
                    """insert into raw.nbs_entity (snapshot_date, nbs_id, name, address, country, licence_scopes,
                           licences, fetch_run_id) values (%s, %s, %s, %s, %s, %s, %s, %s)
                       on conflict do nothing""", records)
        run.rows = len(records)
        print(f"NBS register as of {snapshot}: {len(records)} entities")
    return 0


if __name__ == "__main__":
    sys.exit(main())
