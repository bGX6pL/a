# Global (US, UK, EU-level) public and open data sources for identifying and verifying active private-market investors

Research date: 2026-10-25. All "as of" dates are the dates shown on the source page or the date of my own query. **[PRE-2024]** marks figures older than 1 Jan 2024. **[SECONDARY]** marks figures taken from a non-primary source. **[UNVERIFIED]** marks background knowledge I could not confirm against a primary page in this session.

Target fields used in the coverage notes: TYPE = investor type, SECTOR = sector focus, STAGE = stage / asset class, TICKET = typical ticket size, AUM = total investable capital / AUM, PROOF = a citable public source plus a date showing it actually invests.

---

## 1. SEC sources (Form D, Form ADV / IAPD, 13F, 13D/G, Reg CF Form C, EDGAR APIs, full-text search)

### Takeaway
The SEC is the strongest free, bulk, machine-readable source for US (and many non-US) fund managers. **Form ADV Schedule D 7.B.(1)** gives a per-fund record with fund type (including "venture capital fund" and "private equity fund"), **current gross asset value per fund**, the LP minimum commitment, the number of beneficial owners and the fund's Form D file number. That covers TYPE, STAGE (coarse) and AUM for both Registered Investment Advisers and Exempt Reporting Advisers. **Form D** gives fund type, target size and amount raised for each pooled-fund offering, plus a dated filing that serves as proof of fundraising. It does not give ticket sizes, and it does not list investors in operating-company rounds. 13F and 13D/G only cover holdings of public securities. Form C (Reg CF) covers the issuers and platforms, not who invested.

### Cited Findings
**Form D data sets (DERA)**
- The data sets are quarterly ZIPs of structured data from Form D notices filed under Rule 504, 506(b), 506(c) or Section 4(a)(5). The latest is **2026 Q3** (page updated 30 Sep 2026). The header says "September 2009 – September 2026", but 2008 quarterly files are also listed. Each ZIP is about 3.5 MB per quarter (2026 Q3 = 3.48 MB). Data is "as filed" and the SEC does not guarantee its accuracy. — [SEC Form D Data Sets](https://www.sec.gov/data-research/sec-markets-data/form-d-data-sets)
- The documentation lists six tab-delimited UTF-8 tables: FORMDSUBMISSION, ISSUERS, OFFERING, RECIPIENTS, RELATEDPERSONS and SIGNATURES. They are keyed on ACCESSIONNUMBER (plus a *_SEQ_KEY for repeating rows), they include amendments, and each quarter carries a W3C tabular-data metadata file. Attachments and optional information are excluded. Scope is XML submissions from Jan 2008 onward. — [SEC "Form D Data" documentation (PDF)](https://www.sec.gov/files/Form_D.pdf)
- Fields in the OFFERING table, extracted from that documentation:
  - classification: INDUSTRYGROUPTYPE, INVESTMENTFUNDTYPE, REVENUERANGE, AGGREGATENETASSETVALUERANGE, FEDERALEXEMPTIONS_ITEMS_LIST
  - amendment status: ISAMENDMENT, PREVIOUSACCESSIONNUMBER
  - sale timing: SALE_DATE, YETTOOCCUR, MORETHANONEYEAR
  - security type: ISEQUITYTYPE, ISDEBTTYPE, ISPOOLEDINVESTMENTFUNDTYPE and related flags
  - amounts: MINIMUMINVESTMENTACCEPTED, TOTALOFFERINGAMOUNT, TOTALAMOUNTSOLD, TOTALREMAINING
  - investors: HASNONACCREDITEDINVESTORS, NUMBERNONACCREDITEDINVESTORS, TOTALNUMBERALREADYINVESTED
  - fees and use of proceeds: SALESCOMM_DOLLARAMOUNT, FINDERSFEE_DOLLARAMOUNT, GROSSPROCEEDSUSED_DOLLARAMOUNT
  - RELATEDPERSONS is a separate table, and the FORMDSUBMISSION table includes FILING_DATE and SIC_CODE.

  — [SEC Form D data documentation](https://www.sec.gov/files/Form_D.pdf)
- Scale of Form D filing:
  - 2025: **34,553 new Regulation D offerings** (2024: 32,554) raised **$2,391.5bn**, of which **pooled investment funds accounted for $2,118.3bn (~89%)**. The author says pooled funds are "well under half" of deals by count but gives no fund-only filing count. — [Angel Investors Network, 12 Aug 2026, citing SEC DERA statistics and SEC press release 2026-29](https://angelinvestorsnetwork.com/market-analysis/sec-form-d-private-placements-2026-data) **[SECONDARY]**
  - The SEC's own Reg D statistics page covers calendar years 2009–2025 and quarters 2009Q1–2026Q2 (updated 22 Sep 2026). It counts "the number of initial Form D filings during the report period", and its figures are in a downloadable spreadsheet. The page text shows no breakdown by fund type. — [SEC Regulation D Offerings statistics](https://www.sec.gov/data-research/statistics-data-visualizations/regulation-d-offerings/regulation-d-offerings-number-offerings-capital-raised)
  - Older DERA work found that "the largest number (39%) of Regulation D issuers are from the pooled investment fund industry", with a Table 9 breakdown by fund type for 2009–2019. — [SEC DERA white paper (search-snippet)](https://www.sec.gov/files/dera-white-paper_regulation-d_082018.pdf) **[PRE-2024]**
  - A presentation hosted on sec.gov gives **100,553 pooled-fund offerings for 2009–2023** in total. — [Regulation D: Issuers, Investors and Intermediaries, Sept 2023](https://www.sec.gov/files/craig-mccann-presentation-092123.pdf) **[PRE-2024; third-party presenter]**
  - DERA's fiscal-year table counts 35,080 "New Form D" filings in FY2023, with a 2021 peak of 46,558. — [SEC DERA report (search-snippet)](https://www.sec.gov/files/dera-offering-reg-d-cf-2504.pdf)
  - Reports differ on what they count. One gives 37,785 Reg D offerings for 2017 and another 24,476 new Form Ds. Fund-only counts must therefore be recomputed from the raw data set.

**Form ADV (registered and exempt reporting advisers)**
- The SEC publishes monthly "Investment Adviser Information Reports" as ZIP spreadsheets. There is one file for SEC-registered advisers and one for ERAs; the latest is **October 2026** (ia100226.zip and ia100226-exempt.zip, page updated 2 Oct 2026). The files contain a subset of Items 1–11, and ERAs file only Items 1, 2, 3, 6, 7, 10 and 11. The page does not mention Schedule D. — [SEC: Information about RIAs and ERAs](https://www.sec.gov/data-research/sec-markets-data/information-about-registered-investment-advisers-exempt-reporting-advisers)
- Full Form ADV Part 1 data (multi-table CSV that must be joined) covers 19 Oct 2000 – 31 Dec 2024. Part 2 brochures and Form CRS are separate PDF ZIPs. **Data from 1 Jan 2025 onward is "available on the Investment Adviser Public Disclosure website" at adviserinfo.sec.gov/adv** (page updated 16 Dec 2025). The page does not say whether Schedule D or 7.B.(1) is a separate table. — [SEC FOIA Form ADV Data](https://www.sec.gov/foia-services/frequently-requested-documents/form-adv-data)
- Contents of Schedule D Section 7.B.(1), Private Fund Reporting, from the current Form ADV Part 1A text:
  - Q1: fund name and **private fund identification number**
  - Q2: jurisdiction
  - Q3: GP, manager or directors
  - Q4: 3(c)(1) or 3(c)(7) exclusion
  - Q6–7: master-feeder structure
  - Q8: fund of funds
  - **Q10: fund type** — hedge, liquidity, private equity, real estate, securitized asset, **venture capital** or other
  - **Q11: current gross asset value**
  - **Q12: minimum investment commitment** required of investors
  - **Q13: approximate number of beneficial owners**
  - Q14–16: percentage owned by the adviser or related persons, by funds of funds and by non-US persons
  - Q17–18: sub-adviser and other advisers
  - Q21–22: reliance on Reg D and **the fund's Form D file number (021-…)**
  - Q23 onward: auditors and other service providers

  — [Form ADV Part 1A (PDF)](https://www.sec.gov/files/formadv-part1a_1.pdf)
- Item 2.B lets an ERA claim the exemption as an adviser **"solely to one or more venture capital funds, as defined in rule 203(l)-1"**, or the private fund adviser exemption for under $150m of US AUM (rule 203(m)-1). Item 7.B says an adviser "must complete a Section 7.B.(1) of Schedule D" for each private fund it advises, except where another filer reports that fund (for example, as sub-adviser). — [Form ADV Part 1A (PDF)](https://www.sec.gov/files/formadv-part1a_1.pdf)
- Scale of the adviser population:
  - 2023 data: 5,390 ERAs filed with the SEC and 3,920 with states, together managing over $6tn of private-fund gross assets. **[PRE-2024]**
  - 2025 data: 16,544 SEC-registered advisers, $176.8tn regulatory AUM.

  — [IAA/COMPLY Investment Adviser Industry Snapshot coverage](https://www.investmentadviser.org/iaatoday/news/industry-snapshot-continued-growth-in-demand-for-adviser-services) **[SECONDARY; trade association]**
- Form PF / Private Fund Statistics:
  - 2025Q4: **58,891 private funds** reported on Form PF, with $29.6tn gross and $19.0tn net assets (YoY +9.2% / +18.5% / +16.3%). Page updated 19 Aug 2026.
  - Only SEC-registered advisers with **≥$150m private fund AUM** file Form PF. Smaller RIAs, ERAs and state advisers appear only on Form ADV.
  - Form PF data is aggregate only; there is no per-fund public data.

  — [SEC Private Fund Statistics](https://sec.gov/data-research/statistics-data-visualizations/private-fund-statistics)
- Fund and adviser counts by type sit in a separate JSON file ("Number_of_Funds_and_Advisers_08-05-2026a.json"). Advisers are counted for three quarters after each quarter in which they report a fund. — [SEC: Private funds – number of funds and advisers](https://sec.gov/data-research/data-visualizations/private-fund-statistics/private-funds-number-funds-advisers)
- Form PF private fund information "will not be publicly available on IAPD". — [FINRA IARD notice](https://www.finra.org/sites/default/files/AppSupportDoc/p126051.pdf)

**13F**
- Form 13F data sets run quarterly from July 2013 to **Jun–Aug 2026** (page updated 31 Aug 2026). Since March 2024 each set covers the three months ending Feb, May, Aug or Nov. Data is flattened "as filed" XML. — [SEC Form 13F Data Sets](https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets); [13F readme](https://www.sec.gov/files/form_13f_readme.pdf)

**Reg CF (Form C)**
- Crowdfunding Offerings Data Sets are quarterly ZIPs from **2016 Q2 to 2026 Q3**, built from Form C offering statements, updates (C-U), annual reports and terminations. Co-issuer data starts with 2021Q1. The SEC does not guarantee accuracy. — [SEC Crowdfunding Offerings Data Sets](https://www.sec.gov/data-research/sec-markets-data/crowdfunding-offerings-data-sets); [documentation](https://www.sec.gov/dera/data/crowdfund.pdf)

**EDGAR access rules and APIs**
- Fair access:
  - "Current max request rate: 10 requests/second", which the SEC may lower.
  - The User-Agent must declare the requester, in the form "Sample Company Name AdminContact@<domain>.com".
  - "The SEC does not allow botnets or automated tools to crawl the site."
  - The SEC offers no technical support.
  - Bulk options are the full-index and daily-index files, the Feed/Oldloads tar archives and the CIK/ticker files.
  - "Anyone can access and download this information for free."

  — [SEC: Accessing EDGAR Data](https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data)
- data.sec.gov endpoints:
  - Endpoints: submissions/CIK##########.json, companyconcept, companyfacts and frames. The XBRL endpoints cover 10-K, 10-Q, 8-K, 20-F, 40-F and 6-K forms only.
  - Bulk files: **submissions.zip** (all filers' filing history) and companyfacts.zip, both rebuilt nightly at about 03:00 ET.
  - No authentication, and **no CORS support**.

  — [SEC EDGAR APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)
- EDGAR Full-Text Search:
  - Covers filings "since 2001" and indexes "all data in the filing itself as well as all attachments (such as exhibits)".
  - It is a web interface only; programmatic-use questions go to textsearch@sec.gov.

  — [SEC EDGAR FTS FAQ](https://www.sec.gov/edgar/search/efts-faq.html)
  - The JSON endpoint behind it, efts.sec.gov/LATEST/search-index, is undocumented. Community write-ups report a 10,000-hit cap per query. — [orthogonal.info write-up](https://orthogonal.info/sec-edgar-full-text-search-api-efts-python/) **[SECONDARY]**

### Inferences
- **Form D cannot give TICKET for a fund.**
  - In a fund's Form D, TOTALOFFERINGAMOUNT is the fund's target size and TOTALAMOUNTSOLD is capital raised so far. That is a good proxy for **fund size (AUM)**, with the filing date as **PROOF of fundraising**.
  - MINIMUMINVESTMENTACCEPTED is the LP minimum, not the fund's investment ticket.
  - In an operating company's Form D, the round size is visible but the investors are not. RELATEDPERSONS lists executive officers, directors and promoters, not investors. Investor names appear only incidentally, for example when a VC partner is listed as a director. Form D therefore proves that companies raise money, not who invested.
- **Form ADV gives AUM per fund:** Q11 gross asset value, reported annually, gross rather than net, and excluding uncalled commitments.
  - Firm-level regulatory AUM (Item 5) exists only for RIAs. ERAs do not file Item 5, so ERA AUM must be computed by summing 7.B.(1) gross asset values.
  - ADV gives no SECTOR or TICKET. Use ADV Part 2A brochures (PDF, RIAs only) for strategy text.
- **Linkage keys:**
  - The ADV private fund ID (805-…) and Form D file number (021-…) let you join ADV fund records to Form D filings.
  - The Form D issuer CIK joins to data.sec.gov submissions.
  - ERA status under rule 203(l)-1 is a strong VC flag.
- **Pooled-fund Form D count:** compute it directly as COUNT(*) WHERE INDUSTRYGROUPTYPE='Pooled Investment Fund' AND ISAMENDMENT=false, grouped by INVESTMENTFUNDTYPE and year. Published figures conflict:
  - 100,553 pooled-fund offerings over 15 years (2009–2023) averages about 6,700 a year (my arithmetic).
  - "39% of issuers" applied to about 35k filings a year would imply far more.
- **13F only covers listed US securities.** 13F (managers with ≥$100m in 13(f) securities **[UNVERIFIED]**) and 13D/G (>5% stakes in registered equity **[UNVERIFIED]**) report public-market positions. They help identify large family offices or crossover funds and give a dated proof, but say nothing about private holdings.
- **Form C covers issuers and platforms only.** It shows issuer, intermediary or portal, target and maximum amounts, and progress updates **[UNVERIFIED field detail]**. It does not show who invested, so it helps with the "crowdfunding platform" investor type but not with identifying angels.
- **Fetch-script design:**
  - Use quarterly ZIPs for Form D, 13F and Form C.
  - Use nightly submissions.zip for the filing-history index.
  - Use the full-index files for Form D, ADV and 13F accession lists.
  - Keep a ≤10 req/s token bucket with a contact User-Agent.
  - Do not use FTS as a bulk source.

#### Catalog rows
| Source | Investor types | Fields | Count (date) | Access | Licence/ToS | Cadence | Reliability |
|---|---|---|---|---|---|---|---|
| Form D data sets | Pooled funds: VC / PE / hedge / other | TYPE, fund size (target & sold), LP minimum, #investors, PROOF (filing date) | ~34.5k new Reg D offerings in 2025 (all issuers) [SECONDARY] | Bulk quarterly TSV ZIP | US gov public data; fair-access rules | Quarterly | As filed. Many funds never amend, so TOTALAMOUNTSOLD goes stale. Non-US funds and 4(a)(2) deals are often missing. |
| Form ADV Sch. D 7.B.(1) | RIAs and ERAs; per-fund records incl. VC & PE | TYPE, fund GAV (AUM), LP minimum, #owners, Form D link | 58,891 funds on Form PF alone (2025Q4); ADV covers more | Pre-2025 CSV bulk; 2025+ via IAPD (format unclear) | Public | Monthly firm files; filings annual plus amendments | Self-reported. GAV is annual and gross. Fund names may be coded (rule 204-2(d)). |
| 13F / 13D/G | Large managers, family offices | Public holdings only | n/a | Bulk quarterly / EDGAR | Public | Quarterly / event | Listed securities only |
| Form C | Issuers, funding portals | Offering amounts | 2016Q2–2026Q3 | Bulk quarterly | Public | Quarterly | No investor identities |

### Gaps
- I could not confirm what format the post-2025 Form ADV data takes on adviserinfo.sec.gov/adv, or whether it includes Schedule D 7.B.(1) as a table (the page is JavaScript-rendered). The IAPD "compilation" XML feed was not verified.
- I could not confirm exactly which 7.B.(1) questions ERAs may skip.
- No primary SEC per-year count of **fund** Form Ds by type (VC / PE / hedge) for 2024–2025 was found. The Reg D statistics spreadsheet and the 2025 DERA report were not opened.
- The fund-type counts in the Form PF JSON (number of VC and PE funds) were not retrieved.
- No SEC statement on reuse licensing was found beyond "free to access"; US federal works are generally public domain **[UNVERIFIED]**.

---

## 2. UK sources (Companies House, FCA Register, British Business Bank / British Patient Capital)

### Takeaway
Companies House offers free bulk and API data covering every UK company, with SIC codes and PSC (beneficial control) data. SIC 64303 ("venture and development capital") gives an over-inclusive candidate list of about 4,400 active companies. Most are SPVs or personal investment vehicles, so SIC alone is not proof of investing. The FCA Register API identifies regulated managers (full-scope AIFMs, small registered AIFMs, RVECA/SEF managers) but has no documented bulk download. British Patient Capital publishes portfolio totals; I could not confirm a structured fund-by-fund list.

### Cited Findings
- Companies House API:
  - "You can make up to 600 requests within a five-minute period". Exceeding that returns 429 until the window resets.
  - Repeat abusers "may be banned without notice".
  - Higher limits are available on request.

  — [Companies House API rate limiting](https://developer-specs.company-information.service.gov.uk/guides/rateLimiting)
- Free Company Data Product:
  - Monthly CSV snapshot of live companies, compiled to the previous month-end and published within 5 working days.
  - Latest file: **BasicCompanyDataAsOneFile-2026-10-01.zip (471 MB)**, also available as 7 parts.
  - "Provided free of charge and will not be supported."

  — [Companies House Free Company Data Product](https://download.companieshouse.gov.uk/en_output.html)
- PSC snapshot:
  - JSON, **refreshed daily** before 10am, compiled to the end of the previous day.
  - One archive or 33 parts (about 5–80 MB each; roughly 2.4 GB in total by my sum). Latest dated **25 Oct 2026**.
  - Field list is on the API site.

  — [Companies House PSC snapshot](https://download.companieshouse.gov.uk/en_pscdata.html)
- SIC 64303 ("Activities of venture and development capital companies"): **4,377 active companies**, based on Companies House Basic Company Data. Page updated 1 Dec 2025. — [GB Companies directory, SIC 64303](https://gbcomp.p-o.co.uk/en/siccode/64303) **[SECONDARY]**
- FCA Register API:
  - Base URL https://register.fca.org.uk/services/V0.1. Requires registration plus X-AUTH-EMAIL and X-AUTH-KEY headers, and is GET-only.
  - Endpoints: Firm (by FRN, with permissions, passports, individuals, appointed representatives, disciplinary history and requirements), Individuals (by IRN), Funds/CIS (by PRN), and Search (firm / individual / fund).
  - Rate limit: **50 requests per 10 seconds**; breaching it returns 429 and a 1-minute block.
  - No bulk download is described.

  — [Financial Services Register API docs (third-party client)](https://financial-services-register-api.readthedocs.io/en/latest/sources/financial-services-register-api.html) **[SECONDARY]**; official portal: [FCA Register Developer Portal](https://register.fca.org.uk/Developer/s/)
  - Another third-party source cites 100 requests per 60 seconds. — [Apify FCA Register scraper](https://apify.com/danielainsworth/fca-register) **[SECONDARY; conflicts]**
- FCA register of small registered UK AIFMs:
  - The FCA keeps a list of "all current and lapsed" small registered UK AIFMs since Nov 2013, including UK managers of SEF and RVECA funds. Lapsed firms are included, so it is not an active count.
  - Annual fee £781.

  — [FCA: Apply to be a registered AIFM](https://www.fca.org.uk/firms/aifmd/apply-registered-aifm)
- Older FOI-based counts:
  - 2,721 FCA-authorised AIFMs as of 1 Sep 2017 **[PRE-2024]**
  - 105 firms with only the small-AIFM requirement in Feb 2021 **[PRE-2024]**

  — [FCA FOI7928 response](https://www.fca.org.uk/publication/foi/foi7928-response.pdf); [FCA FOI7928 page](https://fca.org.uk/freedom-information/information-alternative-investment-fund-manager-aifm-populations-february-2021)
- British Patient Capital, year to 31 Mar 2024:
  - 44 fund managers in the portfolio, about 1,350 underlying companies.
  - Since inception: £2,287m across 80 fund commitments, 10 co-investments and 18 Future Fund: Breakthrough deals.
  - The programme has £2.5bn to invest over 10 years from June 2018.

  — [BBB: BPC Full Year Results to March 2024](https://www.british-business-bank.co.uk/news-and-events/news/british-patient-capital-full-year-results-period-ending-31-march-2024)
- British Patient Capital, year to 31 Mar 2023: 70 funds managed by 40 firms. — [BBB: BPC results to March 2023](https://www.british-business-bank.co.uk/news-and-events/news/british-patient-capital-full-year-results-period-ending-31-march-2023) **[PRE-2024]**

### Inferences
- **SIC codes produce candidates, not verified investors.**
  - Codes to use: 64303 (VC), 64209 (other holding companies), 64999 (other financial intermediation), 66300 (fund management) **[UNVERIFIED descriptions for 64209 / 64999 / 66300]**.
  - These codes mostly catch holding companies, SPVs and personal investment companies. Use them only to generate candidates, then require PROOF from another source (FCA permission, Form D or ADV, LP disclosure, portfolio page, or PSC links into investee companies).
- **Reverse lookup via PSC.** Corporate PSC records ("corporate-entity-person-with-significant-control" kinds **[UNVERIFIED field names]**) show which entities control which companies. Searching PSC data for known fund LPs or GPs as controlling persons of operating companies gives dated evidence of control-level investments, mainly PE/buyout. Minority VC stakes usually stay below the 25% threshold and do not appear.
- **Shareholdings via filings.** Confirmation statements and SH01 allotment filings (filing-history API; documents are PDF) name shareholders, which helps detect VC and angel participation. It is document-level and needs OCR or parsing; there is no bulk structured shareholder dataset **[UNVERIFIED]**.
- **FCA authorisation as an existence signal.** FCA permissions ("managing an AIF", small registered AIFM, RVECA) confirm a regulated manager exists but not AUM or deployment. There is no bulk export, so script FRN-by-FRN lookups at ≤50 req/10 s, seeded from Companies House candidates or ESMA/GLEIF names.
- **API sizing.** At 600 requests per 5 minutes, about 172,800 Companies House calls a day are possible (my arithmetic). Use the monthly and daily bulk files for the base load and the API for deltas.

#### Catalog rows
| Source | Investor types | Fields | Count (date) | Access | Licence/ToS | Cadence | Reliability |
|---|---|---|---|---|---|---|---|
| CH Free Company Data | All UK cos; SIC-filtered VC/holding cos | Name, number, SIC, status, address | ~4,377 active SIC 64303 (Dec 2025) [SECONDARY] | Bulk CSV 471 MB | Free, unsupported; licence not stated on page | Monthly | Self-chosen SIC; noisy |
| CH PSC snapshot | Corporate/individual controllers | Control links (≥25%) | n/a | Bulk JSON ~2.4 GB | Free | Daily | Under-captures minority stakes |
| CH API | Same | Officers, filings, PSC, charges | n/a | REST, key, 600/5 min | Free | Live | Good |
| FCA Register API | AIFMs, small AIFMs, RVECA/SEF managers | Permissions, status, individuals | n/a | REST, key, ~50/10 s | Not found | Live | Authoritative for regulatory status |
| BPC / BBB | Govt fund-of-funds | Aggregate totals | 80 commitments (Mar 2024) | HTML press releases | — | Annual | Fund-level list not confirmed |

### Gaps
- The Companies House reuse licence (often described as the Open Government Licence) was not confirmed on the pages fetched.
- The current count of small registered UK AIFMs, and whether the FCA list can be downloaded, were not determined.
- Whether British Patient Capital or BBB publish a fund-by-fund portfolio page with commitment amounts was not confirmed.
- The FCA Register API's official terms of use and rate limit were not read from the FCA portal; the figures above come from a third-party client.

---

## 3. EU-level sources (ESMA registers, GLEIF LEI / Level 2, beneficial-ownership registers after CJEU Nov 2022)

### Takeaway
The ESMA Registers provide CSV export (no documented API) of authorised AIFMs, UCITS management companies, EuVECA, EuSEF and ECSP entities. The ELTIF register is a separate ESMA document. GLEIF is the best open (CC0) bulk identity layer, published three times a day. It has explicit fund-to-manager relationships (IS_FUND-MANAGED_BY, IS_SUBFUND_OF, IS_FEEDER_TO), which can map fund vehicles to their manager. Public beneficial-ownership access in the EU ended after the CJEU ruling and is being rebuilt as "legitimate interest" access under AMLD6. It is not usable for bulk commercial investor discovery.

### Cited Findings
- ESMA Registers (registers.esma.europa.eu):
  - Entity register for "MiFID/UCITS/AIFMD/EUSEF/EUVECA/ECSPR entities".
  - Filters: legal framework, name, home and host Member State, status, LEI, authorisation and withdrawal dates. Entity tabs cover identifiers, activities and notified host states.
  - **Export as PDF or CSV only**; the help file mentions no API.
  - ELTIF and MMF are not part of this interface.

  — [ESMA Registers help file](https://registers.esma.europa.eu/publication/helpPage)
- ESMA ELTIF register:
  - Published as a separate ESMA document (ESMA34-46-101). — [ESMA ELTIF register page](https://www.esma.europa.eu/sv/node/92169)
  - 159 ELTIFs listed as of 7 Mar 2025 (62 authorised in 2024); Luxembourg 100, France 32, Italy 13. — [Universal Investment / BAI Newsletter II 2025](https://universal-investment.com/-/media/Project/Universal-Investment-Reference-Page/Universal-Investment/Medienkooperationen/BAI-Newsletter_II_2025.pdf) **[SECONDARY]**
  - Morningstar's 2026 report counts 189 new ELTIFs authorised since the start of 2024, from 72 new firms. — [Morningstar ELTIF 2026](https://www.morningstar.com/content/cs-assets/v3/assets/blt9415ea4cc4157833/blt1a5a934435a71f76/69c40d5a1b3f55790a4895f2/Eltif_2026_Final.pdf) **[SECONDARY]**
- ECSP (crowdfunding service providers):
  - ESMA keeps the Art. 14 register of providers authorised under Reg. (EU) 2020/1503: name, legal form, LEI, platform, authorising NCA and host states.
  - Withdrawals stay in the register for five years.

  — [ESMA Databases and Registers](https://www.esma.europa.eu/databases-and-registers); [FMA Austria](https://www.fma.gv.at/en/financial-service-providers/crowdfunding-service-providers/authorised-crowdfunding-services-providers-in-europe/)
  - EUROCROWD keeps a non-exhaustive list citing the ESMA register as accessed on 16 Jan 2026, and earlier flagged "significant concerns" about data representation in the register. — [EUROCROWD platforms under ECSPR](https://eurocrowd.org/platforms-under-ecspr/) **[SECONDARY]**
- GLEIF Golden Copy:
  - Formats: XML, CSV and JSON.
  - Published **three times daily** (02:00, 10:00 and 18:00 UTC).
  - Delta files against the versions from 8 hours, 24 hours, 7 days and 1 month earlier.
  - Adds geocodes and normalised addresses.

  — [GLEIF Golden Copy](https://www.gleif.org/en/lei-data/gleif-golden-copy)
- GLEIF terms of use:
  - LEI data is "provided under the CC0 licence".
  - Users must not imply GLEIF endorsement or circumvent technical restrictions.
  - Liquidated damages of CHF 100,000 per breach.

  — [GLEIF LEI Data Terms of Use](https://www.gleif.org/en/meta/lei-data-terms-of-use)
- GLEIF fund relationships in the Relationship Record (RR) CDF:
  - **IS_FUND-MANAGED_BY**: fund → management entity "legally responsible for the constitution and operation of the fund"
  - **IS_SUBFUND_OF**: sub-fund → umbrella fund
  - **IS_FEEDER_TO**: feeder → master fund
  - The API exposes these as paired links, and the IS_INTERNATIONAL_BRANCH_OF type is retained.

  — [GLEIF RR-CDF format](https://www.gleif.org/en/about-lei/common-data-file-format/relationship-record-cdf-format)
  - The API needs no authentication. — [API Evangelist GLEIF profile](https://providers.apievangelist.com/providers/gleif/) **[SECONDARY]**
- CJEU WM and Sovim (22 Nov 2022) and its aftermath:
  - Public access to BO registers was held to be a serious, disproportionate interference, and Art. 1(15)(c) AMLD5 is invalid. Ireland moved to legitimate-interest applications. — [McCann FitzGerald](https://www.mccannfitzgerald.com/knowledge/asset-management-and-investment-funds/public-access-to-beneficial-ownership-information-restricted) **[PRE-2024]**
  - Austria, the Netherlands, Belgium and Ireland suspended their registers. — [Spear's](https://spearswms.com/wealth/is-this-the-beginning-of-the-end-for-beneficial-ownership-registers/) **[PRE-2024; SECONDARY]**
- AMLD6 (Directive (EU) 2024/1640) and its transposition:
  - Art. 74 limits access to authorities, obliged entities and persons who "demonstrate a legitimate interest".
  - The Commission opened infringement proceedings against 18 Member States for incomplete AMLD6 transposition.
  - Sources say Arts 11, 12, 13 and 15 (register provisions) were due by **10 July 2026**.

  — [Mondaq: transposition of EU AML Directive](https://www.mondaq.com/corporate-and-company-law/1651480/amendments-to-beneficial-ownership-regulations-following-transposition-of-eu-aml-directive); [A&O Shearman: operation of the RBO](https://www.aoshearman.com/en/insights/operation-of-the-register-of-beneficial-owners-have-we-finally-reached-a-turning-point)
- Italy: Legislative Decree No. 210 of 31 Dec 2025 (in force 9 Jan 2026) implements Art. 74. Non-obliged parties must show a "relevant and differentiated legal interest" ("direct, concrete and current") backed by documented evidence. Access is no longer open to the general public, and the register remains suspended pending a CJEU ruling. — [A&O Shearman: Italy BO register new access rules](https://www.aoshearman.com/en/insights/beneficial-ownership-register-new-access-rules-enter-into-force)

### Inferences
- **Use GLEIF as the identity spine.**
  - Pull managers via IS_FUND-MANAGED_BY end-nodes, grouping funds by manager LEI. Fund names often encode strategy and vintage ("… Ventures Fund III SCSp").
  - CC0 allows bulk reuse in PostgreSQL. The no-endorsement and no-circumvention clauses still apply.
  - The LEI-CDF EntityCategory value "FUND" can filter fund entities **[UNVERIFIED]**.
  - Coverage of the fund relationships depends on what LOUs and registrants report, so expect gaps.
- **ESMA registers prove status, not activity.** Authorisation or registration of an AIFM or EuVECA manager is evidence of existence and regulatory standing, but not of deployment, AUM or ticket size. The fetch script should use the CSV export, saved per legal framework, since no API is documented. Completeness depends on NCAs' uploads.
- **Do not plan on BO registers.** EU BO data should not be planned as a source for a commercial investor database: post-2022 access is case-by-case legitimate interest, and countries differ. National company registers are covered by another researcher.

#### Catalog rows
| Source | Investor types | Fields | Count (date) | Access | Licence/ToS | Cadence | Reliability |
|---|---|---|---|---|---|---|---|
| ESMA Registers (AIFMD/EuVECA/EuSEF/ECSP) | AIFMs, EuVECA/EuSEF managers & funds, crowdfunding platforms | TYPE (via framework), LEI, country, auth date | ELTIF 159 (Mar 2025) [SECONDARY] | Web + CSV export | ESMA site terms (not checked) | NCA-driven | Patchy NCA uploads |
| GLEIF Golden Copy + RR | Funds, managers, holding cos | Legal name, LEI, address, fund→manager links | (global LEI population not checked) | Bulk XML/CSV/JSON, 3×/day + deltas; REST API | CC0 (+ ToU) | 3×/day | Good identity data; relationship coverage depends on reporting |
| EU BO registers | Natural-person UBOs | — | — | Legitimate interest only | GDPR-restricted | — | Not usable in bulk |

### Gaps
- ESMA AIFM register completeness by Member State, and the current EuVECA and ECSP counts, could not be confirmed.
- The ELTIF register's current row count (2026) was not found.
- The GLEIF API rate limit was not found in official documentation; a "60 requests per minute" figure circulates but could not be confirmed.
- I found no consolidated status of every Member State's BO register as of Oct 2026.

---

## 4. Fund-of-funds and LP disclosures (EIF, EIB, KfW Capital, Bpifrance, US public pensions, endowments)

### Takeaway
LP disclosures are the best **PROOF** that a GP actually raises and deploys capital: a named fund, a vintage, a commitment amount and a date. US public pensions publish the most structured lists. CalPERS has a fund-level table (fund, vintage, commitment, cash in/out, net IRR) as of 31 Dec 2025; WSIB publishes quarterly PDFs. European public fund-of-funds mostly publish aggregates and per-deal press releases rather than downloadable lists. EIF's fund-list PDFs I found date from 2022.

### Cited Findings
- CalPERS Private Equity Program (PEP) Fund Performance Review:
  - Columns: fund name, **vintage year**, **capital committed**, cash in, cash out, cash out plus remaining value, net IRR and investment multiple.
  - The latest version is as of **31 Dec 2025** (program net IRR 11.6%, 1.5x).
  - Active partnerships only; generally a 2-quarter reporting lag.
  - CalPERS publishes the same format for Private Debt (e.g. Antares Credit Opportunities CA LLC, vintage 2021, $885m committed).

  — [CalPERS PEP Fund Performance Review](https://www.calpers.ca.gov/investments/about-investment-office/investment-organization/pep-fund-performance); [CalPERS Private Debt](https://www.calpers.ca.gov/investments/about-investment-office/investment-organization/private-debt-performance)
  - The table is rendered by a web application, which returned "This Application Is Currently Unavailable" when fetched on 25 Oct 2026.
- WSIB (Washington State Investment Board):
  - Quarterly "Private Equity Portfolio Overview by Strategy" PDFs, with IRRs computed by Hamilton Lane and a one-quarter lag. Strategies: corporate finance, growth equity, VC, special situations and distressed. — [WSIB quarterly report (2021 example)](https://www.sib.wa.gov/docs/reports/quarterly/ir063021.pdf) **[PRE-2024 example file]**
  - Private markets committee materials name new commitments (e.g. Insight Partners XI at $200m, Madison Dearborn VIII at $250m). — [WSIB private markets committee content (Nov 2025)](https://sib.wa.gov/docs/meetings/private/25_1106content.pdf); [Buyouts Insider](https://www.buyoutsinsider.com/washington-eyes-commitments-to-insight-madison-dearborn-funds/) **[SECONDARY]**
  - WSIB's PE portfolio was $49.9bn at 30 Jun 2025. — [AlphaMaven](https://www.alpha-maven.com/story/real-estate/wsib-commits-12b-to-private-equity-amid-signs-of-sector-resiliency-markets-group) **[SECONDARY]**
- EIF:
  - The VC & PE page linked two PDFs: active funds still investing, and all active EIF investments. They exclude co-investments, business-angel deals and fund-of-funds structures, and the overview is **dated 30 Sep 2022** **[PRE-2024]**. — [EIF for VC & PE funds (search snippet; page returned 404 on fetch 25 Oct 2026)](https://eif.org/what_we_do/equity/deals/index_.htm)
  - EIF lists all financial intermediaries with ongoing InvestEU agreements (debt, VC, PE, private credit). — [EIF InvestEU financial intermediaries](https://eif.org/InvestEU/financial-intermediaries/index.htm)
  - 2024: 196 transactions and €7.2bn committed to equity. — [EIF Annual Report 2024](https://www.eif.org/news_centre/publications/eif-annual-report-2024.htm)
  - Per-deal press releases name the fund and the commitment amount (e.g. €30m to an Alfa Framtak fund). — [EIF press release](https://www.eif.org/press/all/alfa-framtak-lands-eur30-million-european-commitment-for-icelandic-private-equity-fund)
- KfW Capital:
  - Portfolio of about **€2.9bn across 153 VC funds** at end-2025.
  - 2025 commitments of about €748m, including €383m across 21 European VC funds.
  - Growth Fund Germany: about €850m committed to 42 target funds.
  - Sector split: ICT 47%, Life Sciences 21%, Industrial Tech 9%, Generalist 23%.

  — [KfW press release 26 Feb 2026](https://www.kfw.de/About-KfW/Newsroom/Latest-News/Pressemitteilungen-Details_882944.html); [KfW Capital reporting 2025](https://www.kfw.de/About-KfW/Reporting-Portal/Berichterstattung-2025_EN/KfW-Capital/)
  - PitchBook's free view lists 38 KfW Capital commitments but shows only 5. — [PitchBook LP profile](https://pitchbook.com/profiles/limited-partner/277650-01) **[paywalled]**
- Bpifrance:
  - Activity results for 2025 were presented on 17 Feb 2026. — [Banque des Territoires](https://www.banquedesterritoires.fr/regions-et-bpifrance-un-partenariat-fructueux-en-2025)
  - The retail fund-of-funds "Bpifrance Entreprises 3" holds stakes in 76 French PE funds. — [toutsurmesfinances](https://www.toutsurmesfinances.com/placements/bpifrance-entreprises.html) **[SECONDARY]**
  - A 2026 IPP report analyses Bpifrance private equity. — [IPP Rapport 69](https://www.ipp.eu/wp-content/uploads/2026/07/Rapport_IPP_69_BPI_Private_Equity.pdf)
  - No consolidated public partner-fund list was found.

### Inferences
- **US public pensions are the richest structured PROOF source.**
  - They give fund name, vintage, commitment and as-of date.
  - **Fund size and GP AUM are not included.** Join to Form D (TOTALAMOUNTSOLD) and Form ADV (Q11) through the fund name to fill AUM.
  - Many other pensions (CalSTRS, Oregon, Texas TRS etc. **[UNVERIFIED]**) publish similar tables, mostly as PDF or HTML. Expect per-source parsers and robust fund-name normalisation ("Fund III, L.P." vs "III LP").
- **European fund-of-funds PROOF must be assembled from press releases.**
  - Sources are dated press releases from EIF, KfW, BBB and Bpifrance, plus annual reports.
  - The 2022 EIF PDFs can seed a list of historic GPs, but they need re-verification.
  - The InvestEU intermediary list is the most current EIF-wide roster.
- **Endowments rarely publish fund-level holdings.** Public university systems may disclose under state public-records laws **[UNVERIFIED]**.

#### Catalog rows
| Source | Investor types | Fields | Count (date) | Access | Licence/ToS | Cadence | Reliability |
|---|---|---|---|---|---|---|---|
| CalPERS PEP/PD tables | PE/VC/credit GPs (as fund managers) | Fund, vintage, commitment, IRR, PROOF | as of 31 Dec 2025 | HTML app (JS) | Public records | Semi-annual/quarterly, 2Q lag | High; active funds only |
| WSIB quarterly PDFs | PE/VC GPs | Fund, vintage, commitment, IRR | Quarterly | PDF | Public records | Quarterly, 1Q lag | High |
| EIF lists / InvestEU / press | EU VC/PE/private credit GPs | Fund, commitment (press), country | 196 equity deals (2024) | PDF/HTML | EIF site terms (not checked) | Ad hoc | Fund lists stale (2022) |
| KfW Capital | German/EU VC GPs | Aggregates + press | 153 funds (end-2025) | HTML press | — | Annual | No full list found |
| BPC, Bpifrance | UK / FR VC & PE GPs | Aggregates | see §2 | HTML / PDF | — | Annual | No full list found |

### Gaps
- I did not verify CalSTRS, Oregon, NYSCRF, Texas or university endowment disclosure formats.
- I found no EIB-level fund list.
- I could not confirm whether EIF still publishes a current fund-list PDF (the page returned 404 on 25 Oct 2026).
- I could not confirm whether KfW Capital, BPC or Bpifrance publish full fund-by-fund portfolio pages with commitment sizes.

---

## 5. Open datasets and the open web (Wikidata, OpenCorporates, Crunchbase free tier, OpenVC, GitHub/Kaggle, GDELT, Common Crawl, press wires, firm websites)

### Takeaway
Wikidata (CC0) is small but clean, and its "investor" property (P1951) gives dated, citable investor→company edges for notable deals only. OpenCorporates is ODbL share-alike, and free access is limited to journalists, NGOs and academics, so it is not usable commercially without a licence. Crunchbase's free and Basic tiers prohibit scraping, bulk storage and AI training. Kaggle and GitHub Crunchbase mirrors are typically the 2013 snapshot and stale. News and press-release wires are the main open source of deal-level PROOF, but wire terms restrict reuse; GDELT is the most permissive news index. Firms' own websites are the only broad source of stated TICKET and SECTOR.

### Cited Findings
- **Wikidata** (my SPARQL queries on 25 Oct 2026):
  - Property **P1951 "investor"** (individual or organisation investing for financial return) has **7,190 statements**, with **980 distinct investor items** and **6,513 distinct investee items**. — [Wikidata API property search](https://www.wikidata.org/w/api.php?action=wbsearchentities&search=investor&type=property&language=en&format=json&limit=10); [Wikidata Query Service](https://query.wikidata.org/)
  - Class counts (direct P31 only, no subclass traversal): **venture capital firm (Q3487908) = 348**, **private equity firm (Q5418962) = 90**, **private equity fund (Q5978114) = 37**, **investment company (Q1752459) = 278**. — [Wikidata Query Service](https://query.wikidata.org/)
  - Items with industry (P452) = venture capital (Q219409): 63. Industry = private equity (Q476115): 86. — [Wikidata Query Service](https://query.wikidata.org/)
  - Related property: P8324 "funder". — [Wikidata API](https://www.wikidata.org/w/api.php?action=wbsearchentities&search=investor&type=property&language=en&format=json&limit=10)
  - Wikidata structured data is CC0. — [Wikidata:Licensing](https://www.wikidata.org/wiki/Wikidata:Licensing) (not re-fetched this session)
- **OpenCorporates:**
  - Data is offered under the **share-alike attribution Open Database Licence (ODbL)**, plus a paid non-open licence for users who do not want to share derived databases. Free access covers personal website use and "journalists, NGOs and academics… conducting public benefit research". Financial institutions and corporations are not Permitted Users. — [OpenCorporates Terms of Use](https://opencorporates.com/terms-of-use-2/)
  - If your use lets you share results under the open licence, bulk products can be provided at no cost. The API is paid, "from as little as £99/year". — [OpenCorporates bulk data legal page](https://assets.opencorporates.com/legal/bulk_core_legal_entity_data)
  - Reported free-key limits are 200 requests per month and 50 per day. — [Tildes forum](https://tildes.net/~tech/1qs2/interpreting_the_open_database_license) **[SECONDARY, anecdotal]**
- **Crunchbase Terms of Service** (updated 30 Sep 2026). Users may not:
  - "crawl, scrape or spider" any page or data
  - use "any automated means or tools" to access or export content
  - copy or store "any significant portion" of the content
  - use content to train models

  Other uses require prior written consent, and API use or data export needs a separate arrangement. **Crunchbase Basic and the 2013 Snapshot are licensed under Creative Commons Attribution**, subject to the Terms. — [Crunchbase Terms of Service](https://about.crunchbase.com/terms-of-service/)
  - Crunchbase data was historically CC-BY-NC / CC-BY until 2016, and newly created data sets can no longer be shared free. — [arXiv 1907.08671](https://ar5iv.arxiv.org/html/1907.08671) **[PRE-2024]**
  - The Kaggle "Startup Investments" dataset is the Crunchbase 2013 Snapshot, with data up to Dec 2013. — [Baselight mirror of Kaggle dataset](https://baselight.app/u/kaggle/dataset/justinas_startup_investments) **[PRE-2024 data]**
- **OpenVC:**
  - Claims "16,000+" early-stage investors (one listing says 16,696 across 6,000+ firms, angel networks and family offices).
  - Export applies only to the user's own CRM (CSV/XLS). ToS not located.

  — [OpenVC investor database](https://openvc.app/investor-database); [AngelsPartners review](https://angelspartners.com/reviews/openvc/) **[SECONDARY]**
- **Press-release wires:**
  - Business Wire limits site use to "submission of news releases…, retrieving RSS feeds, and the reading of releases". — [Business Wire Terms of Use](https://www.businesswire.com/terms-of-use)
  - GlobeNewswire offers RSS feeds by subject, industry and exchange, plus media-partner arrangements. — [GlobeNewswire media partners](https://www.notified.com/GNW-PR/media-partners)
- **Common Crawl:** generally no republishing of crawled content, no resale, no illegal use, and users must respect crawled sites' terms. — [Common Crawl FAQ](https://commoncrawl.org/faq); [AWS Open Data Registry](https://registry.opendata.aws/commoncrawl/)
- **GDELT:** reportedly free for "unlimited and unrestricted use" (academic, commercial, governmental) with citation and link back. — [jwatte.com blog quoting GDELT terms](https://jwatte.com/blog/gdelt-open-data-kalev-leetaru.md) **[SECONDARY]**

### Inferences
- **Wikidata**
  - Useful for seeding and cross-checking large, well-known investors. With fewer than 1,000 investors carrying P1951 edges, it is far too sparse to be a primary source.
  - Qualifiers such as point in time (P585) on P1951 statements, where present, give dated PROOF with references.
  - CC0 allows unrestricted loading. Use SPARQL with a polite User-Agent, or the weekly JSON dumps.
- **OpenCorporates:** treat it as unavailable for a commercial product unless you buy a licence or accept ODbL share-alike on the derived database. Use primary registers (Companies House, GLEIF, SEC) instead.
- **Crunchbase:** a DB loader should not ingest Crunchbase pages or the free tier. The CC-BY "Basic" carve-out is tied to compliance with ToS clauses that forbid scraping and storing significant portions, so it is unusable in bulk without a licence.
- **News and wires:** store headline, URL, date and extracted facts (investor, investee, round, amount) rather than full text. That is defensible as fact extraction, but wire ToS should be reviewed with counsel. GDELT can be the discovery index, linking out to the original URLs.
- **Firm websites:** the only broad public source of stated TICKET, SECTOR and STAGE, and often of fund size. Respect robots.txt and site ToS, rate-limit, store the URL and fetch date as PROOF, and re-crawl periodically to detect stale "Fund II" claims.

#### Catalog rows
| Source | Investor types | Fields | Count (date) | Access | Licence/ToS | Cadence | Reliability |
|---|---|---|---|---|---|---|---|
| Wikidata | Notable VC/PE firms, funds, angels | TYPE, HQ, website, investor→company edges | 980 investors on P1951; 348 VC firms (25 Oct 2026) | SPARQL, dumps | CC0 | Continuous | Sparse; crowd-edited |
| OpenCorporates | All companies | Registry data | — | Paid API / bulk | ODbL share-alike; commercial licence | — | Mirrors registries |
| Crunchbase free/Basic | VC, angels, PE | Rounds, investors | — | Web/API | No scraping, no storage | — | Not reusable |
| Kaggle/GitHub CB mirrors | VC | Rounds | to Dec 2013 | Download | CB 2013 snapshot terms | Frozen | Stale |
| OpenVC | Early-stage VCs, angels | Stage, ticket, sector (self-reported) | 16,000+ (2026) | Web app | ToS not found | — | Self-reported |
| Press wires / GDELT | All | Deal facts, PROOF | — | RSS / GDELT | Wires restrictive; GDELT permissive [SECONDARY] | Real-time | Varies |
| Firm websites | All | Ticket, sector, stage, fund size | — | HTML | Site-specific | Ad hoc | Marketing claims, may be stale |

### Gaps
- PR Newswire terms were not checked.
- GDELT's own terms page was not fetched.
- OpenVC's terms of service could not be found.
- I did not survey current GitHub investor lists or their licences beyond the Kaggle Crunchbase snapshot.

---

## 6. Angels and large private investors (ACA, EBAN, AngelList, crowdfunding platforms)

### Takeaway
Public data on individual angels is thin and mostly at the network level. EBAN and ACA publish organisation directories (angel groups, networks, platforms), but individual members are not listed. AngelList data is publicly visible but has no documented open-reuse path. Crowdfunding regulators (SEC Form C, the ESMA ECSP register) identify platforms and issuers, not individual investors. Large private investors (family offices) surface mainly through 13F, 13D/G and Form D related-person roles, plus press.

### Cited Findings
- EBAN:
  - Public membership directory by country and type; "over 100 member organizations". — [EBAN Membership Directory](https://eban.org/membership-directory)
  - EBAN's 2023 data report counted 358 active business angel networks or federations in 37 countries. — [EBAN Data Report 2023](https://www.eban.org/2023/12/01/) **[PRE-2024]**
- Angel Capital Association:
  - The public directory covers angel groups, accredited platforms and affiliated organisations. The fuller directory is members-only, and "individual members are not listed for privacy reasons". — [ACA Member Directory](https://angelcapitalassociation.org/directory/)
  - An ACA overview cited more than 15,000 individual investors. — [ACA Membership Overview 2022](https://www.angelcapitalassociation.org/data/Documents/Membership/ACA_Membership_Overview_080422.pdf?rev=3511) **[PRE-2024]**
- AngelList:
  - Paid scrapers and datasets exist. Vendors note that "AngelList scraping tools are likely to be blocked". — [Coresignal](https://coresignal.com/data-sources/angellist) **[SECONDARY]**; [Oxylabs](https://oxylabs.io/products/scraper-api/web/angellist) **[SECONDARY]**
  - AngelList's own ToS was not found.
- Crowdfunding: see §1 for SEC Form C data sets (2016Q2–2026Q3) and §3 for the ESMA ECSP register. — [SEC Crowdfunding Data Sets](https://www.sec.gov/data-research/sec-markets-data/crowdfunding-offerings-data-sets); [FMA: ESMA register of CSPs](https://www.fma.gv.at/en/financial-service-providers/crowdfunding-service-providers/authorised-crowdfunding-services-providers-in-europe/)

### Inferences
- **Model angel networks as organisation records.** Treat angel networks and groups (EBAN, ACA, national federations) as "angel network" investor records. Individual angels should enter only with an independent public PROOF: a named participation in a press release, a company filing (e.g. a Companies House allotment or PSC), a Form D related-person role, or the angel's own public profile. Each individual record then raises GDPR issues (see §7).
- **Family offices via 13F/13D.** Large US family offices that file 13F or 13D/G can be identified with a dated public source. Their private-market activity still needs press or Form D evidence, and Form D lists them only when they are an officer or director of the issuer.

### Gaps
- No usable public bulk source of individual angel investors was found.
- AngelList and crowdfunding-platform (Crowdcube, Seedrs, Republic, StartEngine) ToS on reuse were not reviewed.
- Current (2025–26) EBAN and ACA member counts from primary sources were not found.

---

## 7. Legal: scraping, reuse and GDPR (LinkedIn, Crunchbase, natural-person angels)

### Takeaway
Contractual bans on scraping are explicit for LinkedIn (User Agreement §8.2, effective 3 Nov 2025) and Crunchbase (ToS of 30 Sep 2026). Government registers (SEC, Companies House, GLEIF CC0) are the low-risk core. For EU natural-person angels, "publicly available" does not equal lawful. The Dutch DPA (May 2024) called scraping of personal data "almost always" a GDPR violation and read legitimate interest narrowly. Natural-person records therefore need a documented legitimate-interest assessment, data minimisation and Art. 14 notice, or should be excluded.

### Cited Findings
- LinkedIn User Agreement §8.2 ("Don'ts"), effective **3 Nov 2025**:
  - users may not "scrape or copy the Services, including profiles and other data from the Services"
  - users may not "copy, use, display or distribute any information… obtained from the Services"
  - users may not "use bots or other unauthorized automated methods to access the Services"

  — [LinkedIn User Agreement](https://www.linkedin.com/legal/user-agreement)
- Crunchbase ToS (30 Sep 2026) prohibits crawling and scraping, automated export, storing significant portions of content and AI training; see §5. — [Crunchbase Terms of Service](https://about.crunchbase.com/terms-of-service/)
- Dutch Autoriteit Persoonsgegevens guidance (1 May 2024):
  - Scraping personal data is "almost always a violation of the GDPR".
  - A legitimate interest must be shown even for public data.
  - The AP took the narrow view that "purely commercial interests" do not qualify; commentators note this position is under review.

  — [Pinsent Masons Out-Law](https://www.pinsentmasons.com/out-law/news/dutch-web-scraping-guidance-warn-businesses-gdpr-breach-risk); [IAPP](https://iapp.org/news/a/netherlands-dpa-issues-guidance-against-web-scraping)
- EDPB Guidelines 03/2026 on scraping for generative-AI training: consent is "generally not a viable legal basis" for scraping at scale, and legitimate interest requires the three-part test. — [Reed Smith summary](https://www.reedsmith.com/our-insights/blogs/technology-law-dispatch/102nbqu/edpb-web-scraping-guidelines-for-ai-making-the-impossible-possible/) **[SECONDARY]**
- GLEIF data is CC0, with conditions on endorsement and circumvention plus liquidated damages. — [GLEIF Terms](https://www.gleif.org/en/meta/lei-data-terms-of-use)
- OpenCorporates is ODbL share-alike, and commercial users are not free Permitted Users. — [OpenCorporates ToU](https://opencorporates.com/terms-of-use-2/)
- SEC EDGAR data is free to access, but botnets and crawling are banned and requests are capped at 10 per second. — [SEC Accessing EDGAR Data](https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data)

### Inferences
- **Lowest legal risk:** SEC bulk data sets, Companies House bulk and API, GLEIF, ESMA CSV exports and LP disclosures published by public bodies (public-records data).
- **Medium risk:**
  - firms' own websites (organisation-level facts; check ToS and robots.txt)
  - GDELT-indexed news with fact extraction only
- **Avoid without a licence:** LinkedIn, Crunchbase (including free and Basic), AngelList scraping and OpenCorporates for commercial use.
- **Natural-person investors (EU/UK GDPR)** **[UNVERIFIED legal specifics; get counsel]**:
  - Rely on Art. 6(1)(f) legitimate interest with a documented balancing test.
  - Collect only professional-capacity data (name, role, investing entity, public source URL and date). No personal contact details or home addresses.
  - Provide Art. 14 notice to data subjects when data is not collected from them, and honour objections (Art. 21).
  - Prefer modelling the investing *vehicle* (company, fund, syndicate) over the individual.
  - Enforcement precedent exists for failing to give Art. 14 notice to people whose public-register data was reused commercially (the Polish UODO / Bisnode case, 2019) **[PRE-2024; not verified this session]**.
- **US filings and individuals:** natural persons named in US filings (Form D related persons, ADV control persons) are public records. Their reuse is not GDPR-governed unless the database operator is in the EU or targets EU data subjects.

### Gaps
- The text of the AP guidance and EDPB Guidelines 03/2026 were not read in primary form.
- UK ICO guidance on scraping and on the legitimate-interest test was not reviewed.
- AngelList, PR Newswire, GlobeNewswire and OpenVC terms remain unverified.
- No formal legal opinion was obtained on the CC-BY status of "Crunchbase Basic" in light of the ToS anti-scraping clauses.
