-- Base layout. Schemas:
--   meta  pipeline bookkeeping: applied migrations, every fetch run and fetched file
--   raw   untouched copies of fetched source data, one table per source
--   core  curated investor records (designed together with the inclusion rules)
--   ref   research catalog: data sources and competitors
create schema if not exists raw;
create schema if not exists core;
create schema if not exists ref;

-- One row per execution of a fetch script, so every raw row can be traced to a run.
create table meta.fetch_run (
    fetch_run_id bigint generated always as identity primary key,
    source_slug  text not null,
    script       text not null,
    started_at   timestamptz not null default now(),
    finished_at  timestamptz,
    status       text not null default 'running' check (status in ('running', 'ok', 'failed')),
    params       jsonb not null default '{}',
    rows_fetched integer,
    error        text
);

-- Every downloaded payload: where it came from, when, and a hash to detect changes.
create table meta.fetched_file (
    fetched_file_id bigint generated always as identity primary key,
    fetch_run_id    bigint not null references meta.fetch_run on delete cascade,
    url             text not null,
    http_status     integer,
    content_type    text,
    sha256          text,
    bytes           bigint,
    local_path      text,  -- relative to the project root, under data/raw/
    fetched_at      timestamptz not null default now()
);
create index on meta.fetched_file (fetch_run_id);
create index on meta.fetched_file (url);
