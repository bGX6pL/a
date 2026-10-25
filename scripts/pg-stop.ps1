# Stop the project's Postgres server cleanly.
. "$PSScriptRoot\env.ps1"
& pg_ctl -D $PgData -m fast -w stop
