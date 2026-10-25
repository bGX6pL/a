# Dot-source this file (". .\scripts\env.ps1") to load the project's Postgres settings
# into the current PowerShell session: PATH to the bundled binaries, PG* variables from
# .env and the project-local .pgpass file.
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$PgBin = Join-Path $ProjectRoot 'pgsql\bin'
$PgData = Join-Path $ProjectRoot 'pgdata'
$PgLogs = Join-Path $ProjectRoot 'logs'

if (-not ($env:PATH -split ';' | Where-Object { $_ -eq $PgBin })) {
    $env:PATH = "$PgBin;$env:PATH"
}

$envFile = Join-Path $ProjectRoot '.env'
if (Test-Path $envFile) {
    foreach ($line in Get-Content $envFile) {
        # Passwords stay out of the environment: psql reads them from .pgpass, Python from .env
        if ($line -match '^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$' -and $Matches[1] -notmatch 'PASSWORD') {
            Set-Item -Path "env:$($Matches[1])" -Value $Matches[2].Trim()
        }
    }
}
$env:PGPASSFILE = Join-Path $ProjectRoot '.pgpass'
# Keep Python/uv caches on D: as well
$env:UV_CACHE_DIR = Join-Path $ProjectRoot '.uv-cache'
