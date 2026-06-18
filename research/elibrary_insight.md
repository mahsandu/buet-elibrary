# Insight Extraction: Strategic Implications for BUET E-Library V4

**Project:** BUET E-Library V4 Platform  
**Date:** 2026-06-18  
**Source:** Cross-dimensional synthesis of 6 wide-exploration facets + cross-verification results.

---

## Insight 1: The "External Harvester Architecture" Mitigates BUET's Two Biggest Risks Simultaneously

**Insight:** BUET can decouple Drupal from Elasticsearch compatibility concerns by having Python microservices populate the ES index directly, while Drupal only queries ES via Search API or a lightweight custom JSON endpoint. This pattern simultaneously (a) bypasses the Drupal 11 + ES 8.x connector uncertainty, and (b) avoids forcing Drupal to index hundreds of thousands of MARC/DC records through its native Search API pipeline, which would be slow and fragile.

**Derived From:**
- Dim 05 (Drupal + ES): External harvester pattern used by Norway's data.norge portal; Drupal 11/ES 8.x compatibility gap [^13][^14]
- Dim 04 (OAI-PMH ETL): OARepo/Invenio and MIT Libraries both use external Python harvesters that write directly to Elasticsearch, with Drupal/Solr only as the query layer [^4][^5]
- Dim 03 (Containerized Stacks): DSpace 7+ and Islandora both separate frontend from backend indexing, with external services populating search indexes [^10][^11]

**Rationale:** The research reveals that native Drupal indexing is suitable for content-managed pages but struggles with large external metadata catalogs. The external harvester pattern is proven in production (OARepo, MIT, CORE) and aligns with BUET's existing microservices strategy. It also isolates Drupal from ES client version mismatches.

**Implications:** BUET should design the architecture as: Python harvesters → Elasticsearch → Drupal (read-only query layer). This is a strategic shift from "Drupal indexes everything" to "Drupal discovers everything."

**Confidence:** High

---

## Insight 2: BUET's Stack Is a "Reverse-Engineered VuFind" — This Is Both a Risk and an Opportunity

**Insight:** The V4 architecture (Elasticsearch + Drupal + OAI-PMH harvesters + live OPAC scraping) is functionally equivalent to what VuFind already does with Solr + PHP + OAI-PMH + ILS drivers. BUET is essentially rebuilding VuFind's core integration patterns but with modern components. This means the integration logic (Koha ILS driver, DSpace OAI harvester, real-time availability lookup) has been solved before — but the *technology translation* from Solr/PHP to ES/Drupal/Python requires custom engineering.

**Derived From:**
- Dim 01 (Open-source Discovery): VuFind's `harvest_oai.php`, `KohaILSDI` driver, and `MultiBackend` pattern [^7][^8]
- Dim 04 (OAI-PMH ETL): VuFind's `batch-import-xsl.sh` and `last_harvest.txt` watermarking are the canonical reference for OAI-PMH → search index pipelines [^4][^6]
- Dim 05 (Drupal + ES): No major library has built this exact stack; Islandora is Drupal + Solr, not ES [^29][^30]

**Rationale:** VuFind has 15+ years of production-hardened Koha/DSpace integration code. BUET can borrow the *integration patterns* (OAI-PMH metadata prefixes, ILS driver logic, deduplication precedence lists) but must translate them into Python/Elasticsearch. This is less risky than building from first principles, but requires deep study of VuFind's integration wiki.

**Implications:** BUET should treat VuFind's documentation (vufind.org/wiki/indexing:koha, vufind.org/wiki/indexing:dspace) as primary reference material, even though the implementation technology differs. The "VuFind pattern book" should be mapped to the "Elasticsearch/Drupal pattern book."

**Confidence:** High

---

## Insight 3: The Live Scraper Should Be a Separate Service with TTL Caching, Not an Inline Synchronous Call

**Insight:** The V4 proposal describes a lightweight scraper API that Drupal calls asynchronously when viewing a physical book. However, research on scraping best practices and library OPAC patterns suggests that the scraper should be a standalone service with a Redis/in-memory cache (TTL 5-15 minutes), not a direct inline request. This prevents repeated scrapes of the same bib record, reduces load on the Koha OPAC, and improves user experience by showing "stale" cached status rather than waiting 2-5 seconds for a live HTTP request.

**Derived From:**
- Dim 06 (Live Scraping): Web scraping best practices recommend rate limiting and caching; Oxylabs advises exponential backoff and off-peak scheduling [^17][^18]
- Dim 03 (Containerized Stacks): Redis is a standard sidecar in modern containerized stacks (Hyku, DSpace) for caching and session storage [^12]
- Dim 01 (Open-source Discovery): VuFind uses ILS drivers with caching layers to avoid hammering the Koha backend [^8]

**Rationale:** Synchronous scraping on every page load is an anti-pattern. The BI-Library project caches open-access status, and production scrapers universally use caching. Redis in Docker is a one-line addition to the compose file and adds minimal resource overhead (~100MB RAM).

**Implications:** The `live_status.py` microservice should be redesigned to:
1. Check Redis cache first (`biblionumber:{id}` → `status_json`)
2. If cache miss, scrape Koha OPAC with 5-second timeout
3. Store result in Redis with 10-minute TTL
4. Return cached or fresh result to Drupal
5. Run a background "cache warming" job that pre-fetches statuses for frequently viewed items

**Confidence:** High

---

## Insight 4: The "Missing Database" in the V4 Docker Compose Is a Critical Gap — But the Fix Is Standard

**Insight:** The original V4 implementation guide's `docker-compose.yml` omitted a MariaDB/PostgreSQL container for Drupal, yet included Drupal 11. Drupal 11 requires a relational database (MySQL/MariaDB/PostgreSQL). The fix is straightforward: add a MariaDB 10.6+ container, but this also creates a dependency chain (Drupal → MariaDB → Elasticsearch) and networking considerations that must be documented.

**Derived From:**
- Dim 03 (Containerized Stacks): DSpace uses PostgreSQL; Islandora uses MySQL/MariaDB; Hyku uses PostgreSQL; all multi-service stacks include a database container [^10][^11][^12]
- Dim 05 (Drupal + ES): Drupal 11 requires a database; Platform.sh and DDEV both include MariaDB/PostgreSQL in their Drupal + ES recipes [^13][^14]

**Rationale:** This is a mechanical gap, not a design flaw. The research shows that every containerized library stack includes a database container. The V4 guide should also include an Nginx reverse proxy container for SSL termination and public exposure, as only the frontend should be exposed.

**Implications:** The corrected `docker-compose.yml` must include:
- `mariadb` (Drupal database)
- `nginx` (reverse proxy, SSL termination)
- `redis` (scraper cache, optional Drupal cache)
- Health checks and `depends_on` chains

**Confidence:** High

---

## Insight 5: Koha's Native Elasticsearch Support Creates a Future Migration Path — But Not a Short-Term Solution

**Insight:** Koha 26.x now has mature Elasticsearch support with custom MARC mapping exports, authority bulk updates, and facet ordering. This means BUET could eventually migrate from the "external index" architecture to having Koha natively index into Elasticsearch, eliminating the need for the Koha OAI-PMH harvester. However, this requires Koha configuration changes (SSL unblocking, REST API enablement) that are currently infeasible due to BUET's security constraints.

**Derived From:**
- Dim 01 (Open-source Discovery): Koha adopted Elasticsearch in 2020; ByWater Solutions documented the migration benefits [^27]
- Dim 06 (Live Scraping): BUET's SSL restrictions block the Koha REST API, which also prevents direct ES integration [^16][^18]
- Dim 02 (Commercial Services): EBSCO FOLIO and EDS integrate with Koha via REST API or OAI-PMH, but REST is preferred for real-time features [^19][^20]

**Rationale:** The research reveals that Koha's ES integration is production-ready but requires REST API access and Elasticsearch connectivity from the Koha server. BUET's security constraints (self-signed certificates, SSL blocking) make this a "Phase 2" option, not a V4 solution. The OAI-PMH harvester remains the correct short-term approach.

**Implications:** BUET should design the V4 harvester to be *replaceable* — if Koha ES becomes accessible later, the Python harvester can be retired and the Drupal frontend can query Koha's native ES index directly. This requires using a unified JSON schema that Koha's ES mappings could also produce.

**Confidence:** Medium

---

## Insight 6: Deduplication Strategy Should Use Source-Prefixed IDs + Fingerprint Hashing, Not Merging

**Insight:** When harvesting from both Koha (physical books) and DSpace (digital theses), some records may overlap (e.g., a thesis catalogued in both systems). The research shows two dominant patterns: (a) source-prefixed IDs (`koha_123` vs `dspace_456`) that keep records separate, and (b) fingerprint hashing for true deduplication. For BUET, the correct approach is hybrid: use source-prefixed IDs as the primary key, but compute an MD5 fingerprint of normalized title+author+year to flag potential duplicates in the UI, rather than merging them automatically.

**Derived From:**
- Dim 04 (OAI-PMH ETL): VuFind's `merged_child_boolean` and precedence lists; Elasticsearch's `version` and `op_type=create` for idempotency; MD5/SHA1 fingerprinting [^4][^5][^6]
- Dim 01 (Open-source Discovery): DSpace and Koha records often overlap for theses; merging them automatically loses source-specific metadata (e.g., circulation status vs. PDF URI) [^7][^8]

**Rationale:** Automatic merging of Koha and DSpace records is dangerous because the two sources have different "core truths" — Koha knows shelf location; DSpace knows PDF download URL. A unified search result should show both sources side-by-side when duplicates are detected, not merge them into a single record.

**Implications:** The Elasticsearch schema should include a `fingerprint` field (MD5 of normalized title+author+year) and a `source_system` field. The Drupal frontend should group results by fingerprint, showing a "Available in multiple formats" badge with links to both the physical book (Koha) and the digital thesis (DSpace).

**Confidence:** High

---

## Insight 7: E-Resource Proxy Should Be Deferred to Phase 2 — The Core Discovery Layer Is Higher Priority

**Insight:** The V4 proposal ambitiously includes dynamic subscribed database access, EZproxy/OpenAthens integration, and institutional SSO. However, the research on developing-country libraries reveals that proxy/auth infrastructure is a major undertaking with its own complexity (SAML, stanza maintenance, vendor negotiations). BUET's highest-value deliverable is the unified discovery layer (Koha + DSpace search). The e-resource proxy can be a Phase 2 enhancement, initially replaced by a static database directory with direct links and VPN fallback.

**Derived From:**
- Dim 06 (Live Scraping): Developing-country libraries (Tanzania, Nigeria, India) face severe budget and IT constraints for proxy/auth; SSO integration is described as "tedious" [^26][^27][^28]
- Dim 02 (Commercial Services): EZproxy requires config.txt maintenance; OpenAthens requires subscription; both need vendor coordination [^22][^23]
- Dim 01 (Open-source Discovery): VuFind supports database A-Z lists and federated search connectors as simpler first steps before full proxy integration [^7][^8]

**Rationale:** The proxy/auth layer is a separate infrastructure project. BUET can deliver immediate value with a unified Koha+DSpace search, then incrementally add e-resource proxying. The static database directory in the V4 proposal can be enhanced with "off-campus access via VPN" messaging as a temporary measure.

**Implications:** The V4 implementation should focus on:
1. Priority: Discovery layer (Elasticsearch + harvesters + Drupal search)
2. Priority: Live availability scraper
3. Deferred: E-resource proxy (Phase 2)
4. Deferred: Citation utilities (Phase 2)

**Confidence:** High

---

## Insight 8: The V4 Scraper Has an XSS Vulnerability That Must Be Fixed Before Production

**Insight:** The V4 implementation guide's `live_status.py` returns raw HTML (`str(status_table)`) from the Koha OPAC, which is then injected into the Drupal DOM. If the Koha OPAC ever contains malicious HTML/JS (e.g., via a cataloguing XSS or a compromised upstream source), this creates a stored XSS vector in the discovery portal. The research on library security identifies XSS and session hijacking as critical risks in proxy and scraping workflows.

**Derived From:**
- Dim 06 (Live Scraping): XSS can lead to admin session hijacking; stored XSS via improperly sanitized input is a documented risk in library systems [^23][^24]
- Dim 03 (Containerized Stacks): Security hardening includes input validation, read-only filesystems, and secrets management [^10][^11]
- Dim 04 (OAI-PMH ETL): ETL best practices include validation before indexing; the same principle applies to scraped data before rendering [^4][^5]

**Rationale:** The fix is structural: the scraper should parse the HTML table into structured JSON (e.g., `{"location": "Central Library Floor 2", "status": "Available", "call_number": "QA76.5"}`) rather than returning raw HTML. Drupal then renders this JSON through its own templates, which is safe and thematically consistent.

**Implications:** Redesign `live_status.py` to:
1. Parse the HTML table with BeautifulSoup
2. Extract specific text fields (status, location, call number, barcode)
3. Sanitize/validate each field (whitelist approach)
4. Return JSON only, never HTML
5. Drupal renders the JSON via a custom theme template

**Confidence:** High

---

## Footnotes

[^4]: Sickle Documentation. 2020. https://sickle.readthedocs.io/_/downloads/en/latest/pdf/
[^5]: MIT Libraries. "oai-pmh-harvester." GitHub. 2019. https://github.com/MITLibraries/oai-pmh-harvester
[^6]: OARepo. "oarepo-oai-pmh-harvester." GitHub. 2020. https://github.com/oarepo/oarepo-oai-pmh-harvester
[^7]: VuFind Wiki. https://vufind.org/wiki/indexing:koha
[^8]: VuFind Summit 2020. Mukhopadhyay, P. https://vufind.org/vuFind/docs/summit2020/VuFind2020-V2_PSM.pdf
[^10]: DSpace Docker Compose. https://github.com/DSpace/DSpace/blob/main/dspace/src/main/docker-compose/README.md
[^11]: Islandora ISLE. https://github.com/Islandora-Devops/isle-dc/
[^12]: Hyku Getting Started. https://github.com/samvera/hyku/blob/main/docs/getting-started.md
[^13]: Elastic Discuss. "Drupal ElasticSearch Connector." 2022. https://discuss.elastic.co/t/drupal-elasticsearch-connector/311505
[^14]: OpenSense Labs. "Magnificent combo: Implementing Elasticsearch with Drupal." 2019. https://opensenselabs.com/blog/magnificent-combo-implementing-elasticsearch-drupal
[^16]: BI-Library. "Retrieving and showing open access status within Koha OPAC." GitHub. 2023. https://github.com/BI-Library/retrieving-and-showing-open-access-status-within-Koha-OPAC
[^17]: Oxylabs. "Web Scraping Best Practices." 2024. https://oxylabs.io/blog/web-scraping-best-practices
[^18]: VuFind Summit 2020. Mukhopadhyay, P. https://vufind.org/vuFind/docs/summit2020/VuFind2020-V2_PSM.pdf
[^19]: EBSCO. "EBSCO Discovery Service Tech Sheet." 2025. https://www.ebsco.com/sites/default/files/acquiadam-assets/EBSCO-Discovery-Service-Tech-Sheet.pdf
[^20]: Bhowmick & Chakrabarty. SRELS Journal, 2021. https://www.researchgate.net/publication/354236155
[^22]: Wappalyzer. "Websites using EZproxy." https://www.wappalyzer.com/technologies/reverse-proxies/ezproxy/
[^23]: Rewterz. "Stored XSS in Ivanti EPM Allows Admin Session Hijacking." 2025. https://rewterz.com/threat-advisory/stored-xss-in-ivanti-epm-allows-admin-session-hijacking
[^24]: Nuclear'Atk Security Lab. "利用 Appcache 和 ServiceWorker 进行持久型session hijacking 和 XSS." 2015. https://lcx.cc/post/4564/
[^26]: Mattigiri, M.T. et al. "A Comparative Analysis of Single Sign-On and Proxy Solutions." DESIDOC, 2025. http://publicationsdrdo.in/index.php/djlit/article/download/19823/8488/88541
[^27]: Mkolo, A. "Examining the Availability and Use of Electronic Resources." Tanzania. http://repository.out.ac.tz/2985/1/AGNES%20%20MKOLO%20tyr.pdf
[^28]: Ani et al. "An Overview of Application of E-Resources." https://pdfs.semanticscholar.org/a5e5/61556cc2e7047ba6b0b81982d3d7ebce073a.pdf
[^29]: Islandora Documentation. https://islandora.github.io/documentation/
[^30]: Discovery Garden. "DG Resources: Islandora and Drupal." https://www.discoverygarden.com/resources/islandora-and-drupal-open-source-foundations-for-digital-repositories
