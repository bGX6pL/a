"""Fetch scripts: each downloads one public source into raw.* and logs the run in meta.*.

    uv run python -m investordb.fetch.jerrs      # ČNB JERRS lists (fund managers, funds)
    uv run python -m investordb.fetch.nbs        # NBS register export (Slovakia)
    uv run python -m investordb.fetch.cvca       # CVCA member profiles
    uv run python -m investordb.fetch.ares       # ARES records for every Czech IČO we hold
    uv run python -m investordb.fetch.ruz        # RÚZ entities and balance sheets for Slovak IČOs
    uv run python -m investordb.fetch.evidence   # every evidence URL cited in dossiers (V2/V3)
"""
