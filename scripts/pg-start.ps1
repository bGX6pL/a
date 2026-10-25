# Start the project's Postgres server (data in D:\investor-db\pgdata, port from .env).
. "$PSScriptRoot\env.ps1"
& pg_ctl -D $PgData status *> $null
if ($LASTEXITCODE -eq 0) { Write-Host "Postgres already running on port $env:PGPORT"; exit 0 }
& pg_ctl -D $PgData -l (Join-Path $PgLogs 'pg_ctl.log') -w start
& pg_isready -h $env:PGHOST -p $env:PGPORT
