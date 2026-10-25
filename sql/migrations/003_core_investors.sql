-- Curated investor records (core), the raw register snapshots they are checked against (raw),
-- and a catalog category for evidence pages cited in dossiers.

alter table ref.data_source drop constraint data_source_category_check;
alter table ref.data_source add constraint data_source_category_check check (category in (
    'regulatory_filing', 'regulatory_register', 'company_registry', 'public_programme', 'lp_disclosure',
    'association', 'news_media', 'press_release', 'open_dataset', 'ecosystem_report', 'investor_website',
    'commercial_free_tier', 'web_evidence'));

-- ---------------------------------------------------------------- core

-- Every screened candidate, included or not. Loaded from data/curated/dossiers/**.json;
-- the columns after loaded_at are computed by investordb.build.
create table core.investor (
    investor_id        bigint generated always as identity primary key,
    investor_key       text not null unique,
    pilot              text not null,
    name               text not null,
    aliases            text[] not null default '{}',
    investor_type      text check (investor_type in
                           ('vc', 'pe', 'family_office', 'angel', 'angel_network', 'private_investor')),
    secondary_types    text[] not null default '{}',
    is_corporate       boolean not null default false,
    is_public          boolean not null default false,
    is_accelerator     boolean not null default false,
    hq_country         text,
    website            text,
    decision           text not null check (decision in ('include', 'exclude', 'unverified')),
    rule_codes         text[] not null default '{}',
    decision_note      text,
    discovered_via     text[] not null default '{}',
    co_investors_seen  text[] not null default '{}',
    analyst_notes      text,
    researched_on      date not null,
    dossier_path       text not null,
    loaded_at          timestamptz not null default now(),
    last_activity_date date,
    status             text check (status in ('active', 'inactive', 'unknown')),
    confidence         numeric(4, 3),
    published          boolean
);

create table core.evidence (
    evidence_id  bigint generated always as identity primary key,
    investor_id  bigint not null references core.investor on delete cascade,
    local_id     text not null,  -- id used inside the dossier, e.g. e1
    url          text not null,
    publisher    text,
    published_on date,
    source_class char(1) not null check (source_class in ('A', 'B', 'C', 'D')),
    quote        text not null,
    language     text,
    unique (investor_id, local_id)
);
create index on core.evidence (url);

create table core.legal_entity (
    legal_entity_id bigint generated always as identity primary key,
    investor_id     bigint not null references core.investor on delete cascade,
    name            text not null,
    country         text,
    registry        text not null check (registry in ('CZ-ICO', 'SK-ICO', 'LEI', 'OTHER')),
    registry_id     text,
    role            text not null check (role in ('manager', 'fund', 'gp', 'holding', 'other'))
);
create index on core.legal_entity (registry, registry_id);

-- One row per required field (sector_focus, stage_focus, geography_focus, ticket_size, capital).
create table core.fact (
    fact_id     bigint generated always as identity primary key,
    investor_id bigint not null references core.investor on delete cascade,
    field       text not null check (field in
                    ('sector_focus', 'stage_focus', 'geography_focus', 'ticket_size', 'capital')),
    value       jsonb,
    method      text not null check (method in ('stated', 'derived', 'self_reported', 'registry', 'not_disclosed')),
    as_of       date,
    unique (investor_id, field)
);

create table core.fact_evidence (
    fact_id     bigint not null references core.fact on delete cascade,
    evidence_id bigint not null references core.evidence on delete cascade,
    primary key (fact_id, evidence_id)
);

create table core.fund (
    fund_id     bigint generated always as identity primary key,
    investor_id bigint not null references core.investor on delete cascade,
    name        text not null,
    size_amount numeric(18, 2),
    currency    text,
    event       text check (event in ('first_close', 'final_close', 'launch', 'target', 'commitment', 'other')),
    event_date  date,
    evidence_id bigint references core.evidence on delete set null
);

create table core.investment (
    investment_id   bigint generated always as identity primary key,
    investor_id     bigint not null references core.investor on delete cascade,
    company         text not null,
    company_country text,
    announced_on    date,
    round           text,
    round_amount    numeric(18, 2),
    currency        text,
    evidence_id     bigint references core.evidence on delete set null
);

-- Script verification of cited evidence (V2/V3); keyed by URL + quote so it survives dossier reloads.
create table core.evidence_check (
    evidence_check_id bigint generated always as identity primary key,
    url               text not null,
    quote_sha256      text not null,
    checked_at        timestamptz not null default now(),
    http_status       integer,
    fetched_file_id   bigint references meta.fetched_file on delete set null,
    text_chars        integer,
    quote_found       boolean,
    similarity        numeric(4, 3),
    error             text
);
create index on core.evidence_check (url, quote_sha256, checked_at desc);

-- Results of automated checks V1-V7 per investor (rewritten by investordb.build).
create table core.check_result (
    check_result_id bigint generated always as identity primary key,
    investor_id     bigint not null references core.investor on delete cascade,
    check_code      text not null,
    passed          boolean,
    detail          text,
    checked_at      timestamptz not null default now()
);
create index on core.check_result (investor_id, check_code);

-- Manual / independent review verdicts (M1, M2), loaded from data/curated/reviews/*.json.
create table core.review (
    review_id     bigint generated always as identity primary key,
    investor_key  text not null,
    sample        text not null,
    reviewer      text not null,
    reviewed_on   date not null,
    verdict       text not null check (verdict in ('correct', 'incorrect', 'unsure')),
    checks        jsonb not null default '{}',
    notes         text,
    unique (investor_key, sample, reviewer)
);

-- ---------------------------------------------------------------- raw register snapshots

create table raw.jerrs_entity (
    jerrs_entity_id bigint generated always as identity primary key,
    snapshot_date   date not null,
    list_name       text not null,
    ico             text,
    name            text not null,
    street          text,
    city            text,
    zip             text,
    country         text,
    card_url        text,
    fetch_run_id    bigint not null references meta.fetch_run,
    unique (snapshot_date, list_name, ico, name)
);

create table raw.ares_subject (
    ico          text primary key,
    http_status  integer not null,
    payload      jsonb,
    fetched_at   timestamptz not null default now(),
    fetch_run_id bigint not null references meta.fetch_run
);

create table raw.nbs_entity (
    snapshot_date  date not null,
    nbs_id         text not null,
    name           text not null,
    address        text,
    country        text,
    licence_scopes text[] not null default '{}',
    licences       jsonb,
    fetch_run_id   bigint not null references meta.fetch_run,
    primary key (snapshot_date, nbs_id)
);

create table raw.ruz_unit (
    ico          text primary key,
    unit_id      bigint,
    payload      jsonb,
    statements   jsonb,  -- [{id, period_from, period_to, type, total_assets, equity}]
    fetched_at   timestamptz not null default now(),
    fetch_run_id bigint not null references meta.fetch_run
);

create table raw.cvca_member (
    fetched_on   date not null,
    url          text not null,
    member_class text not null check (member_class in ('full', 'associate')),
    name         text not null,
    website      text,
    posted_on    date,
    profile      jsonb not null default '{}',  -- label -> text as shown on the profile
    fetch_run_id bigint not null references meta.fetch_run,
    primary key (fetched_on, url)
);
