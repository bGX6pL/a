# Open psql on the project database as the application role. Extra args are passed through,
# e.g.  .\scripts\psql.ps1 -c "select count(*) from ref.data_source"
. "$PSScriptRoot\env.ps1"
& psql -h $env:PGHOST -p $env:PGPORT -U $env:PGUSER -d $env:PGDATABASE @args
