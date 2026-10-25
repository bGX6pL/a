"""Fetch RÚZ (Slovak register of financial statements) entities and recent balance sheets.

    uv run python -m investordb.fetch.ruz

IČOs: Slovak legal entities in dossiers (core.legal_entity, SK-ICO) and the Slovak registered fund
managers / self-managed funds / EuVECA managers in the NBS snapshot. For the latest three statements
the structured balance sheet, when the filer submitted one, gives total assets and equity
(Strana aktív row 1, Strana pasív "Vlastné imanie"); PDF-only filings are listed with their
attachments. Data is CC0 (https://www.registeruz.sk/cruz-public/home/api).
"""

import sys

from psycopg.types.json import Jsonb

from investordb.db import connect
from investordb.fetch.common import FetchRun

API = "https://www.registeruz.sk/cruz-public/api/"
NBS_SCOPES = [
    "registrovaný správca alternatívnych investičných fondov",
    "registrovaný samosprávny alternatívny investičný fond",
    "správca Európskych fondov rizikového kapitálu (EuVECA)",
]
ICOS_SQL = """
select distinct ico from (
    select lpad(registry_id, 8, '0') as ico from core.legal_entity where registry = 'SK-ICO' and registry_id ~ '^[0-9]+$'
    union
    select nbs_id from raw.nbs_entity
    where country = 'SK' and nbs_id ~ '^[0-9]{8}$' and licence_scopes && %s
      and snapshot_date = (select max(snapshot_date) from raw.nbs_entity)
) icos order by ico
"""


def balance_sheet(run: FetchRun, report: dict, templates: dict) -> dict:
    """Total assets and equity (current period) from a structured report, if there is one."""
    tables = (report.get("obsah") or {}).get("tabulky") or []
    template_id = report.get("idSablony")
    if not tables or not template_id:
        return {}
    if template_id not in templates:
        templates[template_id] = run.get(f"{API}sablona?id={template_id}", name=f"sablona_{template_id}.json").json()
    shape = {t["nazov"]["sk"]: t for t in templates[template_id]["tabulky"]}
    out = {"template": templates[template_id].get("nazov")}
    for table in tables:
        title = table["nazov"]["sk"]
        meta = shape.get(title)
        if not meta or title not in ("Strana aktív", "Strana pasív"):
            continue
        cols = meta["pocetDatovychStlpcov"]
        current = 2 if cols == 4 else 0  # POD: brutto, korekcia, netto current, netto previous; MUJ: current, previous
        rows = [r["text"]["sk"] for r in meta["riadky"]]
        values = table["data"]

        def cell(row_index: int):
            raw = values[row_index * cols + (current if title == "Strana aktív" else 0)] if row_index * cols < len(values) else ""
            return float(raw) if raw not in ("", None) else None

        if title == "Strana aktív":
            out["total_assets"] = cell(0)
        else:
            equity_row = next((i for i, text in enumerate(rows) if text.lower().startswith("vlastné imanie")), None)
            out["equity"] = cell(equity_row) if equity_row is not None else None
    return out


def main() -> int:
    templates: dict = {}
    with FetchRun("sk-ruz", "investordb.fetch.ruz", min_interval=0.3) as run, connect() as conn:
        icos = [r[0] for r in conn.execute(ICOS_SQL, (NBS_SCOPES,))]
        print(f"fetching {len(icos)} Slovak IČOs from RÚZ")
        for ico in icos:
            ids = run.get(f"{API}uctovne-jednotky?zmenene-od=2000-01-01&ico={ico}", save=False).json().get("id") or []
            if not ids:
                conn.execute("""insert into raw.ruz_unit (ico, unit_id, payload, statements, fetch_run_id)
                                values (%s, null, null, '[]', %s)
                                on conflict (ico) do update set unit_id = null, payload = null, statements = '[]',
                                    fetched_at = now(), fetch_run_id = excluded.fetch_run_id""", (ico, run.id))
                conn.commit()
                continue
            unit = run.get(f"{API}uctovna-jednotka?id={ids[0]}", name=f"unit_{ico}.json").json()
            statements = []
            for zid in sorted(unit.get("idUctovnychZavierok") or [], reverse=True)[:3]:
                z = run.get(f"{API}uctovna-zavierka?id={zid}", name=f"zavierka_{zid}.json").json()
                entry = {"id": zid, "period_from": z.get("obdobieOd"), "period_to": z.get("obdobieDo"),
                         "type": z.get("typ"), "attachments": []}
                for vid in z.get("idUctovnychVykazov") or []:
                    report = run.get(f"{API}uctovny-vykaz?id={vid}", name=f"vykaz_{vid}.json").json()
                    entry["attachments"] += [{"id": a["id"], "name": a.get("meno")} for a in report.get("prilohy") or []]
                    entry.update({k: v for k, v in balance_sheet(run, report, templates).items() if v is not None})
                statements.append(entry)
            statements.sort(key=lambda s: s.get("period_to") or "", reverse=True)
            conn.execute(
                """insert into raw.ruz_unit (ico, unit_id, payload, statements, fetch_run_id) values (%s, %s, %s, %s, %s)
                   on conflict (ico) do update set unit_id = excluded.unit_id, payload = excluded.payload,
                       statements = excluded.statements, fetched_at = now(), fetch_run_id = excluded.fetch_run_id""",
                (ico, ids[0], Jsonb(unit), Jsonb(statements), run.id))
            conn.commit()
            run.rows += 1
        print(f"done: {run.rows} entities with filings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
