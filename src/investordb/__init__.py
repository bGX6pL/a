"""Public-data investor database tooling."""

import sys

# Czech and Slovak names are printed by most scripts; Windows consoles and redirected output
# otherwise default to a legacy code page and fail on characters such as Č.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure") and (_stream.encoding or "").lower().replace("-", "") != "utf8":
        _stream.reconfigure(encoding="utf-8", errors="replace")
