-- Research catalog: the public data sources we evaluated and the commercial competitors.
-- Loaded from data/seed/*.json by investordb.load_seed; every row carries the URLs that back it
-- and the date it was researched.

create table ref.data_source (
    slug              text primary key,
    name              text not null,
    publisher         text,
    jurisdiction      text not null,  -- ISO 3166-1 alpha-2, or EU / CEE / GLOBAL
    category          text not null check (category in (
                          'regulatory_filing', 'regulatory_register', 'company_registry',
                          'public_programme', 'lp_disclosure', 'association', 'news_media',
                          'press_release', 'open_dataset', 'ecosystem_report', 'investor_website',
                          'commercial_free_tier')),
    investor_types    text[] not null default '{}',  -- vc, pe, family_office, angel, private_investor, cvc, fund_of_funds, crowdfunding
    fields_provided   text[] not null default '{}',  -- identity, investor_type, sector_focus, stage_focus, ticket_size, fund_size, aum, portfolio, deal_dates, people, geography
    roles             text[] not null default '{}',  -- discovery, verification, enrichment
    access_methods    text[] not null default '{}',  -- bulk_download, api, html, pdf, search_ui
    url               text not null,
    licence           text,
    cost              text,
    update_cadence    text,
    coverage_estimate text,
    reliability       text check (reliability in ('high', 'medium', 'low')),
    priority          smallint check (priority between 1 and 3),  -- 1 = use in the pilot
    limitations       text,
    notes             text,
    evidence_urls     text[] not null default '{}',
    researched_on     date not null
);

create table ref.competitor (
    slug                text primary key,
    name                text not null,
    owner               text,
    hq_country          text,
    segment             text,
    investor_coverage   text,   -- headline counts as stated, with dates
    coverage            jsonb not null default '[]',  -- [{"metric", "value", "as_of", "basis", "source"}]
    sourcing_methods    text[] not null default '{}', -- web_crawl_ml, analyst_research, surveys, self_reported, community, regulatory_filings, lp_disclosures, news_press, partnerships
    sourcing_notes      text,
    verification_notes  text,
    known_issues        text,
    pricing             text,
    price_usd_year_min  numeric(12, 0),
    price_usd_year_max  numeric(12, 0),
    price_basis         text check (price_basis in ('list_price', 'third_party_estimate', 'vendor_quote', 'unknown')),
    free_tier           boolean,
    api_available       boolean,
    licence_terms       text,
    weak_spots          text,
    url                 text,
    evidence_urls       text[] not null default '{}',
    researched_on       date not null
);

-- Every fetch run must name a catalogued source.
alter table meta.fetch_run
    add constraint fetch_run_source_slug_fkey foreign key (source_slug) references ref.data_source (slug);

-- Liveness checks of evidence URLs (written by investordb.check_links).
create table meta.link_check (
    link_check_id bigint generated always as identity primary key,
    url           text not null,
    checked_at    timestamptz not null default now(),
    http_status   integer,
    final_url     text,
    error         text
);
create index on meta.link_check (url, checked_at desc);
