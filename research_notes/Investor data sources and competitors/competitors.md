# Commercial investor-database market: competitors, coverage, sourcing, verification, pricing (as of 25 Oct 2026)

Conventions used below:
- **[V]** = vendor's own marketing or self-reported claim. **[3P]** = third-party report or estimate (review site, procurement aggregator, blog). **[IND]** = independent or academic source.
- **(pre-2024)** = flags any figure older than 1 Jan 2024. Vendor counts change fast.
- Several vendor pages (PitchBook, OpenVC, SSRN, Medium) returned HTTP 403 to direct fetch. Figures for those come from search-engine snippets or secondary pages and are marked as such.

---

## 1. Coverage and investor profile fields, competitor by competitor

### Takeaway
On investor-entity counts, three groups stand out. The PE/VC platforms are PitchBook (~450K–667K "investors", sources conflict), Crunchbase (~300K) and Dealroom (~250K). The LP and allocator specialists are much smaller but deeper: Preqin (16.6K PE investors), With Intelligence/S&P (~30K) and FINTRX (~4.6K family offices). Founder-facing lists (Signal, OpenVC, Unicorn Nest) hold 16K–38K mostly self-claimed profiles. No vendor publishes a reliable breakdown by investor type (VC / PE / family office / angel), and almost none publishes counts by region.

### Cited Findings

**PitchBook (Morningstar)**
- Investor counts conflict across sources, and all of them come from snippets or secondary pages:
  - 634K+ investors on PitchBook's investor data page (per search snippet; direct fetch was blocked) — [PitchBook](https://pitchbook.com/platform-data/investors) [V]
  - 597K investors in the dataset exposed through Claude's PitchBook integration — [Claude Academy](https://academy.claude.com/tutorials/using-pitchbook-for-investment-research) [3P]
  - 570,000 investors — [ZoomInfo review](https://pipeline.zoominfo.com/sales/pitchbook-review) [3P]
  - "450,000+ investor profiles as of Sept 2026" — [InvestorLists.vc](https://investorlists.vc/blog/crunchbase-vs-pitchbook) [3P, competitor]
  - 423,000+ investor profiles — [Apify scraper listing](https://apify.com/parseforge/pitchbook-investors-scraper) [3P]
  - A further snippet attributed to a PitchBook data page gave "13.4M+ companies, 667K+ investors, 3.2M+ deals, 175K+ funds, 5.1M+ professionals". The underlying page could not be identified or fetched, so this one is unverified.
- Investor profile content: PitchBook's investor product covers PE/VC firms, funds and deals — [PitchBook](https://pitchbook.com/platform-data/investors) [V]. Kaplan & Lerner note that Preqin and PitchBook are "the only major data sources that identify GPs by fund name" — [NBER chapter](https://www.nber.org/system/files/chapters/c13495/c13495.pdf) [IND, 2016 (pre-2024)]
- Regional and stage data: PitchBook's Q3 2025 quantitative report counts active US VC investors and new entrants, using only US investors in US VC deals — [PitchBook Q3 2025](https://files.pitchbook.com/website/files/pdf/Q3_2025_Quantitative_Perspectives_A_Fork_in_the_Road_20179.pdf) [V]
- Headcount (proxy for analyst capacity):
  - 1,748 observed employee profiles in a July 2026 snapshot, ~36% in Seattle; "Research Associate" is the top title at 8.3% — [Unify GTM](https://www.unifygtm.com/insights/headcount/pitchbook) [3P]
  - ~1.8K headcount, Sept 2025 — [Revelio Labs](https://www.reveliolabs.com/companies/pitchbook-data/employees) [3P]
  - PitchBook does not disclose a data-researcher headcount.

**Preqin (BlackRock)**
- PE product page, fetched Oct 2026: "Investor coverage 16,638; Fund coverage 68,822; Active firm coverage 31,653; Fund performance coverage 9,284" — [Preqin PE](https://www.preqin.com/data/private-equity) [V]
- Investor profile fields — [Preqin PE](https://www.preqin.com/data/private-equity) [V]:
  - future PE investment plans
  - active fund searches and mandates
  - full investment history, including prior and current commitments
  - decision-maker contacts and their preferred contact method
  - AUM and dry powder are listed under fund managers, not investors.
- Definition: "investors" means "confirmed, active allocators". Preqin excludes inactive investors, investors active only in other asset classes, investment consultants, fund administrators and GPs committing to their own funds — [Preqin Data Coverage Map](https://www.preqin.com/data/data-coverage-map-view) [V]
- Family offices: 4,592, from Preqin's 2024 "Fundraising from Family Offices" report describing 2023, as cited by competitor Altss. Not confirmed on Preqin's own site — [Altss vs Preqin](https://altss.com/vs/preqin) [3P, competitor]
- Ownership: BlackRock closed the acquisition on 3 Mar 2025. At that point Preqin covered 210,000 private-market funds and had 220,000+ users. It remains a standalone product while being integrated into Aladdin and eFront — [BusinessWire/BlackRock](https://www.businesswire.com/news/home/20250228261104/en/BlackRock-Establishes-Preeminent-Private-Markets-Technology-and-Data-Provider-with-Close-of-Preqin-Acquisition) [V]. Price was about £2.5bn cash — [BlackRock 10-Q](https://www.sec.gov/Archives/edgar/data/2012383/000095017025065838/Financial_Report.xlsx); [Investment Executive](https://www.investmentexecutive.com/news/blackrock-completes-preqin-acquisition-bolstering-its-private-markets-capabilities/)

**Crunchbase**
- About 4M entities (~40% US-based) and ~300K investors, institutional and individual, with 700K+ funding rounds from 1990 to 2024. This comes from the OECD's June 2025 extract — [OECD STI WP 2026/04](https://www.oecd.org/content/dam/oecd/en/publications/reports/2026/03/the-oecd-start-ups-database_6b7828eb/be8e5317-en.pdf) [IND]
- Crunchbase's own data page gives no entity counts. It cites 4,000+ venture partners, 600,000 active contributors, 80M+ users, 1,000+ news and government sources, and 30M+ "verified updates" per year — [About Crunchbase Data](https://about.crunchbase.com/data) [V]
- Investor profile content: number of investments, recent activity and portfolio. Third-party commentary calls this good for building a list but weak for qualifying investors — [Gigaboost](https://gigaboost.ai/blog/crunchbase-not-enough-investor-discovery/) [3P]
- Contact data carries ML confidence scores, and Crunchbase disclaims liability for contact accuracy — [InvestorLists.vc](https://investorlists.vc/blog/crunchbase-vs-pitchbook) [3P]

**Dealroom**
- As of Aug 2026: 3.2M+ companies, 1.5M+ startups and 500K+ European startups. Profiles cover VC firms, PE funds, corporate investors, angels and LPs, but the FAQ gives no investor counts. It records 9,242 VC rounds in Europe and Israel for 2024 — [Dealroom FAQ](https://dealroom.co/faq/) [V]
- More than 250K investors in 900K+ transactions from 1990 to 2024, per the OECD June 2025 extract. Dealroom is "more likely to capture early-stage deals like angel financing, spinouts, and crowdfunding" — [OECD 2026](https://www.oecd.org/content/dam/oecd/en/publications/reports/2026/03/the-oecd-start-ups-database_6b7828eb/be8e5317-en.pdf) [IND]

**CB Insights**
- 13M+ company profiles, marketed as "Double verified". No investor-profile count is published — [CB Insights Data](https://www.cbinsights.com/what-we-offer/data/) [V]
- The Smart Money 2025 analysis covered 12,000+ venture investors with 10+ unique portfolio companies over 2015–2025, which is a lower bound on its active-VC universe — [CB Insights Smart Money 2025](https://www.cbinsights.com/research/smart-money-2025/) [V]

**Tracxn**
- Its own materials:
  - 71,500+ investor profiles and 3.7M+ entities, Nov 2024 investor deck filed with BSE — [BSE filing](https://www.bseindia.com/xml-data/corpfiling/AttachHis/40fbfa81-11f6-4800-824c-792fc368572f.pdf) [V]
  - 72,900+ investor profiles — [Screener.in](https://www.screener.in/company/TRACXN/) [3P relaying company data]
- University guides say "200,000+ investor profiles", which conflicts with the company's figure — [Stanford GSB guide](https://libguides.stanford.edu/library/tracxn); [IIT Roorkee guide](https://mgcl.iitr.ac.in/uploads/traxn.pdf) [3P]

**S&P Capital IQ Pro + With Intelligence (S&P Global)**
- S&P completed its $1.8bn acquisition of With Intelligence on 25 Nov 2025 — [BIIA](https://www.biia.com/sp-global-completes-1-8-billion-acquisition-of-with-intelligence-strengthening-its-position-as-a-leader-in-private-markets-data-analytics/)
- With Intelligence brings ~30,000 investors (PE, private credit, infrastructure, hedge funds, family offices), ~30,000 managers, ~3,000 customers and ~$130M expected 2025 revenue — [Crowdfund Insider](https://www.crowdfundinsider.com/?p=254694) [3P relaying deal materials]
- Since June 2026, Capital IQ Pro's private-markets data comes from With Intelligence. Cambridge Associates benchmarks in the platform cover 2.5K+ managers and 9.5K+ funds — [CIQ Pro June 2026 release notes](https://capitaliq.spglobal.com/releasenotes/announcements/june-2026-sp-capital-iq-pro-release-notes) [V]
- July 2026 integration covers 60M+ private companies — [AlphaMaven](https://alpha-maven.com/story/private-equity/sampp-global-introduces-expanded-private-markets-datasets-from-with-intelligence-into-sampp-capital-iq-pro-tradingview) [3P]
- Before that, a 2024 S&P–Preqin partnership sheet cited 60K+ firms and 196K+ funds — [S&P/Preqin one-pager, Jun 2024](https://www.spglobal.com/marketintelligence/en/documents/spgmi-preqin-partnership_one-pager_ltr_062024.pdf) [V]

**LSEG Workspace / VentureXpert (ex-Refinitiv/Thomson)**
- 46,000+ PE/VC firms, 96,000+ funds and 217,000+ current and former PE/VC-backed companies. Coverage of foreign markets is "select", while the US is well covered — [LSEG PE deals data](https://www.lseg.com/en/data-analytics/financial-data/deals-data/private-equity-data) [V]
- A second LSEG page conflicts: 43,000+ firms, 91,000+ funds, 316,000+ companies — [LSEG Private Markets](https://www.lseg.com/en/data-analytics/private-market-data) [V]
- The Investment Professionals dataset covers 241,000 professionals at 46,000 firms in 70 countries — [LSEG](https://www.lseg.com/en/data-catalogue/company-data/ownership/investment-professionals) [V]

**PEI Group (Private Equity International)**
- 70,000+ funds, 12,000+ actively raising, 11,000+ with performance data. No investor or LP count is given — [PEI Data](https://www.pei.group/solutions/pei-data/) [V]

**Mergermarket (ION Analytics)**
- M&A intelligence backed by "400,000+ deals" since 1998. This comes from a comparison site and is not confirmed by ION. No investor count found — [Multiples.vc compare](https://multiples.vc/compare) [3P]

**FINTRX (family offices and RIAs)**
- 4,600 family offices worldwide in Q2 2026, with 96 added that quarter. The figure comes from a search summary because the PDF was not machine-readable — [FINTRX Q2 2026 report](https://www.fintrx.com/hubfs/_Approved%20Marketing%20Collateral/PDFs%20and%20Reports/FINTRX%20Q2%202026%20Family%20Office%20Report.pdf) [V]
- 4,503 family offices as of 31 Mar 2026. Most newly added multi-family offices are non-SEC-registered international firms — [FINTRX Q1 2026](https://www.fintrx.com/hubfs/FINTRX%20Q1%202026%20Family%20Office%20Intelligence%20Report.pdf) [V]
- April 2024 breakdown — [FINTRX deep dive, Apr 2024](https://www.fintrx.com/blog/a-deep-dive-into-the-fintrx-family-office-dataset) [V]:
  - 1,870+ single-family and 2,130+ multi-family offices; 23,000+ contacts; 42K+ tracked investments
  - typical AUM $100M–$400M
  - preferences: PE 78%, direct investments 71%, real estate 60%; 51% make direct investments
- Also 46,000+ RIA and broker-dealer firms and 802,000+ registered reps — [FINTRX](https://www.fintrx.com/) [V]

**Altrata / Wealth-X**
- The product page gives no counts of dossiers or family offices. Sister products: BoardEx (1.8M executives, 2.2M organisations) and RelSci (10M+ profiles) — [Altrata Wealth-X](https://altrata.com/products/wealth-x) [V]

**Signal by NFX**
- Launched in 2017 with 4,500 investors, mostly Silicon Valley and Israel (pre-2024) — [TechCrunch 2017](https://techcrunch.com/2017/02/23/a-new-way-for-founders-to-connect-with-the-right-vcs/)
- Third-party figures:
  - 18,830+ investors — [Beancount directory](https://beancount.io/de/founder-resources/investor-database) [3P]
  - 349 lists across 103 sectors and 4 stages, per an unaffiliated scraper — [Apify](https://apify.com/johnvc/nfx-signal-investor-api) [3P]
- Profiles show deal histories and connections — [Signal profile example](https://signal.nfx.com/investors/james-currier)

**OpenVC**
- Investor counts vary by source: 20,000+ "verified investors" as advertised, 16,000+ and 5,000+ elsewhere. Fields include check size, lead preference, geography and industry — [Causo OpenVC vs Signal](https://hub.causo.ai/compare/openvc-vs-signal-nfx); [Causo best VC DBs 2026](https://hub.causo.ai/guides/best-vc-databases-find-investors-2026); [OpenScout list](https://openscout.substack.com/p/a-comprehensive-list-of-investor) [3P]

**Unicorn Nest**
- The homepage claims 37,602 investors (VC, CVC, family offices, angel syndicates), 33,253 partners and 226K VC deals, collected since 2019. No type split is given. Country pages include PL, CZ, EE, LV, LT, HU, RO, SK, SI, BG and UA — [Unicorn Nest](https://unicorn-nest.com/); [country index](https://unicorn-nest.com/country/) [V]
- In 2020 it released 26,000 VC funds as a free spreadsheet under a licence that barred academic and commercial use (pre-2024) — [Tech.eu 2020](https://tech.eu/2020/04/29/unicorn-nest-database/)

**Vestbee (CEE)**
- VC list focused on CEE, the Baltics and Europe. Filters: ticket €0–5M+, pre-seed to buyout/PE, ~99 sectors. No total count is shown and access requires login — [Vestbee VC list](https://vestbee.com/vc-list) [V]
- Co-publishes CEE ecosystem reports with Dealroom — [Dealroom/UNIQA/Cogito/Vestbee CEE 2024](https://dealroom.co/uploaded/2024/03/Dealroom-uniqa-cogito-vestbee-CEE-report-2024.pdf)

**Landscape.vc**
- A startup-discovery and deal-sourcing tool, not an investor database. It monitors "15+ alternative data sources" (GitHub trending, Product Hunt, YC launches), refreshes daily, and publishes no investor counts. Page dated 21 Aug 2026 — [Landscape.vc](https://landscape.vc/) [V]

**Harmonic**
- 35M+ companies and 195M+ people; receives "routine portfolio updates from the world's leading investors" — [Harmonic vs Sourcescrub](https://harmonic.ai/blog/harmonic-vs-sourcescrub) [V]

**Grata / Sourcescrub (both now Datasite)**
- Grata was acquired by Datasite in June 2025 (reported $200M+). Sourcescrub was sold to Datasite in Aug 2025 and is being merged into Grata. Sourcescrub covers 16–17M companies from 220–290K sources — [corpdev.ai Grata alternatives](https://www.corpdev.ai/research/grata-alternatives) [3P]

**Inven**
- 28M+ companies, 100M+ entities, 430M+ contacts and 3M+ transactions. Says its data is collected in-house, not licensed from PitchBook, Capital IQ or FactSet. Raised a $12.75M Series A in May 2026 — [corpdev.ai Inven alternatives](https://www.corpdev.ai/research/inven-alternatives) [3P relaying vendor]

**Beauhurst (UK/Germany)**
- Claims coverage of every private company in the UK and Germany — [Beauhurst competitors page](https://www.beauhurst.com/competitors/) [V]

**AngelList**
- No current public count of angels or syndicates found. The only data found is 2015 platform statistics (pre-2024) — [StrictlyVC 2015](https://strictlyvc.com/2015/02/20/naval-ravikant-secondary-deals-quietly-reaching-primary-funding-levels/)

**Other relevant players found (all vendor claims)**
- Altss (family offices): 9,000+ single family offices; pricing from $12,000/yr — [Altss FO DB guide](https://altss.com/blog/best-family-office-databases-for-2025-a-comparison-guide.md); [PrivateEquityList comparison](https://privateequitylist.com/intelligence/investor-database-comparison) [V/3P]
- Venture Capital Archive: 40,000+ family offices and LPs combined — [Venture Capital Archive](https://venturecapitalarchive.com/) [V]
- InveXora Family Office DB: 36,000+ "verified" contacts, "triple-verified" — [parse.gl listing](https://parse.gl/brands/invexoratech-com-2) [V]
- Angel Match: 125,000+ angels and VCs, 99,000+ "verified" emails — [InvestorLists.vc](https://investorlists.vc/blog/crunchbase-vs-pitchbook) [3P]
- InvestorHunt: 110,000+ investors — same source [3P]
- InvestorLists.vc: 8,004 US firms — same source [V]
- Private Equity List: another low-cost investor list — [PrivateEquityList](https://privateequitylist.com/intelligence/investor-database-comparison) [V]

### Inferences
- **Why the large platforms' counts are so much higher:** the ~250K–670K "investor" totals at PitchBook, Crunchbase and Dealroom almost certainly include every entity that appears on a cap table: individual angels, corporates, accelerators, and dormant or one-off investors. Specialist counts (Preqin's 16.6K PE investors, With Intelligence's ~30K) apply an "active allocator" filter. For our product, "real and active" needs an explicit definition (for example, ≥1 publicly sourced investment or commitment in the past 24–36 months) to be comparable.
- **Family-office census:** FINTRX (~4.6K) and Preqin (~4.6K, 2023) are the best-documented counts. Altss's 9K+ SFO claim and other larger figures are unverified marketing. The real global universe is unknown. Incumbents disagree by about 2x.
- **Pace of consolidation:** BlackRock bought Preqin (Mar 2025), S&P bought With Intelligence (Nov 2025), and Datasite bought Grata and Sourcescrub (2025). Independent mid-market alternatives are shrinking, and incumbents' data is moving inside larger workflow suites (Aladdin, Capital IQ Pro, Datasite).

### Gaps
- No vendor publishes counts by investor type (VC / PE / family office / angel) or by region, and none publishes a CEE-specific count. PitchBook, CB Insights and Crunchbase do not publish a current investor count on fetchable pages.
- Wealth-X's family-office dossier count, AngelList's current investor numbers, Mergermarket's investor coverage, Beauhurst's investor count, and Signal's and OpenVC's own official totals: none were found.
- PitchBook pages returned 403, so the 634K vs 667K figures could not be checked against the primary page.

---

## 2. Data sourcing methodology

### Takeaway
The incumbents fall into three models:
1. **Analyst-and-survey heavy:** PitchBook, Preqin, PEI, With Intelligence, FINTRX, Wealth-X. These rely on direct firm contact, FOIA requests to public pensions, and regulatory filings.
2. **Community plus ML:** Crunchbase's 4,000+ venture partners and 600K contributors; Dealroom's 100+ government partners, registries and user submissions; Signal's and OpenVC's self-claimed profiles.
3. **Registry-first:** Beauhurst's Companies House SH01 filings.

Every major vendor combines automated web and news extraction with human review. Their competitive moats are the non-public inputs: surveys, portfolio feeds from VCs exchanged for data access, LP data, and government partnerships. A public-data-only product cannot replicate these.

### Cited Findings
- **Preqin:**
  - "One-to-one conversations form the backbone of our data collection", plus "thousands of sources every day" (regulatory filings, press releases, news, websites). It will "never just use machines" — [Preqin PE](https://www.preqin.com/data/private-equity) [V]
  - Relationships with fund managers and investors since 2003, plus FOIA requests, public filings and news — [Preqin Data Coverage Map](https://www.preqin.com/data/data-coverage-map-view) [V]
  - An "in-house research team of over 450 multi-lingual analysts" who monitor filings and make FOIA requests daily (undated university page) — [UMass Isenberg](https://www.isenberg.umass.edu/centers/center-for-international-securities-and-derivatives-markets/preqin-database) [3P]
  - Performance data comes primarily from public pension filings, FOIA requests to public pensions, and voluntary GP submissions (~60% of performance data) and LP submissions — [Kaplan & Lerner NBER chapter](https://www.nber.org/system/files/chapters/c13495/c13495.pdf) [IND, pre-2024]
- **Crunchbase:** five inputs — [About Crunchbase Data](https://about.crunchbase.com/data) [V]:
  1. "market experts": venture partners and contributors
  2. user-engagement signals from 80M+ users
  3. proprietary ingestion systems
  4. 1,000+ news outlets and government filings
  5. analyst validation
- **Crunchbase Venture Program:** 4,000+ members send monthly portfolio updates in exchange for data access. 600K+ contributors update 100K+ profiles a month (the help page is ~1.5 years old) — [Crunchbase Support](https://support.crunchbase.com/hc/en-us/articles/360009616013-Where-does-Crunchbase-get-their-data) [V]. In 2017 the figures were 3,000+ firms and ~500K contributors — [OECD 2017](https://www.oecd.org/content/dam/oecd/en/publications/reports/2017/11/using-crunchbase-for-economic-and-managerial-research_9ba53344/6c418d60-en.pdf) [IND, pre-2024]
- **Dealroom:** five streams — [Dealroom FAQ](https://dealroom.co/faq/) [V]:
  1. official filings and trade registers
  2. 100+ government and ecosystem partners supplying local data
  3. founder and investor submissions, manually checked
  4. public web (news, job boards, websites)
  5. predictive models
  - The OECD adds domain registries, web and app-store analytics, investor portfolios and third-party data — [OECD 2026](https://www.oecd.org/content/dam/oecd/en/publications/reports/2026/03/the-oecd-start-ups-database_6b7828eb/be8e5317-en.pdf) [IND]
  - The partner count varies across Dealroom's own pages: 100+ (FAQ), "over 90 governments" — [Dealroom vs Crunchbase](https://dealroom.co/dealroom-vs-crunchbase) — and "over 75" — [Dealroom vs PitchBook](https://dealroom.co/dealroom-vs-pitchbook) [V]
- **With Intelligence (S&P):** intelligence "sourced directly from LPs/investment allocators and GPs/fund managers" — [Crowdfund Insider](https://www.crowdfundinsider.com/?p=254694) [3P]
- **PEI:** direct manager and investor submissions, regulatory filings (SEC, FCA and equivalents) and PEI editorial research — [PEI Data](https://www.pei.group/solutions/pei-data/) [V]
- **Beauhurst:**
  - Primary source is SH01 share-allotment filings at Companies House, treated as more reliable than press releases — [Beauhurst blog](https://beauhurst.com/blog/why-investment-data-varies-beauhurst-pitchbook-dealroom/) [V]
  - The ONS, which uses Beauhurst data in its national accounts, confirms that from 2015 Beauhurst captures all filed UK unlisted-equity issuances. Data for 2011–14 covered only announced deals, and only cash-for-shares issuances are counted — [ONS](https://www.ons.gov.uk/economy/nationalaccounts/uksectoraccounts/articles/economicstatisticstransformationprogramme/enhancedfinancialaccountsukflowoffundsusingbeauhurstdatatobetterunderstandtheeconomy) [IND]
- **Signal by NFX:**
  - Investors add themselves to up to 10 lists through their "Investment categories", or a trusted community member adds them. Ranking draws on self-reported data, founder activity, Gmail-derived connectedness and community upvotes — [Signal methodology](https://signal.nfx.com/investor-lists/methodology) [V]
  - Profiles are for investors "highly sought after by Founders and vetted by them and by other investors" — [NFX help](https://products.nfx.com/en/articles/4809095-which-investors-get-an-investing-profile-on-signal) [V]
- **Harmonic:** proprietary web data plus routine portfolio updates from investors — [Harmonic](https://harmonic.ai/blog/harmonic-vs-sourcescrub) [V]
- **Sourcescrub/Grata:** websites, job postings, news, regulatory filings, trade-publication mentions, conference attendee lists and speaker rosters, and industry award lists — [corpdev.ai](https://www.corpdev.ai/research/grata-alternatives) [3P]
- **Inven:** collects and maintains its own data rather than licensing from PitchBook, Capital IQ or FactSet — [corpdev.ai](https://www.corpdev.ai/research/inven-alternatives) [3P]
- **Landscape.vc:** 15+ alternative signal feeds (GitHub, Product Hunt, YC) — [Landscape.vc](https://landscape.vc/) [V]
- **Wealth-X:** dossiers are "built, verified and updated by a team of 400+ researchers" — [Altrata](https://altrata.com/products/wealth-x) [V]
- **FINTRX:** a "75+ person research team" tracks family-office direct investments (Apr 2024) — [FINTRX](https://www.fintrx.com/blog/a-deep-dive-into-the-fintrx-family-office-dataset) [V]
- **PitchBook:** a job listing says the core product depends on analysts who "collect, verify, structure, and enrich private market data". A Seattle Senior Analyst role was posted in July 2025 at $150K–$200K — [Simplify job post](https://simplify.jobs/p/210d2b26-f6ee-4b62-93c3-48769dec8d1c/Senior-Analyst) [3P]
- **EBAN (angel statistics body, not a vendor):** sources angel activity from business angel networks, national associations, Dealroom, PitchBook and Crunchbase — [EBAN Compendium 2024](https://www.eban.org/wp-content/uploads/2025/12/Stats-Compendium-2024.pdf) [IND]

### Inferences
- What incumbents have that public data can't replace:
  - private feeds from VCs who trade portfolio data for access (Crunchbase, Harmonic)
  - LP and GP surveys and calls (Preqin, With Intelligence, PEI, PitchBook)
  - government data partnerships (Dealroom)
  - large analyst benches: Preqin 450+, Wealth-X 400+, FINTRX 75+
- A public-only product therefore competes on transparency and citability (every field carries a source URL and date) rather than on breadth of private fields.
- Our own build inputs largely overlap with what incumbents already use publicly: SEC Form D/ADV, Companies House, pension FOIA disclosures, press releases and fund websites. Public-data parity is achievable.
- Cost: for a global analyst-verified build, incumbents' staffing is the benchmark. Preqin (450+ analysts) and Wealth-X (400+ researchers) suggest that verifying records at scale needs hundreds of FTEs unless verification is automated.

### Gaps
- PitchBook's methodology page could not be fetched (403). No public PitchBook researcher headcount or survey response rate was found.
- No vendor discloses the share of investor records that come from surveys vs crawling vs self-submission.

---

## 3. Verification / QA claims and documented accuracy problems

### Takeaway
Every vendor claims "human-verified" data, but none publishes record-level accuracy metrics for investor profiles. Users repeatedly report the same problems: stale data (PitchBook ownership and deal tags, Crunchbase missing or outdated records), unverifiable contact emails, and inconsistent investor-type tags. Academic work documents systematic biases: missing small rounds, under-reported failures, stale self-reported performance, and US- or Europe-centric coverage.

### Cited Findings
- **Crunchbase claims:** "AI grading algorithms" plus human validation, continuous benchmarking against external sources, and a global analyst team. It reports 84% of funding events "anticipated" by its predictions, but the 16K+ vs 14K+ "correctly predicted events" figure is inconsistent within its own page. No method for these figures is disclosed — [About Crunchbase Data](https://about.crunchbase.com/data) [V]
- **Dealroom claims:** "AI-powered data collection verified by humans". Partners help catch errors, and corrections are reviewed before publishing — [Dealroom FAQ](https://dealroom.co/faq/); verification by its "Intelligence Unit" — [Dealroom About](https://dealroom.co/about/) [V]
- **Preqin claims:** "During validation, we cross check data… and clarify data points directly" with the firms concerned — [Preqin](https://www.preqin.com/data/data-coverage-map-view) [V]
- **PEI claims:** "Every record is reviewed and validated by PEI's research team". Unverifiable data is "flagged or excluded rather than published" — [PEI Data](https://www.pei.group/solutions/pei-data/) [V]
- **Wealth-X claims:** details are "substantiated by two independent, credible sources" — [Altrata](https://altrata.com/products/wealth-x) [V]
- **CB Insights claims:** "Double verified" — [CB Insights](https://www.cbinsights.com/what-we-offer/data/) [V]
- **PitchBook user complaints (G2):**
  - "outdated information on niche companies", 36 reviews
  - "financial information and deal tags often do not match reality", 20 reviews
  - one example: PE ownership still listed years after the company was sold
  - [G2 PitchBook reviews](https://g2.com/products/pitchbook/reviews) [3P]
- **PitchBook user complaints (TrustRadius):** 21% of reviewers raise timeliness of updates — [TrustRadius](https://trustradius.com/products/pitchbook/reviews/all) [3P]
- **Crunchbase user complaints:** G2 cons include "Missing Information" (17 reviews) and "Outdated Information" (15). Contact-data accuracy is rated 7.7/10 across 140 reviews — [G2 compare](https://www.g2.com/compare/crunchbase-vs-people-data-labs-vs-pitchbook) [3P]
- **Contact data quality:**
  - Tracxn provides personal emails only "in many cases"
  - Crunchbase disclaims contact accuracy
  - Angel Match and InvestorHunt claim "verified" emails but publish no verification methodology (as of Sept 2026)
  - [InvestorLists.vc](https://investorlists.vc/blog/crunchbase-vs-pitchbook) [3P]
- **Investor-type tagging (OECD):** Crunchbase and Dealroom investor-type tags are "not harmonised". They "do not allow for a proper understanding" of government ownership, so the OECD had to survey member countries to validate 308 government-VC entities across 38 economies. CVC arms are not identified as such, so the OECD compiled them manually from Thomson Reuters Eikon — [OECD 2026](https://www.oecd.org/content/dam/oecd/en/publications/reports/2026/03/the-oecd-start-ups-database_6b7828eb/be8e5317-en.pdf) [IND]
- **Registration lag (OECD):** both Crunchbase and Dealroom register innovative startups at an average age of about 3 years. Coverage before each platform's launch (2007 and 2013) is incomplete, which causes survivorship bias — [OECD 2026](https://www.oecd.org/content/dam/oecd/en/publications/reports/2026/03/the-oecd-start-ups-database_6b7828eb/be8e5317-en.pdf) [IND]
- **Undisclosed rounds (Beauhurst):** Beauhurst says unannounced rounds make up 70% of UK investment activity — [Beauhurst blog](https://beauhurst.com/blog/why-investment-data-varies-beauhurst-pitchbook-dealroom/). Its comparison page says ~50% — [Beauhurst vs Dealroom](https://www.beauhurst.com/lp/beauhurst-vs-dealroom/) [V, internally inconsistent]
- **VentureXpert dispute:** in 2011 Rüdiger Stucke challenged VentureXpert's reliability for PE/VC performance, and Thomson Reuters rejected the critique (pre-2024) — [ai-CIO](https://www.ai-cio.com/news/after-virulent-attack-thomson-reuters-defends-popular-pe-venture-capital-database/)
- **AI-generated family-office lists:** these "contain the same 50 famous names… mixed with outdated entries, dissolved entities" — [FamilyOfficeHub](https://familyofficehub.io/blog/can-ai-build-a-family-office-list-what-chatgpt-and-claude-misses-in-2026/) [V, competitor with interest]
- **Signal's model:** self-listing on Signal sits awkwardly with NFX's description of profiles as "vetted", so it should not be treated as a census — [Signal methodology](https://signal.nfx.com/investor-lists/methodology); [NFX help](https://products.nfx.com/en/articles/4809095-which-investors-get-an-investing-profile-on-signal)

### Inferences
- No incumbent offers per-field provenance (a source URL plus date) to the end user. "Verified" is an unaudited label across the market. A citable source and date on every investor field would be a real point of difference, and auditable accuracy (for example, published sample-based precision on ticket size, AUM and activity status) could be a marketing wedge.
- Stale "active" status is the most common complaint. A product that dates and re-checks activity status (last observed investment, last fund close) addresses the main pain point directly.

### Gaps
- No independent, published accuracy audit of investor-level fields (AUM, ticket size, sector focus) for any vendor was found. Existing benchmarks test deal and round data, not investor-profile attributes.
- G2 and TrustRadius counts are self-selected snapshots, not representative samples.

---

## 4. Academic literature benchmarking VC/PE database accuracy and coverage

### Takeaway
Academic benchmarks consistently find that:
- no single database is complete
- larger rounds and successful funds are over-represented
- failures are under-reported
- self-reported performance data is stale
- databases complement each other geographically (Crunchbase is US-centric, Dealroom Europe-centric, with only ~30% entity overlap)

Most rigorous studies predate 2024 and test deals and funds, not investor profiles.

### Cited Findings
- **Kaplan & Lerner (2016), "Venture Capital Data: Opportunities and Challenges"**, NBER WP 22500 — [NBER](https://www.nber.org/papers/w22500); chapter text — [NBER chapter PDF](https://www.nber.org/system/files/chapters/c13495/c13495.pdf) [IND, pre-2024]:
  - VentureXpert (VX) and VentureSource (VS) show "large inconsistencies… and a general problem of incompleteness", and both show quality deterioration over the prior decade. VX has more complete investment coverage; VS measures outcomes more accurately.
  - Across 449 firms present in both, VX has ~40% more financing rounds and ~10% more post-money valuations.
  - VX reports <10% of investments as defunct when >20% actually are.
  - VS tends to exclude failed funds, which likely biases performance upward.
  - Kaplan, Sensoy & Strömberg (2002), checked against 143 actual financings, found VS had almost twice as many valuations as VX, with average absolute error 60% of VX's.
  - Performance-data coverage: Burgiss covers ~90% of capital committed to VC (72% of committed capital for 2000–2008 vintages as of 2014 Q2). Preqin had performance data for ~70% of committed capital in the 2000s.
  - Preqin biases: misses top funds without public-pension LPs (for example, Sequoia and Accel); data is stale because responses are tardy; reports IRRs without cash flows. Cambridge Associates is biased toward successful GPs.
- **Kaplan, Sensoy & Strömberg (2002):** the databases "exclude roughly 15% of the financing rounds" — [Management Science supplement](https://pubsonline.informs.org/doi/suppl/10.1287/mnsc.2016.2482/suppl_file/mnsc.2016.2482-sm.pdf) [IND, pre-2024]
- **Maats, Metrick, Yasuda, Hinkes & Vershovski (2011):** 40 VC funds with vintages 1992/93–2003. Consistency between VX and VS is "low". VX is more reliable for fund-level work, and fund coverage rises with the number of portfolio companies — [Management Science supplement](https://pubsonline.informs.org/doi/suppl/10.1287/mnsc.2016.2482/suppl_file/mnsc.2016.2482-sm.pdf); [NBER chapter](https://www.nber.org/system/files/chapters/c13495/c13495.pdf) [IND, pre-2024]
- **Retterath & Braun (2020), "Benchmarking Venture Capital Databases":** 8 databases tested against verified data on 339 rounds at 108 mostly European companies — [SSRN 3706108](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3706108); [Semantic Scholar](https://www.semanticscholar.org/paper/Benchmarking-Venture-Capital-Databases-Retterath-Braun/41c045f31f6f1461398012087917c492bf8a9ecf) [IND, pre-2024]:
  - VentureSource, PitchBook and Crunchbase "have the best coverage, and are the most accurate".
  - Larger rounds, and their sizes and valuations, are more likely to be reported.
  - Crunchbase offers the best value for price.
  - Crunchbase over-represents IT, software, biotech and healthcare.
- **Retterath & Oechel (2024) follow-up:** original data on 161 companies, 460 rounds and 554 institutional investors, tested against CB Insights, Crunchbase, Dealroom, PitchBook, Preqin, S&P Capital IQ, Tracxn and VentureXpert. 46% of VCs say finding the right data source is their biggest pain point in becoming data-driven. Per-database results could not be retrieved (Medium returned 403) — [Retterath on X](https://x.com/AndreRetterath/status/1792941859691479306); [Medium](https://medium.com/@andreretterath/what-s-the-best-startup-vc-database-8237fc189830)
- **OECD Start-ups Database (Berger et al., STI WP 2026/04; data snapshot June 2025)** — [OECD 2026](https://www.oecd.org/content/dam/oecd/en/publications/reports/2026/03/the-oecd-start-ups-database_6b7828eb/be8e5317-en.pdf) [IND]:
  - Entity overlap: only ~30% of entities appear in both Crunchbase and Dealroom (<20% in Latin America). Crunchbase uniquely covers >40% of North American entities. In Europe, each source uniquely covers ~35% of entities.
  - Deal overlap is higher: non-matching transactions are <30% everywhere, and in North America ~85% of deals appear in both. Dealroom adds more unique European and African deal volume.
  - In 2024, companies found only in Crunchbase raised $160bn (mostly North America). Companies found only in Dealroom raised $80bn (mostly Europe and Asia-Oceania).
  - Compared with national VC associations, the combined database shows higher deal volume: Europe +104.43%, Japan +364.23%, Korea +165.63%, Australia +200.40%, Türkiye +164.03%. The US figure is only ~27% above the NVCA, which itself sources from PitchBook. The OECD's reading is that Crunchbase and PitchBook have similar US deal coverage.
  - Crunchbase is the researchers' preferred source, with US coverage "broadly similar" to CB Insights, Tracxn, Capital IQ and AngelList (citing Retterath & Braun 2020; Dalle, den Besten & Menon 2017).
  - Preqin and PitchBook "remain investor-oriented".
- **Dalle, den Besten & Menon (2017), "Using Crunchbase for economic and managerial research"**, OECD STI WP 2017/08 — [OECD 2017](https://www.oecd.org/content/dam/oecd/en/publications/reports/2017/11/using-crunchbase-for-economic-and-managerial-research_9ba53344/6c418d60-en.pdf) [IND, pre-2024]
- **EBAN 2024 Compendium (angel market):** only the "visible" angel market can be measured: €1,220M across 39 countries in 2024, 4,582 rounds, an estimated ~47,610 angels. EBAN historically used a 10x multiplier for the invisible market and has now deferred total-market estimates. Visible figures "underestimate the actual overall investment activity" — [EBAN Compendium 2024](https://www.eban.org/wp-content/uploads/2025/12/Stats-Compendium-2024.pdf) [IND]

### Inferences
- The literature supports positioning around documented incumbent blind spots: Europe outside major hubs, Asia, angels (the market is mostly invisible) and failed or inactive funds. The low entity overlap (~30%) suggests a public-data build focused on under-covered regions can add records incumbents lack, especially outside North America.
- No academic study benchmarks investor-profile attributes (AUM, ticket size, sector focus) across vendors. That is an open opportunity: a published benchmark of our own accuracy against incumbents would be novel.

### Gaps
- Per-database results of the 2024 Retterath & Oechel benchmark, and exact coverage percentages from Retterath & Braun 2020, could not be retrieved (SSRN and Medium returned 403).
- No academic study specifically on family-office or CEE investor coverage was found.

---

## 5. Pricing and data-licence terms

### Takeaway
The market has a steep price ladder. Founder-facing lists cost $0–$1,000 a year (Signal free, Crunchbase Pro ~$588/yr). Mid-tier tools cost $6.5K–$40K a year (Tracxn, Dealroom ~€12.6K for 3 seats, Grata, Harmonic). Institutional platforms cost $20K–$125K a year (PitchBook median ~$30K, CB Insights ~$47K, Preqin ~$49K). Licences uniformly restrict use to internal business purposes and prohibit bulk export, redistribution and building competing products. That makes incumbent data unusable as a seed for our database. It also makes openly licensed, citable data a differentiator.

### Cited Findings
- **PitchBook (all third-party estimates):**
  - Quote-only. Vendr median ~$30,000/yr, range $20K–$124K, ~14% average negotiated savings; additional seats ~$7K/yr; 1-year minimum, no monthly billing. Tiers were reportedly renamed Core, Pro and Pro Plus in March 2026. CostBench, verified 11 Oct 2026, notes the Vendr source "no longer loads" — [CostBench](https://costbench.com/software/financial-data-terminals/pitchbook/) [3P]
  - $12K–$20K per seat — [VCBeast](https://vcbeast.com/pitchbook-vs-crunchbase) [3P]
  - Vendr list estimate $20K–$40K+ per seat — [Prova](https://www.provaapi.com/blog/pitchbook-api-pricing) [3P]
- **PitchBook licence:**
  - Raw Data may be placed in work product only if it "has no material independent commercial value" — [PitchBook Content License Agreement](https://pitchbook.com/content-license-agreement) (per search snippet; direct fetch blocked) [V]
  - Use is limited to "Licensee's internal business operations" — [Lumonic-hosted copy](https://www.lumonic.com/footer/license-agreement)
  - Users may not "download or export substantial portions… as raw data on a standalone basis" or use the data "to develop, improve, or provide a product… that competes with PitchBook" — [OpenAI financial-services terms reproducing PitchBook terms](https://openai.com/policies/financial-services-terms/)
  - Export caps such as 1,000 rows a day appear in a UK government order form — [U of Toronto](https://onesearch.library.utoronto.ca/pitchbook)
  - Academic licences prohibit data mining — [Yale Library](https://library.yale.edu/eresources/access/access-pitchbook)
- **Crunchbase:**
  - Pro $49/user/mo billed annually (~$588/yr) or $99 monthly; Business ~$199/user/mo; 10 free contacts a month, then paid packs ($29 for 100 up to $99 for 500); exports ~2,000 rows/mo on Pro and 5,000/mo on Business (Sept 2026) — [InvestorLists.vc](https://investorlists.vc/blog/crunchbase-vs-pitchbook); [Vendr](https://www.vendr.com/marketplace/crunchbase) [3P]
  - Enterprise/API: no published price; Vendr-reported median ~$20,000/yr across 71 purchases, range $4,440–$51,377; 200 requests/min per key — [Vendr](https://www.vendr.com/marketplace/crunchbase); [ZoomInfo Crunchbase API review](https://pipeline.zoominfo.com/sales/crunchbase-api) [3P]
  - The free API tier is reported gone in 2026 — [DEV Community](https://dev.to/agenthustler/crunchbase-api-in-2026-free-tier-gone-what-startup-data-hunters-do-now-1177) [3P]
  - Terms and robots.txt prohibit scraping, and resale requires authorisation (secondary sources) — [ScrapeOps](https://scrapeops.io/websites/crunchbase/); [webscraping.ai](https://webscraping.ai/faq/crunchbase-scraping/can-i-sell-the-data-i-scrape-from-crunchbase) [3P]
- **Dealroom:**
  - Premium ~€12,500–12,600/yr with a 3-seat minimum, up to ~€41,000 for 20 seats; Premium Plus ~€17,000/yr — [Peony](https://www.peony.ink/blog/venture-capital-software-solutions); [corpdev.ai](https://www.corpdev.ai/research/pitchbook-alternatives) [3P]
  - Business emails are credit-metered, with 3,000 credits on Premium Plus — [InvestorLists.vc](https://investorlists.vc/blog/crunchbase-vs-pitchbook) [3P]
  - Billed annually. API is a separate plan, and there is an MCP server for AI agents. Free public no-auth endpoints exist. Bulk export and API require paid plans, and licence terms are not published in the FAQ — [Dealroom FAQ](https://dealroom.co/faq/) [V]
- **Preqin:** Vendr median $49,334 (low $27,674, high $77,221) — [Investables](https://investables.ai/blog/how-much-does-preqin-cost) [3P]. $15K–$75K+/yr depending on asset classes — [Multiples.vc](https://multiples.vc/compare/pricing) [3P]
- **CB Insights:**
  - ~$40K–$60K for 1–3 seats, median ~$47K — [corpdev.ai](https://www.corpdev.ai/research/cb-insights-alternatives) [3P]
  - $46,984 verified purchase median — [CostBench](https://costbench.com/best/best-pitchbook-alternatives/) [3P]
  - $40K–$100K per team — [Multiples.vc](https://multiples.vc/compare/pricing) [3P]
  - 90-day cancellation notice in standard terms — [InvestorLists.vc](https://investorlists.vc/blog/crunchbase-vs-pitchbook) [3P]
- **Tracxn:** free "Lite" tier; ~$550/mo individual (SaaSworthy); team licences $6,500–$15,000/yr — [Multiples.vc](https://multiples.vc/compare/pricing) [3P]. ~$500/mo — [InvestorLists.vc](https://investorlists.vc/blog/crunchbase-vs-pitchbook) [3P]
- **Harmonic:** ~$10K–$30K/yr (API-scoped estimate) — [Multiples.vc](https://multiples.vc/compare/pricing) [3P]
- **Grata:** $15K–$40K/yr; a Vendr-based 25-seat range of $28K–$155K — [CostBench Grata vs PitchBook](https://costbench.com/compare/grata-vs-pitchbook/) [3P]
- **Altss:** from $12,000/yr for family-office coverage. **Private Equity List** Pro: $129/mo — [PrivateEquityList](https://privateequitylist.com/intelligence/investor-database-comparison) [3P/V]
- **Low-cost founder lists:** Angel Match $59–$349/mo with export caps of 100–1,200 rows/mo; InvestorHunt $57–$297/mo; InvestorLists.vc $997/yr — [InvestorLists.vc](https://investorlists.vc/blog/crunchbase-vs-pitchbook) [3P/V]
- **Landscape.vc:** $30 for a 30-day trial; per-seat monthly pricing in 3 tiers, no annual commitment — [Landscape.vc](https://landscape.vc/) [V]
- **Unicorn Nest:** "FREE Investor Database" on its homepage; current paid pricing not found. Its 2020 dataset licence barred academic and commercial use, and in 2020 it charged $5 per AI-match query (pre-2024) — [Unicorn Nest](https://unicorn-nest.com/); [Tech.eu 2020](https://tech.eu/2020/04/29/unicorn-nest-database/)
- **Beauhurst, FINTRX, Wealth-X, PEI, LSEG, Capital IQ, Mergermarket:** no published prices; quote or demo only — [Beauhurst pricing](https://www.beauhurst.com/de/pricing/); [PEI](https://www.pei.group/solutions/pei-data/); [Altrata](https://altrata.com/products/wealth-x) [V]
- **Signal by NFX:** free to founders (implied by the platform model; no price page reviewed). OpenVC pricing could not be fetched (403).

### Inferences
- **Price positioning:** a public-data product with citations could sit between the founder lists (<$1K/yr) and Dealroom/Tracxn (~$6.5K–$17K/yr). It could add an open or attribution-friendly API licence, because every incumbent forbids redistribution and competitive use.
- **Gap in the middle of the ladder:** no incumbent sells an affordable, exportable, redistributable investor dataset. Licence terms, not price alone, are the gap.
- **Build-cost benchmark:** institutional ACVs ($30K–$50K) support analyst-heavy models such as Preqin and PitchBook. A sub-$10K product needs automated extraction and verification, with humans reviewing only exceptions.

### Gaps
- Nearly all prices are third-party estimates; vendors publish list prices only for Crunchbase self-serve. Vendr's primary pages were not reachable.
- No pricing was found for FINTRX, Wealth-X, Beauhurst, LSEG, Capital IQ Pro, PEI, Mergermarket, OpenVC or Signal premium features.
- The full Crunchbase ToS and Dealroom licence terms were not retrieved directly.

---

## 6. Gaps and opportunities for a public-data-only product

### Takeaway
Incumbents are documented as weak in six areas:
1. Investor-attribute fields (ticket size, AUM) for non-institutional investors
2. Angels (the market is largely "invisible")
3. Family offices (counts disagree about 2x and most offices are non-registered)
4. Geography outside the US and Western Europe, including CEE
5. Freshness of "active" status
6. Provenance: no per-field citations, and licences forbid reuse

A public-data-only product can't match proprietary survey and LP data. It can win on citable provenance, freshness dating, under-covered regions and an open licence.

### Cited Findings
- **Geography:**
  - Crunchbase is US-centred (~40% of entities US) and Dealroom Europe-centred. Only ~30% of entities overlap, and coverage is "heterogeneous across countries and over time" — [OECD 2026](https://www.oecd.org/content/dam/oecd/en/publications/reports/2026/03/the-oecd-start-ups-database_6b7828eb/be8e5317-en.pdf) [IND]
  - LSEG/VentureXpert covers foreign markets only selectively — [LSEG](https://www.lseg.com/en/data-analytics/financial-data/deals-data/private-equity-data) [V]
  - Retterath & Braun found sampling biases by geography, industry and stage — [Medium summary](https://medium.com/@andreretterath/what-s-the-best-startup-vc-database-8237fc189830) [IND, pre-2024]
- **CEE specifically:** CEE-specific vendors are small and opaque. Vestbee shows no count — [Vestbee](https://vestbee.com/vc-list). Unicorn Nest claims 37,602 investors overall, with CEE country pages — [Unicorn Nest](https://unicorn-nest.com/). EBAN says CEE "remains structurally smaller and more uneven" in angel and early-stage activity — [EBAN 2024](https://www.eban.org/wp-content/uploads/2025/12/Stats-Compendium-2024.pdf) [IND]
- **Angels:** only the "visible" angel market is measurable. EBAN estimates ~47,610 angels across measured European countries, sourced partly from PitchBook and Dealroom, and says visible figures underestimate actual activity — [EBAN 2024](https://www.eban.org/wp-content/uploads/2025/12/Stats-Compendium-2024.pdf) [IND]. Larger rounds are more likely to be reported — [Retterath & Braun](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3706108) [IND]
- **Family offices:**
  - Counts range from ~4.5K–4.6K (FINTRX 2026; Preqin 2023) to 9K+ (Altss claim) — [FINTRX Q1 2026](https://www.fintrx.com/hubfs/FINTRX%20Q1%202026%20Family%20Office%20Intelligence%20Report.pdf); [Altss](https://altss.com/vs/preqin)
  - Most newly added multi-family offices are non-SEC-registered internationals, so SEC filings alone miss them — [FINTRX Q1 2026](https://www.fintrx.com/hubfs/FINTRX%20Q1%202026%20Family%20Office%20Intelligence%20Report.pdf) [V]
  - Crunchbase and Dealroom lump angel groups, family offices and individuals together in their category mappings (OECD annex Figure A.8) — [OECD 2026](https://www.oecd.org/content/dam/oecd/en/publications/reports/2026/03/the-oecd-start-ups-database_6b7828eb/be8e5317-en.pdf) [IND]
- **Investor-type quality:** government-VC and CVC identification needed manual OECD work — [OECD 2026](https://www.oecd.org/content/dam/oecd/en/publications/reports/2026/03/the-oecd-start-ups-database_6b7828eb/be8e5317-en.pdf) [IND]
- **Ticket size and AUM:**
  - Preqin profiles list AUM and dry powder for fund managers, not investors — [Preqin PE](https://www.preqin.com/data/private-equity) [V]
  - Crunchbase investor profiles focus on investment counts and portfolio rather than qualification fields — [Gigaboost](https://gigaboost.ai/blog/crunchbase-not-enough-investor-discovery/) [3P]
  - Founder tools (OpenVC, Vestbee) carry check-size fields, but these are largely self-reported — [Causo](https://hub.causo.ai/compare/openvc-vs-signal-nfx); [Vestbee](https://vestbee.com/vc-list)
- **Stale data:** PitchBook (G2: 36 reviews on outdated information; TrustRadius: 21% raise timeliness) — [G2](https://g2.com/products/pitchbook/reviews); [TrustRadius](https://trustradius.com/products/pitchbook/reviews/all). Preqin's voluntary reporting causes "somewhat stale data" — [Kaplan & Lerner](https://www.nber.org/system/files/chapters/c13495/c13495.pdf) [IND, pre-2024]
- **Undisclosed deals:** 50–70% of UK investment activity is unannounced and visible only through registry filings — [Beauhurst](https://beauhurst.com/blog/why-investment-data-varies-beauhurst-pitchbook-dealroom/) [V]. National registries (where machine-readable) are therefore a public source that press-release-based vendors miss.
- **Licensing:** PitchBook bans competitive use and bulk raw-data export — [OpenAI/PitchBook terms](https://openai.com/policies/financial-services-terms/). Crunchbase bans scraping and resale — [ScrapeOps](https://scrapeops.io/websites/crunchbase/) [3P]

### Inferences
- **Positioning wedges:**
  1. Per-field citation and as-of date, which no incumbent offers.
  2. Explicit "active" status with a last-observed-activity date.
  3. Depth in CEE and other under-covered regions, using national registries plus local-language news and fund websites.
  4. A family-office and angel layer built from public signals (cap-table filings, press, LinkedIn-style public bios, court and registry records), labelled with confidence levels.
  5. Permissive data licensing and an API at a mid-market price.
- **Fields that will be hard from public data alone:** AUM and dry powder for family offices and angels, and typical ticket size for non-VC investors. Expect these to be sparse, and present them as estimated ranges with sources rather than point values. That is more honest than incumbents' unexplained figures.
- **Build-cost benchmarks:** incumbents' analyst benches (Preqin 450+, Wealth-X 400+, FINTRX 75+) and Crunchbase's 600K-contributor community show the human cost of verification. A global public-data build should plan for automated extraction plus targeted human QA on high-value or uncertain records, and publish sample-based accuracy metrics. No vendor currently does this, and it fills the academic gap on investor-attribute accuracy.

### Gaps
- No quantitative per-region (CEE) coverage comparison between incumbents was found. OECD figures are at continent level.
- No study quantifies the share of investor profiles with ticket-size or AUM populated, for any vendor.
- The size of the global family-office and active-angel universe is not established by any independent source in this research; adjacent researchers covering government and registry sources may have relevant counts.
