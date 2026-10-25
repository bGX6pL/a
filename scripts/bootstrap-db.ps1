# Idempotently create the application role and database. Needs the server running
# (scripts\pg-start.ps1) and both passwords in .env / .pgpass (written by the initial setup).
. "$PSScriptRoot\env.ps1"
$ErrorActionPreference = 'Stop'
$su = @('-h', $env:PGHOST, '-p', $env:PGPORT, '-U', $env:PG_SUPERUSER, '-v', 'ON_ERROR_STOP=1', '-X', '-q')
$appPw = (Get-Content (Join-Path $ProjectRoot '.env') | Where-Object { $_ -match '^PGPASSWORD=' }) -replace '^PGPASSWORD=', ''

function Invoke-Su([string]$db, [string]$sql, [switch]$Scalar) {
    $flags = if ($Scalar) { @('-tAc', $sql) } else { @('-c', $sql) }
    $out = & psql @su -d $db @flags
    if ($LASTEXITCODE -ne 0) { throw "psql failed: $sql" }
    return $out
}

if ((Invoke-Su postgres "select 1 from pg_roles where rolname = '$env:PGUSER'" -Scalar) -ne '1') {
    Invoke-Su postgres "create role $env:PGUSER login password '$appPw'" | Out-Null
}
if ((Invoke-Su postgres "select 1 from pg_database where datname = '$env:PGDATABASE'" -Scalar) -ne '1') {
    Invoke-Su postgres "create database $env:PGDATABASE owner $env:PGUSER encoding 'UTF8' template template0 locale_provider icu icu_locale 'und' locale 'C'" | Out-Null
}
Invoke-Su $env:PGDATABASE "alter schema public owner to $env:PGUSER" | Out-Null
Write-Host "Role '$env:PGUSER' and database '$env:PGDATABASE' are ready on port $env:PGPORT"
