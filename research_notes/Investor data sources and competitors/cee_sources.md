# CEE (Slovakia and Czechia) public data sources for identifying and verifying active VC, PE, family office and angel investors

Research date: 2026-10-25. "Accessed 2026-10-25" means the live page was read on that date. Items dated before 2024 are flagged **[pre-2024]**. Paywalled or unverified claims are flagged **[paywall]** or **[unverified]**.

---

## 1. Slovakia: regulatory, registry, public-programme, association and news sources

### Takeaway
Slovakia has one excellent machine-readable source, the RÚZ Open API (JSON, CC0, structured financial-statement line items, updated during the day). It also has a free RPO company-register API and a small NBS register of supervised and "registered" (sub-threshold) fund managers, but that register is HTML only. The best investor seed lists are SLOVCA's 12 full members and Slovak Investment Holding's (SIH) public programmes (Venture to Future Fund, and the 2026–2030 start-up fund-manager tender). The investor universe is small.

### Cited Findings

**Národná banka Slovenska (NBS) – collective investment registers**
- NBS keeps a "Register of Managers" for registered (sub-threshold) AIF managers. It links to it at `https://subjekty.nbs.sk/?s=1059` within the general Financial Entities Register (`https://subjekty.nbs.sk/`, English via `?ll=en`). — [NBS registered managers page](https://nbs.sk/en/financial-market-supervision1/supervision/collective-investment/registered-managers/) (accessed 2026-10-25)
- The sub-threshold exemption (§31a(1), Act 203/2011 on collective investment) applies when total AuM including leverage is ≤ €100m, or ≤ €500m where the AIFs are unleveraged and have no redemption rights for 5 years. — [NBS registered managers page](https://nbs.sk/en/financial-market-supervision1/supervision/collective-investment/registered-managers/)
- New rules: registered managers must add the designation "manager of sub-threshold risk capital funds" to their business name by 30 Dec 2026 (change request by 31 Dec 2026). From 1 Jun 2026 NBS may remove a manager from the register by decision, even without a request. This should make the "registered" list cleaner and easier to identify as VC/PE. — [NBS registered managers page](https://nbs.sk/en/financial-market-supervision1/supervision/collective-investment/registered-managers/)
- Registered managers must calculate AuM under the AIFMD Delegated Regulation and report under NBS Decree 1/2015. These reports are not public. — [NBS registered managers page](https://nbs.sk/en/financial-market-supervision1/supervision/collective-investment/registered-managers/); [Vestník NBS 2/2015 (Decree 1/2015)](https://nbs.sk/_img/Documents/_Legislativa/_Vestnik/ciastka2V-2015.pdf) **[pre-2024 legal text]**
- Counts on the collective-investment register page (accessed 2026-10-25):
  - "Správcovské spoločnosti a zahraničné správcovské spoločnosti": 368. This appears to include foreign passported managers.
  - "Registrované subjekty": 39
  - Slovak funds: 92
  - Foreign funds: 1,049
  - Entities with terminated authorisation: 18 / 708
  - No CSV/XLS/XML export button is visible. A generic "Databáza na stiahnutie" menu item exists, but its content is not verified.
  — [subjekty.nbs.sk](https://subjekty.nbs.sk/?s=1059)
- NBS published a Q&A on applying the Act to registered managers (June 2024, updated Dec 2024). — search result on [nbs.sk registered managers](https://nbs.sk/en/financial-market-supervision1/supervision/collective-investment/registered-managers/) (Q&A document itself not opened)
- The NBS registered-managers page does not mention EuVECA. — [NBS registered managers page](https://nbs.sk/en/financial-market-supervision1/supervision/collective-investment/registered-managers/)

**Register právnických osôb (RPO) and ORSR**
- RPO is run by the Statistical Office at rpo.statistics.sk. It is described as a free, unauthenticated public API covering:
  - name, legal form, status, address and share capital
  - activities and statutory bodies
  - "stakeholders" (shareholders) and statistical codes
  — [Topograph developer docs](https://docs.topograph.co/essentials/slovakia) (third-party); [RPO manual](https://rpo.statistics.sk/manual.pdf)
- A third-party MCP listing says RPO data is open government data under CC-BY 4.0, with no API key, and covers more than 1.4m entities. — [mcp.so SK registers](https://mcp.so/ja/servers/sk-registers-mcp) **[unverified, third-party]**
- An older article says the public RPO version is informational only and not legally binding. The binding version is restricted to state bodies. — [podnikajte.sk](https://www.podnikajte.sk/obchodne-pravo/register-pravnickych-osob) **[pre-2024]**
- RPO also assigns IČO numbers online. — [slovensko.sk](https://www.slovensko.sk/sk/zivotne-situacie/zivotna-situacia/_register-a-identifikator-pravn1/)

**Register partnerov verejného sektora (RPVS – beneficial owners)**
- RPVS is run by the Ministry of Justice under Act 315/2016 (in force since 2017) and kept only in electronic form. It holds public-sector partners, their beneficial owners (KUV, always natural persons) and the "oprávnená osoba". The Ministry says data is also published in structured, machine-processable form. — [justice.gov.sk RPVS](https://www.justice.gov.sk/sluzby/register-partnerov-verejneho-sektora/)
- Open Ownership republishes RPVS in BODS format (snapshot 2025-01-09) under the Open Data Commons Attribution licence and warns that its mappings are still in development. — [Open Ownership BODS – Slovakia](https://bods-data.openownership.org/source/slovakia)

**Register účtovných závierok (RÚZ) Open API – financial statements**
- RÚZ Open API v2.5 returns JSON. Endpoints:
  - lists: `/api/uctovne-jednotky`, `/api/uctovne-zavierky`, `/api/uctovne-vykazy`, `/api/vyrocne-spravy`
  - details: `/api/uctovna-jednotka?id=`, `/api/uctovny-vykaz?id=`, etc.
  - templates: `/api/sablona`, `/api/sablony`
  - classifiers, including `/api/sk-nace` and `/api/pravne-formy`
  - attachments (PDFs): `/domain/financialreport/attachment/{id}`
  — [RÚZ API docs](https://www.registeruz.sk/cruz-public/home/api) (accessed 2026-10-25)
- Incremental sync uses `zmenene-od` (required), `pokracovat-za-id` and `max-zaznamov` (default 1,000, max 10,000). `uctovne-jednotky` also filters by `ico`, `dic` and `pravna-forma`. Deleted records come back as `stav: ZMAZANÉ`. — [RÚZ API docs](https://www.registeruz.sk/cruz-public/home/api)
- Statements carry structured numeric tables (`obsah.tabulky`). Row labels come from the template endpoint. Some filings have only public PDF attachments ("Verejné prílohy") or nothing public ("Neverejné"). — [RÚZ API docs](https://www.registeruz.sk/cruz-public/home/api)
- **Licence: CC0.** Data is updated throughout the day, as soon as it appears on the web interface. No rate limits are documented. — [RÚZ API docs](https://www.registeruz.sk/cruz-public/home/api)
- In practice a company's data changes about once a year, after its financial statements are filed and processed. — [GitHub: SK-doplnenie-udajov-firmy](https://github.com/samuelszabo/SK-doplnenie-udajov-firmy)
- RÚZ rules changed from 1 Jun 2024 under Act 105/2024. — [podnikajte.sk](https://www.podnikajte.sk/uctovnictvo/register-uctovnych-zavierok-od-1-6-2024)
- An example of a fund-related filing found via RÚZ is an attachment linked from an SIH search. — [registeruz attachment 12037767](https://www.registeruz.sk/cruz-public/domain/financialreport/attachment/12037767) (content not verified)

**Slovak Investment Holding (SIH), Národný rozvojový fond II (NRF II / "NDF II") and public VC programmes**
- SIH is 100% owned by Slovenská záručná a rozvojová banka (SZRB). Its subsidiary Slovak Asset Management acts as fund manager. NDF II finances SMEs and infrastructure, directly and through financial intermediaries. — search summary of [SIH direct investment](https://www.sih.sk/en/stranky/investicie/priame) and [fi-compass SIH case study](https://www.fi-compass.eu/library/case-studies/slovak-investment-holding-multi-sector-financial-instruments-slovakia)
- **Start-up fund-manager tender, 10 Mar 2026:** SIH, as manager of NDF II, is selecting 3 fund managers, each with a €30m fund (€90m total from NDF II), for 2026–2030. The deadline was 30 Jun 2026 and the TED notice is 167128-2026. No outcome was published on the page when accessed. — [SIH news 2026](https://www.sih.sk/en/aktuality/sih-vyhlasuje-sutaz-na-vyber-spravcov-fondov-na-podporu-startupov-pre-roky-2026-2030); [TED notice](https://ted.europa.eu/sk/notice/-/detail/167128-2026)
- **Venture to Future Fund (VFF):**
  - Set up in 2019 with €40.4m, as an EIB + Slovak Ministry of Finance initiative through SIH.
  - In May 2024 it added €15.3m from the Recovery and Resilience Plan, which extended the investment period to end-2026.
  - Tickets are €400k–€7m (previously up to €4.9m), always invested pari passu with private co-investors.
  — [SIH press release May 2024](https://www.sih.sk/en/aktuality/venture-to-future-fund-increases-capital-by-eur-15-3-million-to-support-slovak-startups); [SIH VFF page](https://www.sih.sk/en/stranky/cinnosti/venture-to-future-fund)
- The EIB signed a €10m equity commitment to VFF on 20 Dec 2019. — [EIB project 20190166](https://www.eib.org/en/projects/all/20190166?lang=en) **[pre-2024]**
- SIH planned €15m for seed-stage companies from the RRP (June 2024). — [SIH news](https://www.sih.sk/en/aktuality/slovak-investment-holding-podpori-podniky-v-pociatocnej-etape-zivotneho-cyklu-v-celkovom-objeme-15-milionov-eur)
- SIH's pages on financial intermediaries show that legacy funds are no longer investing:
  - Vision Ventures: launched 2020, investment period ended Dec 2023, now divesting. — [SIH Vision Ventures](https://www.sih.sk/en/investicie/investicie-cez-financnych-sprostredkovatelov/vision-ventures-kapitalova-investicia)
  - Neulogy Ventures (Luxembourg fund): invested 2014–2016, now divesting. — [SIH Neulogy](https://www.sih.sk/en/investicie/investicie-cez-financnych-sprostredkovatelov/neulogy-ventures-kapitalova-investicia)
  - Limerock: invested 2014–2016, in liquidation. — [SIH Limerock](https://sih.sk/en/investicie/investicie-cez-financnych-sprostredkovatelov/limerock-fund-manager-kapitalova-investicia)
  - None of these pages state SIH's commitment amounts.
- Social-economy funds: SIH put €20.9m into two funds (€10.45m each), managed by CB ESPRI and Sociálni Inovátori Impact Capital. Contracts could be signed until end-2023. — [podnikajte.sk](https://www.podnikajte.sk/financie-na-podnikanie/investicny-fond-pre-socialnu-ekonomiku)

**EIF in Slovakia**
- In 2025 the EIF gave guarantees to Eximbanka, VÚB, UniCredit and ČSOB and channelled €8m from the RRF to Slovakia. The EIB Group summary for Slovakia names no new VC fund commitment. — [EIB press 2026-118](https://www.eib.org/en/press/all/2026-118-slovakia-financing-from-eib-group-jumps-60-to-eur649-million-in-2025-with-focus-on-energy-upgrades-and-urban-development)
- Historic EIF activity in Slovakia: a €100m JEREMIE holding fund (2009) and three JEREMIE VC/seed funds (2014). — [MF SR](https://www.mfsr.sk/en/press/european-investment-fund-signs-agreements-eur-100m-jeremie-holding-fund-support-businesses-slovakia.html); [EIF JEREMIE 2014](https://www.eif.org/what_we_do/resources/jeremie/news/2014/slovakia_vc.htm?lang=-en) **[pre-2024]**

**SLOVCA (Slovak Venture Capital and Private Equity Association)**
- Founded in 1995 in Bratislava. — [CB Insights](https://www.cbinsights.com/company/slovca/financials) (aggregator)
- IČO 31 748 341. — [CRZ contract](https://crz.gov.sk//data/att/1778762_dokument1.pdf) **[pre-2024]**
- **12 full members (accessed 2026-10-25):** ARX Equity Partners, CVI, Enterprise Investors, Eterus Capital, Fond inovácií a technológií, Genesis Capital, Jet Investment, Národný holdingový fond s.r.o., Neulogy Ventures, Sandberg Capital, Venture to Future Fund, Vision Ventures. Member profiles are on slovca.sk only; no external URLs are shown. — [SLOVCA riadni členovia](https://www.slovca.sk/sk/clenstvo/riadni-clenovia.html)
- **31 associate members.** Only 3 look like investors: Across Private Investments, G4 Investments and Slovak Investment Holding. The rest are law, audit, insurance and bank firms, plus 9 unclear names (BHM group, Danube Capital Advisors, HILLBRIDGES, Finhold, M3 Partners, Ments, PFCEU, Montward, Wezeo). — [SLOVCA pridružení členovia](https://www.slovca.sk/sk/clenstvo/pridruzeni-clenovia.html)
- The homepage links a "Štatistiky" download section, but no figures appear on the page. The latest news item is dated 3 Sep 2026. — [slovca.sk](https://www.slovca.sk/)
- CVCA and SLOVCA run joint awards, with registration open to members only (2025). — [AmCham Slovakia](https://amcham.sk/events/3462/cvcaslovca-awards-2025)

**Business angels (Slovakia)**
- Klub podnikateľských anjelov Slovenska was the first Slovak angel network, founded in 2011 by ZMPS and the Slovak Business Agency. — [podnikajte.sk podnikateľskí anjeli](https://www.podnikajte.sk/temy/podnikatelski-anjeli) **[pre-2024]**
- "Slovak Business Angels" were listed in 2020 with typical tickets of €10k–€80k. — [Vestbee, 8 Oct 2020](https://vestbee.com/insights/articles/top-vc-funds-in-slovakia-to-finance-your-startup) **[pre-2024]**
- EBAN's CEE Community (2016) includes Slovakia. That does not show a current Slovak EBAN member. — [EBAN 2016](https://www.eban.org/2016/10/22/) **[pre-2024]**

**News and ecosystem round-ups (Slovakia)**
- Startitup (13 Aug 2026), citing Invest Europe:
  - Slovak companies received about €7m of PE/VC in 2025, across 5 companies. That is 0.005% of GDP, the lowest in Europe.
  - About €5.8m went to established companies and about €1.2m to growth capital and start-ups.
  - The prior 5-year average was about €190m a year. Czechia received about €275m.
  — [Startitup](https://www.startitup.sk/slovensko-ziskalo-7-cesko-az-275-milionov-eur-nedokazeme-ziskat-zahranicny-kapital-v-europe-sme-uplne-posledni/)
- "Startup Report Slovensko 2025" (Slovenská sporiteľňa + Civitta) surveyed 600 firms and investors. 183 start-ups and 41 investors responded. It is in Slovak. — [pravnenoviny.sk](https://pravnenoviny.sk/slovenske-startupy-silneju-v-it-rast-brzdi-nedostatok-investicii/)
- The Recursive publishes Slovak round-ups, for example "Slovak Startup Ecosystem Biggest Funding Rounds (H1 2025)". That list includes:
  - Vestberry €2.2m seed, investors: Seed Starter ČS, Slovakia Venture to Future Fund, Zero One Hundred, CB Investment Management
  - Xatoms €2.62m seed (investors are mostly Canadian)
  — [The Recursive search results](https://therecursive.com/search/venture+capital/page/61) (full article not opened; country page returned 404)
- A 2020 Vestbee list of Slovak VC funds (with websites, tickets and portfolios) is summarised in Section 5. — [Vestbee, 8 Oct 2020](https://vestbee.com/insights/articles/top-vc-funds-in-slovakia-to-finance-your-startup) **[pre-2024]**

### Inferences
- The NBS "Registrované subjekty" count (39) is probably close to the number of sub-threshold AIF managers in the collective-investment sector. That would be the closest Slovak equivalent of the Czech §15 list, and it is small enough to review by hand. This is not verified: the count may include other registered entity types.
- RÚZ is the strongest public lever for "total investable capital / AuM" in Slovakia. Fund vehicles (a.s., SICAV, s.r.o. general partners) file balance sheets, and their financial-investment lines and equity can proxy fund size. The data is CC0, incremental and JSON, so a re-runnable fetch script is easy. Expect the latest available year to be 12–18 months behind.
- SK NACE codes as a filter: the RÚZ `/api/sk-nace` classifier and the RPO statistical codes let you filter by 64.30 / 64.99 / 66.30. These codes are likely to be very noisy:
  - 64.99 and holding-type codes are used by many SPVs, family holdings and real-estate vehicles.
  - Many real VC managers are registered as s.r.o. under 70.22 (consulting) or 66.30.
  - Use NACE only as a recall booster, combined with the NBS lists, SLOVCA and the SIH intermediary lists.
  - *[From general knowledge, unverified here]* NACE Rev. 2.1 (in force from 2025) splits 64.30 into finer codes. Expect dual coding during the transition.
- The SIH 2026–2030 tender will produce 3 new Slovak VC managers with €30m public money each. Once awarded (TED award notice), they become high-quality "active" records.

### Gaps
- No direct count of Slovak entities under SK NACE 64.30 / 64.99 / 66.30 was obtained, so noise cannot be quantified. A suggested test: pull RÚZ accounting units, filter by SK NACE, and hand-check a sample of about 100.
- I did not verify whether NBS publishes AIF or EuVECA lists separately, or whether "Databáza na stiahnutie" offers a bulk file.
- ORSR (orsr.sk) was not examined in this pass; it is known to be HTML-only, but that is not verified here.
- SBA / Startup Slovakia investor databases, the SBAN member list, and Forbes Slovensko, Trend and Index SME round-ups were not retrieved.
- A June 2026 report says SIH group AuM reached €1,593m at end-2025, but I could not identify which document. **[unverified]**
- The outcome of the SIH 2026 tender (awarded managers) was not published on the SIH page as of the fetch.

---

## 2. Czechia: regulatory, registry, public-programme, association and news sources

### Takeaway
Czechia has better bulk data than Slovakia:
- ARES REST API
- ČSÚ RES open-data CSV snapshots twice a month, with CZ-NACE
- justice.cz open-data CSV/XML exports
- ČNB JERRS, covering all funds, AIFMs and §15 sub-threshold managers, with point-in-time lists and counts. Machine access to JERRS (WS JERRS) needs a commercial certificate and registration.

Public VC programmes (EIF, MPO / Národní plán obnovy via EIF, NRB/NRI, the regional JIC) give dated, citable fund-commitment evidence. CVCA's member list could not be retrieved (TLS certificate error).

### Cited Findings

**ČNB – JERRS (lists of regulated and registered entities)**
- JERRS presents all ČNB lists in one place. Menus:
  - "Přímé vyhledání" (direct search)
  - "Základní seznamy" (basic lists)
  - "Počty subjektů" (counts as at a date, plus time series)
  - "Vznik a zánik subjektů" (entity creation and termination)
  - Status dates can go back to 1 Jan 2009.
  - The last data publication was 24.10.2026 01:45:50.
  - Contact details are updated quarterly for banks and insurers; other entities update them only when they notify the ČNB.
  — [JERRS intro](https://jerrs.cnb.cz//apljerrsdad/JERRS.WEB07.INTRO_PAGE?p_lang=cz) (accessed 2026-10-25)
- The §15 ZISIF list is under "Základní seznamy". It is the last item: "Osoby uvedené v § 15 odst. 1 ZISIF, kterým vznikla povinnost nechat se zapsat do seznamu". Each entity has a "vizitka" (information card). — [ČNB FOI response 26 May 2025](https://www.cnb.cz/cs/o_cnb/106/informace-poskytnute-ceskou-narodni-bankou-podle-zakona-c.-106-1999-sb.-o-svobodnem-pristupu-k-informacim/Informace-poskytnute-na-zadost-ze-dne-21.-5.-2025-tykajici-se-subjektu-registrovanych-dle-15-ZISIF)
- §15 managers under Act 240/2013 are not supervised. Registration is a notification, not a licence. They file an annual asset report only to confirm they stay under the €100m ceiling (including leverage). ČNB warns that a listing is not an endorsement. — [ČNB: Role ČNB u správců podle §15](https://www.cnb.cz/cs/dohled-financni-trh/vykon-dohledu/upozorneni-pro-verejnost/Role-CNB-u-spravcu-podle-15-zakona-o-investicnich-spolecnostech-a-investicnich-fondech); [ČNB warning on §15 offers](https://www.cnb.cz/cs/dohled-financni-trh/vykon-dohledu/upozorneni-pro-verejnost/Upozorneni-Ceske-narodni-banky-na-rizika-nabizeni-investicnich-prilezitosti-osob-podle-15-ZISIF)
- **WS JERRS** (since 1 Jul 2019):
  - endpoint `https://aplc.cnb.cz/jerrsws/ws`, with WSDL and XSD (SOAP-style XML)
  - operations: `getSubjekt`, `getSubjekty` (all entities in a role, paginated) and `getZastoupeny`
  - needs a commercial (non-qualified) certificate from eIdentity, I.CA, PostSignum or an EU-trusted issuer, plus a signed request to jerrsws@cnb.cz
  - an "Otevřená data" section exists, but its contents were not described
  — [ČNB WS JERRS](https://www.cnb.cz/cs/dohled-financni-trh/seznamy/webove-sluzby-ws-jerrs/)

**ARES (Ministry of Finance)**
- ARES is the MF aggregator of Czech economic-subject registers. The official developer documentation is the "Katalog veřejných služeb" PDF (v06–v08, dated 2023-08-01). — [MF ARES](https://mf.gov.cz/cs/ministerstvo/informacni-systemy/ares); [ARES Katalog v08](https://mf.gov.cz/assets/attachments/2023-08-01_ARES-Technicka-dokumentace-Katalog-verejnych-sluzeb_v08.pdf)
- REST search endpoint (POST): `https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/vyhledat`. Lookup: `/ekonomicke-subjekty/{ico}`. — [Apify ARES actor](https://apify.com/osmateus/czech-ares-company-api); [ARES MCP client](https://glama.ai/mcp/servers/@vzeman/ares-mcp-server/blob/f3074b5f9ee3fba6205cc424ce8b8839c88d4d9c/ares_mcp_server/api_client.py) (third-party; confirm against the Katalog)

**ČSÚ Registr ekonomických subjektů (RES) – open data with CZ-NACE**
- The full RES snapshot is published as open data twice a month (as at the 15th and month-end). Files are `res_data.csv` (subjects) and `res_pf_nace.csv` (legal forms and NACE activities), UTF-8 CSV with JSON metadata schemas. — [ČSÚ RES open data documentation](https://csu.gov.cz/registr-ekonomickych-subjektu-otevrena-data-dokumentace)
- CZ-NACE 2025 (the Czech version of NACE Rev. 2.1) exports start on 1 Jan 2026. Dual coding runs until 31 Dec 2028. — [ČSÚ RES open data documentation](https://csu.gov.cz/registr-ekonomickych-subjektu-otevrena-data-dokumentace)

**Veřejný rejstřík (justice.cz) open data**
- Public-register data is exportable as CSV and XML on dataor.justice.cz, with a user guide. — [Advokátní deník, 26 Mar 2019](https://advokatnidenik.cz/2019/03/26/otevrena-data-verejnych-rejstriku-budou-jiz-brzy-v-plnem-provozu/) **[pre-2024]**
- A third party says the files are free, CSV/XML, with the current year updated daily. The same source says the beneficial-owner register has been closed to the public since 17 Dec 2025. — [companydata.com](https://companydata.com/company-register/czech-republic/) **[unverified, single non-official source]**
- The files are very large; streaming XML parsing is recommended. — [Lupa.cz](https://www.lupa.cz/clanky/ares-jako-otevrena-data-ministerstvo-financi-slo-cestou-nejmensiho-odporu/)

**Národní rozvojová banka (NRB) / Národní rozvojová investiční (NRI) / Národní rozvojový fond**
- NRI is 100% owned by NRB and is NRB's equity / fund-of-funds arm. — [BusinessInfo ČMZRB/NRB](https://www.businessinfo.cz/informace/ceskomoravska-zarucni-a-rozvojova-banka/)
- NRI "Fond Ukrajina": NRI selected DEPO Ventures One SCSp (managed by DEPO Ventures Sàrl, Luxembourg) and committed CZK 94m, up to CZK 141m if private money is raised. The programme targets start-ups from Ukraine, Moldova and Georgia. — [BusinessInfo](https://www.businessinfo.cz/clanky/nri-dokoncila-vyber-venture-kapitaloveho-fondu-pro-program-fond-ukrajina/) (article date not captured)
- The separate Czech "Národní rozvojový fond" focuses on infrastructure (2019), not VC. — [BusinessInfo](https://www.businessinfo.cz/clanky/narodni-rozvojovy-fond-prichazi-podpori-projekty-v-infrastrukture/) **[pre-2024]**

**EIF and MPO / Národní plán obnovy (NPO) programmes**
- As of 15 May 2024, the EIF had committed €334m to 17 Czech VC/PE funds since 2002 (the first was Genesis in 2002).
  - Named funds: Genesis Capital, Kaya, Credo, N1, Espira Investments.
  - EIF money also helped create Lighthouse Ventures, i&i Biotech, Arx and Tilia Impact Ventures.
  — [CzechCrunch, 15 May 2024](https://cc.cz/evropsky-investicni-fond-uz-vlozil-penize-do-17-ceskych-fondu-miliardovy-ted-otevira-s-tensor-ventures/)
- Tensor Ventures Co-investment Fund: target up to €50m, of which up to €20m comes from the NPO via the EIF RRF fund of funds (MPO is responsible). It invests in pre-seed digital start-ups, about 50 over 5 years, always co-investing with other VCs. — [CzechCrunch](https://cc.cz/evropsky-investicni-fond-uz-vlozil-penize-do-17-ceskych-fondu-miliardovy-ted-otevira-s-tensor-ventures/); [BusinessInfo](https://www.businessinfo.cz/clanky/prvni-investicni-vc-fond-z-narodniho-planu-obnovy-cr-bude-spravovat-tensor-ventures/)
- MPO planned 3 pilot NPO start-up funds with the EIF, about CZK 1.3bn. Other articles cite CZK 3.3bn; the figures conflict. — [Forbes CZ](https://forbes.cz/ministerstvo-rozdeli-13-miliardy-start-upum-podpori-rozvoj-strategickych-technologii/); [Lupa.cz](https://www.lupa.cz/aktuality/stat-zacal-ceskym-startupum-rozdelovat-evropske-miliardy-z-narodniho-planu-obnovy/)
- JIC Ventures (Brno) launched in April 2026 with CZK 400m, backed by JIC, the South Moravian Region, the city of Brno and 4 universities. Tickets go up to €1m, for about 20 companies over 4 years. — [Lupa.cz](https://www.lupa.cz/aktuality/v-brne-vznikl-fond-pro-startupy-ktery-bude-investovat-i-penize-kraje/)

**CzechInvest**
- czechstartups.gov.cz runs a "Find your investor" directory. Search snippets show it listing CVCA, Reflex Capital, Credo Ventures and Inven Capital. The page refused the connection when fetched, so its fields and count are unknown. — [CzechInvest investors](https://czechstartups.gov.cz/en/startup-ecosystem/investors)
- CEE Funding Map (26 May 2026): an interactive map of active CEE investors by Warsaw Equity Group with CzechInvest and Czech Founders. It cites Dealroom: Czech start-ups raised more than €213m in 86 rounds in 2025 (€11.2m pre-seed; more than €110m Series B/C). — [EEN/CzechInvest](https://een.gov.cz/en/news/cee-funding-map-provides-an-overview-of-active-investors-in-central-and-eastern-europe/); [map](https://www.pampam.city/funds-poland-BJpHbykKoXoBaILayYBs?52.231418%2C20.931213%2C11.26=)

**CVCA (Czech Private Equity and Venture Capital Association)**
- Founded in 1997; a member of Invest Europe. — [Wikipedia: VC in the Czech Republic](https://en.wikipedia.org/wiki/Venture_capital_in_the_Czech_Republic)
- cvca.cz returned "unable to verify the first certificate" (TLS error) on 2026-10-25, so the member list was **not retrieved**. — fetch attempt on https://www.cvca.cz/
- Caution: "CVCA" also stands for the Croatian association (cvca.hr). Its pages (e.g. 23 regular members in 2025) must not be mixed up with the Czech CVCA. — [cvca.hr AGM 2025](https://cvca.hr/annual-general-assembly-meeting-2025/)

**Business angels (Czechia)**
- The Czech Business Angel Association (CBAA) is chaired by Karel Obluk. Founding backers include Jiří Hlavenka, Petr Skrla, Keiretsu, Garage Ventures and Fazole Ventures. — [Forbes CZ](https://forbes.cz/cesko-se-musi-vymanit-ze-statusu-montovny-pomoci-ma-asociace-andelskych-investoru/) (date not captured)
- CBAA runs a free angel-investing course with ESIL and LUMUS Investment, and works on legislation with Czech Founders and the Česká startupová asociace. — [BusinessInfo](https://www.businessinfo.cz/clanky/vice-andelskych-investoru-a-investorek-akademie-nauci-jak-investovat-do-startupu/); [BusinessInfo](https://www.businessinfo.cz/clanky/jak-zlepsovat-legislativu-pro-startupy-startupove-asociace-spojuji-sily/)
- A World Bank study (2018) found Czech angel investing small, concentrated in Prague and ICT, with little syndication. — [World Bank blog](https://blogs.worldbank.org/en/psd/how-can-czech-republic-activate-its-business-angels-market); [MF CZ](https://www.mfcr.cz/en/themes/capital-market/capital-market-in-the-czech-republic/the-ministry-of-finance-publishes-a-worl-33724) **[pre-2024]**

**News and annual round-ups (Czechia)**
- CzechCrunch (2 Jan 2026), on 2025:
  - 75 announced rounds by Czech founders, the lowest in 6 years
  - CZK 9.8bn total, down nearly a third
  - median round CZK 29m, the highest in 6 years
  - 12 exits
  — [CzechCrunch](https://cc.cz/zmapovali-jsme-vsechny-investice-ktere-loni-oznamily-ceske-startupy-neseme-tri-dobre-a-tri-spatne-zpravy/)
- CzechCrunch "Startupové Česko 2025":
  - headline CZK 13,331,223,064 (−19.78% year on year)
  - medians: pre-seed about CZK 13m, seed about CZK 73m, Series A+ about CZK 445m
  - the most-active-funds chart and the "100+ investors" database sit behind the CC+ paywall
  — [CzechCrunch Startupové Česko](https://cc.cz/startupovecesko/) **[paywall for investor names]**
- The Ambit "VC Deals Report 2025" counts about 100 Czech VC deals in 2025, against up to 200 a year in 2021–22. Median early-stage ticket €500k, median pre-money €6.5m, more than 80% early stage. — [BusinessInfo](https://www.businessinfo.cz/clanky/investice-do-ceskych-startupu-mene-dealu-vetsi-investice-prisnejsi-investori/) (page returned 403; figures from search snippet)
- Smart Market Report: investment in Czech start-ups rose 174% to CZK 14.3bn in 2024. Methodologies differ across sources. — [Forbes CZ](https://forbes.cz/investice-do-ceskych-startupu-vzrostly-o-174-procent-mews-a-rohlik-vedou-rekordy/)

### Inferences
- In Czechia, the §15 ZISIF list is the main noise source for a "registered managers" seed. Many §15 entities are real-estate or club-deal vehicles. Use it as a candidate pool, then confirm against deal evidence (news, EIF/NRI/MPO commitments).
- For bulk, re-runnable ingestion: ČSÚ RES CSV (NACE filter, twice a month) plus justice.cz open data (officers, shareholders, daily) plus ARES REST (lookup by IČO). JERRS is easiest to scrape as HTML "Základní seznamy" by date. WS JERRS is possible once a certificate is registered.
- Czech financial statements sit in the Sbírka listin as scanned or PDF documents, not as a structured CC0 API like RÚZ. *[not verified in this pass]* That means AuM extraction is costlier in Czechia than in Slovakia.

### Gaps
- No count of §15 managers, licensed AIFMs (investiční společnosti / samosprávné fondy), FKI or EuVECA managers was retrieved from JERRS. A third-party snippet said qualified-investor funds (FKI) rose from 516 (end-2024) to 585 (end-2025), but the source page was not identified. **[unverified]**
- The CVCA member list could not be retrieved because of the TLS error.
- The licence terms of ČSÚ RES, justice.cz open data and ARES were not confirmed.
- The claim that the Czech BO register closed on 17 Dec 2025 is unverified.
- Hospodářské noviny and Forbes CZ annual round-ups were not retrieved (Forbes "Investoři při chuti…" returned only its headline).

---

## 3. Ecosystem reports and CEE-level data (Invest Europe, Dealroom, Vestbee, others)

### Takeaway
Invest Europe's annual CEE Private Equity Statistics are free PDFs with CZ and SK country tables (EDC data, "market approach"). They show Czechia far ahead of Slovakia:
- 30 vs 8 country-based funds raising capital in 2011–2025
- 2025 investment of about €275m vs about €7m

EDC, however, badly under-counts VC deals in both countries compared with Dealroom. Use these figures as an order-of-magnitude, cross-country benchmark, not as a deal census.

### Cited Findings

**Invest Europe – "2024 Central and Eastern Europe Private Equity Statistics" (published 19 Jun 2025)**
- CEE has 17 countries; the data uses the "market approach" (by country of the portfolio company) and is collected on the EDC platform. — [Invest Europe CEE 2024 PDF](https://www.investeurope.eu/media/wvrnw0lr/20250619_invest-europe_cee-report-2024.pdf) (read via [mirror on cvca.hr](https://cvca.hr/wp-content/uploads/2025/12/Invest-Europe_CEE-Statistics_2024.pdf)); [publication page](https://www.investeurope.eu/publications-policy/publications/2025/2024-central-and-eastern-europe-private-equity-statistics/)
- 2024: Czechia took 14% of CEE investment value. CZ buyout and growth was €373m in 9 companies. CZ exits were €52m. — same PDF
- PE investment as % of GDP in 2024: Czechia 0.124%, Slovakia 0.027%, CEE 0.112%, Europe 0.551%. — same PDF
- Table 6, 2024 (€ thousands):
  - CZ: total venture 20,948 (seed 7,227; start-up 6,198; later stage 7,523); growth 112,182; total about 394,313
  - SK: total venture 26,761 (seed 600; start-up 4,420; later stage 21,741); growth 7,625; buyout 690; total 35,076
  - 2023: CZ total 536,976 (venture 60,333); SK total 45,840 (venture 16,325)
  - The PDF layout is garbled; venture subtotals were cross-checked as sums.
  — same PDF
- CEE fundraising 2024: €1.42bn, of which VC funds €657m. 13 funds reached final close, raising €1.83bn in total. — same PDF
- Family offices and private individuals were 21% of CEE fundraising in 2024. Within CEE-located LPs, 34% came from private individuals and family offices. — same PDF
- Appendix 2010–2024:
  - CZ: fundraising €1,370.2m by **25 funds**; investments €4,832.4m in 228 companies; divestments €3,416.6m in 112 companies
  - SK: fundraising €252.8m by **8 funds**; investments €432.0m in 184 companies; divestments €256.1m in 47 companies
  — same PDF

**Invest Europe – "2025 CEE Private Equity Statistics" (published 23 Jun 2026)**
- CEE 2025:
  - VC €675m, almost double
  - fundraising €1.87bn (−3%; buyout funds €1bn, the highest since 2018; VC funds €548m)
  - exits €1.71bn (+26%)
  - 24 mid-market buyouts (a record)
  — [Invest Europe press release](https://www.investeurope.eu/news/newsroom/central-and-eastern-european-exits-reach-17bn-in-2025-as-trade-sales-drive-second-best-year-on-record/); [CEE 2025 PDF](https://www.investeurope.eu/media/z3pasguu/20260623_invest-europe_cee-report-2025.pdf)
- 15 CEE funds reached final close in 2025, raising €1.81bn in total. — [CEE 2025 PDF](https://www.investeurope.eu/media/z3pasguu/20260623_invest-europe_cee-report-2025.pdf)
- Czechia 2025:
  - 11% of CEE investment value; total about €275.3m (Table 6)
  - VC €34m in 14 companies
  - buyout and growth €241m in 12 companies
  - exits €98m
  — [CEE 2025 PDF](https://www.investeurope.eu/media/z3pasguu/20260623_invest-europe_cee-report-2025.pdf)
- PE as % of GDP in 2025: Czechia 0.080%, Slovakia 0.005% (the lowest), CEE 0.091%. Slovakia: about €7m in 5 companies. — [CEE 2025 PDF](https://www.investeurope.eu/media/z3pasguu/20260623_invest-europe_cee-report-2025.pdf); [Startitup, 13 Aug 2026](https://www.startitup.sk/slovensko-ziskalo-7-cesko-az-275-milionov-eur-nedokazeme-ziskat-zahranicny-kapital-v-europe-sme-uplne-posledni/)
- Appendix 2011–2025:
  - CZ: fundraising €1,958.2m by **30 funds**; investments €4,792.7m in 236 companies; divestments €3,393.1m in 108 companies
  - SK: fundraising €252.8m by **8 funds**; investments €433.1m in 176 companies
  — [CEE 2025 PDF](https://www.investeurope.eu/media/z3pasguu/20260623_invest-europe_cee-report-2025.pdf)
- Poland: €994m, 39% of CEE value; record VC of €310m in 57 companies. — [CEE 2025 PDF](https://www.investeurope.eu/media/z3pasguu/20260623_invest-europe_cee-report-2025.pdf); [xyz.pl](https://xyz.pl/dzieje-sie/raport-fundusze-pe-i-vc-zainwestowaly-w-polskie-spolki-blisko-1-mld-euro-w-2025-r-2002)
- Wider CEE in 2025, for cheap context:
  - VC: Estonia €141m (34 companies), Lithuania €55m (21), Hungary €31m (7)
  - Total investment value: Romania 17%, Estonia 12%
  — [CEE 2025 PDF](https://www.investeurope.eu/media/z3pasguu/20260623_invest-europe_cee-report-2025.pdf)
- The general research hub (free PDFs) is the [Invest Europe activity data page](https://www.investeurope.eu/research/activity-data/).

**Dealroom, Vestbee and other trackers**
- Dealroom's public Slovakia page shows $336.3M of VC in the last 12 months, 200 tracked start-ups and $4.8B+ combined enterprise value. Deal-level data and investor lists are paywalled. — [Dealroom Slovakia](https://dealroom.co/countries/slovakia/) (snapshot date not shown) **[paywall beyond headline]**
- Dealroom (via CzechInvest): Czech start-ups raised more than €213m in 86 rounds in 2025. — [EEN/CzechInvest, 26 May 2026](https://een.gov.cz/en/news/cee-funding-map-provides-an-overview-of-active-investors-in-central-and-eastern-europe/)
- Vestbee quarterly CEE reports (free):
  - Q2 2026: about €495m across 143 rounds
  - Q1 2026: €821m across 138 rounds, inflated by Mews and Preply (€385m combined)
  — [Vestbee Q2 2026](https://vestbee.com/insights/articles/vc-funding-in-cee-report-q2-2026)
- Vestbee Q3 2025 most active CEE funds: Inovo VC, FIRSTPICK, Startup Wise Guys, Coinvest Capital, Kaya VC, Purple Ventures. — [CzechInvest repost of Vestbee Q3](https://czechstartups.gov.cz/en/novinky/vestbee-cee-venture-capital-reaches-e510m-across-148-deals-in-q3-driven-by-a-few-standout-rounds)
- Vestbee also publishes quarterly "new VC funds" lists. These are useful dated fund-close evidence: [Q1 2025](https://vestbee.com/insights/articles/list-of-new-vc-funds-launched-in-q1-2025-to-invest-in-europe), [Q2 2025](https://vestbee.com/insights/articles/list-of-new-vc-funds-launched-in-q2-2025-to-invest-in-europe), [Q3 2025](https://www.vestbee.com/insights/articles/new-vc-funds-q3-2025-to-invest-in-europe), [Q1 2026 (31 Mar 2026)](https://vestbee.com/insights/articles/new-vc-funds-launched-in-q1-2026-to-invest-in-europe)
- Commentary on the Invest Europe CEE data: [0100 Conferences Substack](https://0100conferences.substack.com/p/cee-private-markets-2025-the-mid)

### Inferences
- **EDC coverage is unreliable for VC in Czechia and Slovakia.**
  - 2024: EDC shows CZ VC at €20.9m, against about CZK 14–16bn of Czech-founder rounds reported by CzechCrunch and Smart Market.
  - 2025: EDC shows SK VC at about €1.2m, against Dealroom's $336m over 12 months for Slovakia.
  - The gaps come from the market approach (company HQ), EDC survey coverage, and diaspora start-ups headquartered abroad.
  - Use Invest Europe for cross-country ratios and fund counts, not for a deal census.
- The Invest Europe "number of funds" in fundraising (CZ 30, SK 8 over 2011–2025) is the cleanest public, comparable proxy for how many locally based PE/VC fund vehicles exist. It suggests a CZ:SK ratio of roughly 4:1.

### Gaps
- No free Dealroom-based country ecosystem report specifically for CZ or SK was found for 2025/2026; only headline numbers.
- Startup Slovakia / SBA ecosystem databases were not retrieved.
- Invest Europe's "Private Equity at Work 2026" (cited by Startitup) was not opened.
- A snippet said Czech-founded start-ups raised about €540m in 2025 across 79 deals (Cera €146m, Mews €64m, Exaforce €64m), but the source page was not opened. **[unverified]**

---

## 4. Source catalogue: fields, coverage, access method, licence, language, cadence, reliability

### Takeaway
For re-runnable PostgreSQL loaders, use the sources in this order:
- **Slovakia:** RÚZ API (JSON, CC0), then RPO API, then RPVS (structured / BODS).
- **Czechia:** ČSÚ RES CSV, then justice.cz open data, then ARES REST.
- **Investor-type seeds:** regulator lists, which are HTML (NBS, JERRS) or certificate-gated SOAP (WS JERRS).
- **"Active investor" evidence:** news, Vestbee/Recursive round-ups, EIF/SIH/NRI/MPO press releases.

### Cited Findings

| Source | Country | What it gives (fields) | Coverage | Access method | Licence | Lang | Cadence | Reliability / issues | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| NBS Subjekty finančného trhu (collective investment) | SK | Management companies, registered sub-threshold managers, SK and foreign funds; per-entity cards | 368 mgmt cos (incl. foreign), 39 registered, 92 SK funds, 1,049 foreign funds (2026-10-25) | HTML search/browse; no export visible | Not stated | SK/EN | Live | Registered managers not supervised in depth; new removal power from 1 Jun 2026 | [subjekty.nbs.sk](https://subjekty.nbs.sk/?s=1059); [NBS](https://nbs.sk/en/financial-market-supervision1/supervision/collective-investment/registered-managers/) |
| RPO | SK | Name, legal form, status, address, share capital, activities, statutory bodies, shareholders, stat codes | All legal persons (>1.4m, per third party) | Free public API, no auth | CC-BY 4.0 (per third party) | SK | Live | Public version once described as non-binding **[pre-2024]** | [Topograph](https://docs.topograph.co/essentials/slovakia); [mcp.so](https://mcp.so/ja/servers/sk-registers-mcp) |
| RPVS | SK | Public-sector partners, beneficial owners (natural persons), oprávnená osoba | Only firms contracting with the public sector | Structured open data (MoJ); BODS republish | ODC-By (Open Ownership copy) | SK | Live | Covers only public-sector partners; BODS mapping "in development" | [justice.gov.sk](https://www.justice.gov.sk/sluzby/register-partnerov-verejneho-sektora/); [BODS](https://bods-data.openownership.org/source/slovakia) |
| RÚZ Open API | SK | Accounting units (IČO, legal form, SK NACE), statements, structured line items, annual reports, PDFs | All filers | REST JSON, incremental (`zmenene-od`) | **CC0** | SK | Intraday; per company about yearly | Some filings PDF-only or non-public | [RÚZ API](https://www.registeruz.sk/cruz-public/home/api) |
| SIH / NDF II / VFF | SK | Programme sizes, managers, ticket ranges, tenders | Public VC money in SK | HTML press releases; TED notices | Not stated | SK/EN | Ad hoc | Intermediary pages omit amounts | [SIH 2026 call](https://www.sih.sk/en/aktuality/sih-vyhlasuje-sutaz-na-vyber-spravcov-fondov-na-podporu-startupov-pre-roky-2026-2030) |
| SLOVCA members | SK | Member names (12 full, 31 associate) | Self-selected | HTML | Not stated | SK | Ad hoc | Mixes PE, VC and public bodies; associates mostly service firms | [SLOVCA](https://www.slovca.sk/sk/clenstvo/riadni-clenovia.html) |
| ČNB JERRS | CZ | All regulated/registered entities incl. funds, managers, §15 list; counts and time series; as-at-date lists | Full regulated universe since 2009 | HTML; WS JERRS (SOAP/XML) with certificate | ČNB site terms | CZ/EN | Daily publish | §15 entries not supervised (notification only) | [JERRS](https://jerrs.cnb.cz//apljerrsdad/JERRS.WEB07.INTRO_PAGE?p_lang=cz); [WS JERRS](https://www.cnb.cz/cs/dohled-financni-trh/seznamy/webove-sluzby-ws-jerrs/) |
| ARES | CZ | Economic-subject data aggregated from registers | All subjects | REST JSON (POST search, GET by IČO) | Not confirmed | CZ | Live | Aggregator; use Katalog PDF for schema | [MF ARES Katalog](https://mf.gov.cz/assets/attachments/2023-08-01_ARES-Technicka-dokumentace-Katalog-verejnych-sluzeb_v08.pdf) |
| ČSÚ RES open data | CZ | IČO, name, address, legal form, CZ-NACE, dates of creation and dissolution | All economic subjects | Bulk CSV (UTF-8) + JSON schema | Not confirmed | CZ | Twice a month | NACE dual-coding until 2028 | [ČSÚ](https://csu.gov.cz/registr-ekonomickych-subjektu-otevrena-data-dokumentace) |
| justice.cz open data (dataor) | CZ | Public-register extracts (officers, shareholders, etc.) | All registered entities | Bulk CSV/XML | Not confirmed | CZ | Daily for the current year (third party) | Huge files; BO register status unclear | [Advokátní deník](https://advokatnidenik.cz/2019/03/26/otevrena-data-verejnych-rejstriku-budou-jiz-brzy-v-plnem-provozu/); [companydata](https://companydata.com/company-register/czech-republic/) |
| EIF / MPO-NPO / NRI | CZ | Fund commitments, managers, sizes | Public LP money | HTML press releases | Not stated | CZ/EN | Ad hoc | Lists incomplete (17 funds not all named) | [CzechCrunch](https://cc.cz/evropsky-investicni-fond-uz-vlozil-penize-do-17-ceskych-fondu-miliardovy-ted-otevira-s-tensor-ventures/) |
| CzechInvest investors directory | CZ | Investor profiles | Unknown | HTML | Not stated | EN/CZ | Unknown | Connection refused at fetch | [czechstartups.gov.cz](https://czechstartups.gov.cz/en/startup-ecosystem/investors) |
| Invest Europe CEE stats | CEE | Fundraising, investment and exits by country and stage; fund counts | EDC-covered funds | Free PDF | Invest Europe copyright | EN | Annual (June) | Under-counts VC; market approach | [CEE 2025](https://www.investeurope.eu/media/z3pasguu/20260623_invest-europe_cee-report-2025.pdf) |
| CzechCrunch Startupové Česko / CC+ | CZ | Rounds, medians; investor DB (100+) | Announced rounds | HTML; CC+ paywall | Proprietary | CZ | Annual + ongoing | Investor rankings paywalled | [cc.cz](https://cc.cz/startupovecesko/) |
| Vestbee reports and fund lists | CEE | Quarterly rounds, most-active funds, new fund closes | CEE | HTML (free) | Proprietary | EN | Quarterly | Editorial selection | [Vestbee Q2 2026](https://vestbee.com/insights/articles/vc-funding-in-cee-report-q2-2026) |
| Dealroom country pages | SK/CZ | Headline VC totals, start-up counts | Dealroom-tracked | HTML; rest paywalled | Proprietary | EN | Rolling | Commercial; only headlines free | [Dealroom SK](https://dealroom.co/countries/slovakia/) |
| PitchBook profiles | SK/CZ | Latest-deal headline | — | HTML; paywalled | Proprietary | EN | Rolling | Only teaser visible | [PitchBook VFF](https://pitchbook.com/profiles/investor/461930-23) |

### Inferences
- For the database's required fields:
  - **Investor type and existence:** regulators (NBS, JERRS) and associations (SLOVCA, CVCA).
  - **Proof of activity with a date:** news, Vestbee/Recursive, SIH/EIF/NRI press releases.
  - **Ticket size and stage:** fund press releases and programme terms (e.g. VFF €400k–€7m).
  - **AuM / investable capital:** fund-close announcements; in Slovakia, RÚZ balance sheets.

### Gaps
- Licence terms for ARES, ČSÚ RES, justice.cz open data and NBS were not confirmed.
- Rate limits for RPO, ARES and RÚZ were not documented in what was read.

---

## 5. Preliminary list of VC investors active in Slovakia and Czechia (sourced only)

### Takeaway
I found about 15 named investors with a Slovak base or strong Slovak presence, but only about 5–6 have clearly dated 2024–2026 investment or fund evidence. I found about 25 Czech-based VC/growth investors, about 12 of them with dated 2024–2026 fund-close or deal evidence. The Slovak list is probably 60–70% complete for locally based VC managers. The Czech list is probably 40–50% complete; CVCA members and CzechCrunch's paywalled list of more than 100 investors were not available.

### Cited Findings

**Slovakia**

| # | Investor | Type | Website (as shown in source) | Evidence of activity (date) | Fund size / ticket (as stated) | Source |
|---|---|---|---|---|---|---|
| 1 | Venture to Future Fund (VFF) | Public-private VC (SIH/EIB) | not captured | Sloneek investment 16 Jun 2026 (PitchBook teaser); Vestberry €2.2m seed (H1 2025) | €40.4m (2019) + €15.3m (May 2024); tickets €400k–€7m; invests until end-2026 | [SIH](https://www.sih.sk/en/aktuality/venture-to-future-fund-increases-capital-by-eur-15-3-million-to-support-slovak-startups); [PitchBook](https://pitchbook.com/profiles/investor/461930-23) **[paywall]**; [Recursive](https://therecursive.com/search/venture+capital/page/61) |
| 2 | Vision Ventures | VC (seed) | visionventures.vc | Existing investor in Sloneek's €3.6m round (2026; report conflicts on round lead); SIH-backed fund divesting since Dec 2023 | €11m AuM (2020); €100k–€800k | [Silicon Canals](https://siliconcanals.com/business/hr-tech/page/2/); [SIH](https://www.sih.sk/en/investicie/investicie-cez-financnych-sprostredkovatelov/vision-ventures-kapitalova-investicia); [Vestbee 2020](https://vestbee.com/insights/articles/top-vc-funds-in-slovakia-to-finance-your-startup) |
| 3 | Zero Gravity Capital / 0100 Ventures ("Zero One Hundred") | VC (pre-seed–A) | zerogravitycap.com | Vestberry seed (H1 2025) | Initial tickets up to €200k (directory) | [Recursive](https://therecursive.com/search/venture+capital/page/61); [privateequitylist](https://privateequitylist.com/investors/zero-gravity-capital) |
| 4 | CB Investment Management (Crowdberry) | VC / platform | crowdberryim.sk | Vestberry seed (H1 2025) | Up to €1.6m (2020); platform €100k–€5m | [Recursive](https://therecursive.com/search/venture+capital/page/61); [Vestbee 2020](https://vestbee.com/insights/articles/top-vc-funds-in-slovakia-to-finance-your-startup) |
| 5 | Neulogy Ventures | VC (pre-seed/seed) | neulogy.vc | SLOVCA full member (2026); SIH fund divesting; no dated 2024–26 deal found | >€23m invested (2020); AuM $36M (directory, updated Aug 2026); €200k–€1m | [SLOVCA](https://www.slovca.sk/sk/clenstvo/riadni-clenovia.html); [privateequitylist](https://privateequitylist.com/public/investor/neulogy-ventures) **[unverified AuM]** |
| 6 | Fond inovácií a technológií (FIT) | Public VC | fondfit.sk | SLOVCA full member; no dated recent deal found | €20k–€1.5m (2020) | [SLOVCA](https://www.slovca.sk/sk/clenstvo/riadni-clenovia.html); [Vestbee 2020](https://vestbee.com/insights/articles/top-vc-funds-in-slovakia-to-finance-your-startup) |
| 7 | Národný holdingový fond | Public (SBA subsidiary) | not captured | SLOVCA full member; a search snippet says it is the SBA subsidiary that delivers state VC support (snippet not verified) | — | [SLOVCA](https://www.slovca.sk/sk/clenstvo/riadni-clenovia.html) |
| 8 | Eterus Capital | PE / growth with VC | eterus.sk | SLOVCA full member | €500k–€5m (2020) | [SLOVCA](https://www.slovca.sk/sk/clenstvo/riadni-clenovia.html); [Vestbee 2020](https://vestbee.com/insights/articles/top-vc-funds-in-slovakia-to-finance-your-startup) |
| 9 | Sandberg Capital | PE | not captured | Closed a fund of about CZK 3bn (article date not captured, likely before 2024) | Fund II €130m (vs €109m target) | [CzechCrunch](https://cc.cz/slovensky-sandberg-capital-uzavrel-svuj-trimiliardovy-fond-stovky-milionu-z-nej-investoval-do-ceskych-firem/) **[pre-2024?]** |
| 10 | ARX Equity Partners, Genesis Capital, Enterprise Investors, CVI, Jet Investment | PE (CZ/PL-based, active in SK) | not captured | SLOVCA full members (2026); ARX and Genesis are EIF-backed | — | [SLOVCA](https://www.slovca.sk/sk/clenstvo/riadni-clenovia.html); [CzechCrunch 2024](https://cc.cz/evropsky-investicni-fond-uz-vlozil-penize-do-17-ceskych-fondu-miliardovy-ted-otevira-s-tensor-ventures/) |
| 11 | Across Private Investments; G4 Investments | Investors (type unclear) | not captured | SLOVCA associate members | — | [SLOVCA](https://www.slovca.sk/sk/clenstvo/pridruzeni-clenovia.html) |
| 12 | CB ESPRI; Sociálni Inovátori Impact Capital | Impact funds | not captured | SIH €10.45m each (contracts to end-2023) | — | [podnikajte.sk](https://www.podnikajte.sk/financie-na-podnikanie/investicny-fond-pre-socialnu-ekonomiku) |
| 13 | LRJ Capital; 365.fintech; IPM Growth | VC | lrjcapital.com; 365fintech.sk; ipmllp.com | Listed in 2020 only; no recent evidence found | LRJ €100k–€2m+ | [Vestbee 2020](https://vestbee.com/insights/articles/top-vc-funds-in-slovakia-to-finance-your-startup) **[pre-2024]** |
| 14 | 3 SIH-selected start-up funds (2026–2030) | VC (public LP) | — | Tender opened 10 Mar 2026; managers not yet named | €30m each | [SIH](https://www.sih.sk/en/aktuality/sih-vyhlasuje-sutaz-na-vyber-spravcov-fondov-na-podporu-startupov-pre-roky-2026-2030) |

Foreign or Czech investors with dated Slovak deals:
- Seed Starter ČS: Vestberry, H1 2025. — [Recursive](https://therecursive.com/search/venture+capital/page/61)
- Purple Ventures II: reported as lead of Sloneek's €3.6m round, 2026. — [Silicon Canals](https://siliconcanals.com/business/hr-tech/page/2/)
- Orbit Capital: reported as co-lead of Sloneek's $6m round. This conflicts with the Purple Ventures report. — **[unverified: seen only in a search snippet; source page not identified]**

**Czechia**

| # | Investor | Type | Evidence of activity (date) | Fund size / ticket (as stated) | Source |
|---|---|---|---|---|---|
| 1 | Credo Ventures | VC (pre-seed, CEE) | Fund V ("Credo Stage 5") closed 23 Mar 2026; backers include Adams Street, RSJ, Sequoia, Isomer, Aspire11 | $88m; initial checks $1–5m; about 30 companies; prior Fund IV €75m (2022) | [The Next Web, 23 Mar 2026](https://thenextweb.com/news/credo-ventures-88m-fund); [Vestbee](https://vestbee.com/insights/articles/credo-ventures-raises-88-m-fund) |
| 2 | Rockaway Ventures (Rockaway Capital) | VC (late seed / A) | Fund II closed 16 May 2025; 11 portfolio companies | about €55m; about 25% from Rockaway Capital | [tech.eu, 16 May 2025](https://tech.eu/2025/05/16/rockaway-ventures-closes-55m-fund-to-back-transformative-tech-in-cee-and-beyond/) |
| 3 | Kaya VC (formerly Enern) | VC (pre-seed–A, CEE) | Fund V first close, reported 25 Jun 2025; on Vestbee's Q3 2025 most-active list | about €70m first close (target €80m); up to 25 start-ups | [Vestbee](https://www.vestbee.com/blog/articles/kaya-secures-70-m); [CzechInvest/Vestbee Q3](https://czechstartups.gov.cz/en/novinky/vestbee-cee-venture-capital-reaches-e510m-across-148-deals-in-q3-driven-by-a-few-standout-rounds) |
| 4 | Soulmates Ventures | VC (sustainability, SFDR Art. 9) | Fund launched Q1 2025 | €50m | [Vestbee Q1 2025](https://vestbee.com/insights/articles/list-of-new-vc-funds-launched-in-q1-2025-to-invest-in-europe) |
| 5 | Orbit Capital (Prague / Warsaw) | Venture/growth debt | Growth Debt II first close, Q2 2025 | €70m first close; €100m target | [Vestbee Q2 2025](https://vestbee.com/insights/articles/list-of-new-vc-funds-launched-in-q2-2025-to-invest-in-europe) |
| 6 | Aspire11 | Fund of funds / direct / secondaries (pension-backed) | Inaugural fund, Q3 2025; LP in Credo V (2026) | €500m | [Vestbee Q3 2025](https://www.vestbee.com/insights/articles/new-vc-funds-q3-2025-to-invest-in-europe) |
| 7 | JIC Ventures (Brno) | Regional VC | Launched April 2026 | CZK 400m; tickets up to €1m; about 20 companies | [Lupa.cz](https://www.lupa.cz/aktuality/v-brne-vznikl-fond-pro-startupy-ktery-bude-investovat-i-penize-kraje/) |
| 8 | Tensor Ventures | VC (pre-seed, NPO/EIF co-investment) | Selected as NPO fund manager (2024); first fund 2017 | Co-investment Fund up to €50m (€20m EIF/NPO); first fund €20m | [CzechCrunch, 15 May 2024](https://cc.cz/evropsky-investicni-fond-uz-vlozil-penize-do-17-ceskych-fondu-miliardovy-ted-otevira-s-tensor-ventures/) |
| 9 | Purple Ventures | VC | Purple Ventures II led Sloneek's €3.6m round (2026); Vestbee Q3 2025 most-active list | — | [Silicon Canals](https://siliconcanals.com/business/hr-tech/page/2/); [CzechInvest/Vestbee Q3](https://czechstartups.gov.cz/en/novinky/vestbee-cee-venture-capital-reaches-e510m-across-148-deals-in-q3-driven-by-a-few-standout-rounds) |
| 10 | Seed Starter ČS (Česká spořitelna) | Bank-backed seed VC | Vestberry seed (H1 2025) | — | [Recursive](https://therecursive.com/search/venture+capital/page/61) |
| 11 | DEPO Ventures (DEPO Ventures One SCSp) | VC (Ukraine/Moldova/Georgia founders) | Selected by NRI for Fond Ukrajina (date not captured) | NRI CZK 94m, up to 141m | [BusinessInfo](https://www.businessinfo.cz/clanky/nri-dokoncila-vyber-venture-kapitaloveho-fondu-pro-program-fond-ukrajina/) |
| 12 | Nation 1 (N1) | VC | New fund; EIF-backed (2024 list) | €20m, possibly +€15m; ¾ from EIF | [CzechCrunch](https://cc.cz/novy-cesky-investicni-fond-nation-1-ma-pro-startupy-500-milionu-korun-do-konce-roku-nabere-temer-miliardu/) (date not captured) |
| 13 | Genesis Capital | PE/growth | EIF's first Czech commitment (2002); SLOVCA member (2026) | — | [CzechCrunch 2024](https://cc.cz/evropsky-investicni-fond-uz-vlozil-penize-do-17-ceskych-fondu-miliardovy-ted-otevira-s-tensor-ventures/) |
| 14 | Espira Investments; i&i Biotech; Arx Equity Partners; Tilia Impact Ventures; Lighthouse Ventures | VC/PE (EIF-backed) | Named in the EIF Czech portfolio (as of 15 May 2024) | Lighthouse tickets up to €2.3m | [CzechCrunch 2024](https://cc.cz/evropsky-investicni-fond-uz-vlozil-penize-do-17-ceskych-fondu-miliardovy-ted-otevira-s-tensor-ventures/); [Vestbee CZ list](https://www.vestbee.com/insights/articles/top-vc-funds-in-czech-republic-to-finance-your-startup) |
| 15 | ZAKA Ventures | VC (seed/A) | Fund I first close (date not captured) | €15m; up to €2.5m | [Vestbee CZ list](https://www.vestbee.com/insights/articles/top-vc-funds-in-czech-republic-to-finance-your-startup) |
| 16 | Czech Founders VC | VC (pre-seed) | Listed (2021, updated 2023) | €50k–€250k | [Vestbee CZ list](https://www.vestbee.com/insights/articles/top-vc-funds-in-czech-republic-to-finance-your-startup) **[pre-2024]** |
| 17 | Reflex Capital; Inven Capital (ČEZ CVC) | VC / CVC | Listed in the CzechInvest directory; claimed 2025–26 deals (Supernova, Choice) not verified | — | [czechstartups.gov.cz](https://czechstartups.gov.cz/en/startup-ecosystem/investors) **[unverified recency]** |
| 18 | J&T Ventures | VC | On Vestbee's 2022 most-active list only | — | [Vestbee 2022](https://vestbee.com/blog/articles/vc-transactions-in-cee-report-2022) **[pre-2024]** |
| 19 | One Family Office (Havel & Partners) | Multi-family office with co-investments | About CZK 12bn AuM (Forbes CZ); co-investments from $1m | — | [ePravo 2024](https://www.epravo.cz/top/aktualne/one-family-office-prinasi-novou-komplexni-uroven-v-oblasti-spravy-majetku-117492.html); [Forbes CZ](https://forbes.cz/elitni-advokat-jaroslav-havel-spravujte-majetek-jako-dolarovi-miliardari/) |

**Wider CEE funds investing into CZ/SK (cheap additions):**
- Inovo VC (PL): co-led Viktor's $75m Series A, Q2 2026. — [Vestbee Q2 2026](https://vestbee.com/insights/articles/vc-funding-in-cee-report-q2-2026)
- Montis VC (PL): €50m first close, Q1 2026. — [Vestbee Q1 2026](https://vestbee.com/insights/articles/new-vc-funds-launched-in-q1-2026-to-invest-in-europe)
- e2vc Fund III: €100m for CEE and the Baltics, Q1 2026. — [Vestbee Q1 2026](https://vestbee.com/insights/articles/new-vc-funds-launched-in-q1-2026-to-invest-in-europe)
- FIRSTPICK, Startup Wise Guys, Coinvest Capital: on Vestbee's Q3 2025 most-active list. — [CzechInvest/Vestbee Q3](https://czechstartups.gov.cz/en/novinky/vestbee-cee-venture-capital-reaches-e510m-across-148-deals-in-q3-driven-by-a-few-standout-rounds)

### Inferences
- **Rough size of the universe (estimate):**
  - Slovakia: about 8–15 genuinely active locally based VC investors in 2024–2026. That is VFF, Vision Ventures, Zero Gravity/0100, Crowdberry/CB IM, Neulogy and FIT, plus the 3 upcoming SIH funds, plus a handful of angels. This fits Invest Europe's 8 Slovak-based funds that raised capital over 2011–2025.
  - Czechia: about 30–50 active VC/growth managers, including CVCs and bank-backed funds. This fits Invest Europe's 30 Czech-based funds, the EIF's 17 Czech fund commitments by 2024, and 75–100 rounds a year (CzechCrunch, Ambit).
- Several Slovak SLOVCA members are PE houses or public bodies, not VC. Several SIH-backed VC funds are past their investment period. A strict "active within 24 months" rule would shrink the Slovak VC pilot set to roughly 5–8 records.

### Gaps
- The CVCA member list (main CZ seed) and the CzechCrunch most-active-fund ranking (paywalled) were not retrieved.
- Websites for most Czech funds were not captured from sources and should be added from each fund's own site.
- Evidence dates are missing for Nation 1, ZAKA and DEPO.
- The Sloneek 2026 round has conflicting accounts (Purple vs Orbit as lead; €3.6m vs $6m).
- Presto Ventures, Miton, StartupYard, Air Ventures and other commonly cited Czech investors were not checked.

---

## 6. Family offices and large private investors (Penta, J&T, PPF, KKCG, Rockaway, DRFG and others): how verifiable?

### Takeaway
Large CZ/SK investment groups are verifiable as investors through their own press releases and annual reports. Group-level equity and profit are often published (e.g. Penta). "Investable capital" for direct deals is rarely stated. Single-family offices are largely undocumented publicly. Treat them as a separate, lower-confidence tier.

### Cited Findings
- Penta Investments (31 Mar 2026):
  - 2025 net profit €714m (2024: €621m); group equity €5.6bn
  - Penta Equity Fund and Penta Real Estate Fund (launched 2025) drew more than 7,500 external investors and over €600m
  - Privatbanka placed €189m of Penta Funds instruments
  - Penta Real Estate total assets over €2.1bn
  — [Penta press release](https://www.pentainvestments.com/en/?p=5609)
- Penta's group asset figure appears only on a third-party profile ("€9bn", undated). — [Revelio Labs](https://www.reveliolabs.com/companies/penta-investments/employees/) **[unverified]**
- Rockaway Capital provided about 25% of Rockaway Ventures II (about €55m). The rest came mostly from Czech private investors (May 2025). — [tech.eu](https://tech.eu/2025/05/16/rockaway-ventures-closes-55m-fund-to-back-transformative-tech-in-cee-and-beyond/)
- One Family Office (with Havel & Partners):
  - launched 2024, targeting $1bn AuM by end-2026
  - minimum client wealth $10m; co-investments from $1m
  - about CZK 12bn under management per Forbes CZ (a self-reported, promotional figure)
  — [ePravo](https://www.epravo.cz/top/aktualne/one-family-office-prinasi-novou-komplexni-uroven-v-oblasti-spravy-majetku-117492.html); [Forbes CZ](https://forbes.cz/elitni-advokat-jaroslav-havel-spravujte-majetek-jako-dolarovi-miliardari/)
- In CEE fundraising, family offices and private individuals gave 21% of 2024 commitments, a 358% rise in absolute terms. — [Invest Europe CEE 2024](https://cvca.hr/wp-content/uploads/2025/12/Invest-Europe_CEE-Statistics_2024.pdf)
- Credo Fund V's LPs include family/private capital (RSJ, Marktlink, Willgrow), named publicly in March 2026. LP lists in fund-close press releases are a public way to identify family offices acting as LPs. — [Vestbee](https://vestbee.com/insights/articles/credo-ventures-raises-88-m-fund)

### Inferences
- **Verifiability tiers (inferred):**
  - **High:** groups with audited consolidated annual reports, press releases and bond prospectuses (Penta; likely J&T Finance Group, PPF Group, KKCG). Investments can be dated from M&A news, but "investable capital" must be proxied by equity or cash on the balance sheet.
  - **Medium:** VC/CVC arms of these groups (Rockaway Ventures, J&T Ventures, Inven Capital), with fund sizes from close announcements.
  - **Low:** single-family offices and angels. Evidence is mostly news mentions, LP lists and RÚZ/justice.cz shareholder records.
- In Slovakia, RÚZ (CC0 statements) plus RPO shareholders can document holding-company portfolios. In Czechia, the same needs justice.cz plus Sbírka listin PDFs.

### Gaps
- J&T, PPF, KKCG and DRFG annual-report AuM/equity figures were not retrieved in this pass. No source was found ranking CZ/SK family offices (no Forbes family-office list found).
- Penta's portfolio-mix figures (healthcare 40%, etc.) came only from a search snippet. **[unverified]**

---

## 7. Which country is the better pilot for VC funds?

### Takeaway
**Czechia is the better pilot.** It has roughly 3–5 times more active VC managers, about 75–100 VC rounds a year that generate dated evidence, more public LP programmes with named managers (EIF 17 funds, NPO/Tensor, NRI/DEPO, JIC), and bulk open data (ČSÚ RES CSV, justice.cz CSV/XML, ARES REST, JERRS). Slovakia's sample (about 5–15 active VCs) is too small to validate precision and recall. It is, however, an ideal cheap second test of the RÚZ-based AuM extraction, because RÚZ is a CC0 JSON API with structured statements.

### Cited Findings
- Fund counts (Invest Europe):
  - 30 Czech-based vs 8 Slovak-based funds raised capital in 2011–2025
  - cumulative fundraising €1,958m vs €252.8m
  — [Invest Europe CEE 2025](https://www.investeurope.eu/media/z3pasguu/20260623_invest-europe_cee-report-2025.pdf)
- Investment in 2025: Czechia about €275m (0.080% of GDP) vs Slovakia about €7m in 5 companies (0.005% of GDP). — [Invest Europe CEE 2025](https://www.investeurope.eu/media/z3pasguu/20260623_invest-europe_cee-report-2025.pdf); [Startitup](https://www.startitup.sk/slovensko-ziskalo-7-cesko-az-275-milionov-eur-nedokazeme-ziskat-zahranicny-kapital-v-europe-sme-uplne-posledni/)
- Czech VC round volume:
  - 75 announced rounds in 2025 — [CzechCrunch](https://cc.cz/zmapovali-jsme-vsechny-investice-ktere-loni-oznamily-ceske-startupy-neseme-tri-dobre-a-tri-spatne-zpravy/)
  - about 100 VC deals (Ambit) — [BusinessInfo](https://www.businessinfo.cz/clanky/investice-do-ceskych-startupu-mene-dealu-vetsi-investice-prisnejsi-investori/)
  - 86 rounds per Dealroom — [EEN/CzechInvest](https://een.gov.cz/en/news/cee-funding-map-provides-an-overview-of-active-investors-in-central-and-eastern-europe/)
- EIF had backed 17 Czech VC/PE funds (€334m) by May 2024. In Slovakia, 2025 EIF activity was guarantees plus €8m of RRF money, with no new VC fund named. — [CzechCrunch](https://cc.cz/evropsky-investicni-fond-uz-vlozil-penize-do-17-ceskych-fondu-miliardovy-ted-otevira-s-tensor-ventures/); [EIB 2026-118](https://www.eib.org/en/press/all/2026-118-slovakia-financing-from-eib-group-jumps-60-to-eur649-million-in-2025-with-focus-on-energy-upgrades-and-urban-development)
- Slovak association and regulator lists:
  - SLOVCA has 12 full members, a mix of PE, VC and public bodies — [SLOVCA](https://www.slovca.sk/sk/clenstvo/riadni-clenovia.html)
  - NBS shows 39 "registered entities" — [subjekty.nbs.sk](https://subjekty.nbs.sk/?s=1059)
- Data access:
  - Slovakia: RÚZ CC0 JSON API with line items — [RÚZ API](https://www.registeruz.sk/cruz-public/home/api)
  - Czechia: RES bulk CSV twice a month — [ČSÚ](https://csu.gov.cz/registr-ekonomickych-subjektu-otevrena-data-dokumentace); JERRS lists and time series, with SOAP access needing a certificate — [WS JERRS](https://www.cnb.cz/cs/dohled-financni-trh/seznamy/webove-sluzby-ws-jerrs/)

### Inferences
- **Sample size:** about 30–50 Czech VC records gives meaningful validation statistics (precision of "is a real active investor", completeness of fields). About 5–15 Slovak records does not.
- **Data availability:**
  - Czechia is stronger on entity discovery: JERRS includes §15 sub-threshold managers, a likely large and noisy pool, plus bulk registers and many dated press sources.
  - Slovakia is stronger on structured financials (RÚZ) and UBO linkage (RPVS, limited to public-sector partners).
  - The required field hardest to fill from public data in both countries is "total investable capital / AuM". It is best taken from fund-close announcements.
- **Suggested design:** Run the Czech VC pilot as the main validation. In parallel, build the full Slovak VC set by hand, which is small enough to serve as a gold standard. Use it to test the RÚZ AuM proxy and the NBS "registered manager" flag.

### Gaps
- The exact number of Czech §15 managers and licensed AIFMs, and therefore the noise ratio of the JERRS seed, was not obtained. Pull JERRS "Počty subjektů" for 2026-10-25 before the pilot.
- The CVCA member count (needed to check the 30–50 estimate) was not retrieved.
