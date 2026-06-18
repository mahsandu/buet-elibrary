# Cross-Verification: International E-Library Platforms & Reference Architectures

**Project:** BUET E-Library V4 Platform  
**Date:** 2026-06-18  
**Scope:** Synthesis of 6 wide-exploration facets covering open-source discovery, commercial services, containerized stacks, OAI-PMH ETL, Drupal+ES integration, and live scraping/auth patterns.

---

## High Confidence Findings (Confirmed by ≥2 independent sources)

### 1. Elasticsearch is the modern distributed search engine of choice for non-library sectors, but the library ecosystem is overwhelmingly Solr-centric.
- **Evidence:** VuFind, Blacklight, Aspen, DSpace, and Islandora all use Solr. Elasticsearch is used in academic publishing platforms, college search portals, and enterprise search. [^1][^2][^3]
- **Implication for BUET:** BUET's choice of Elasticsearch is unconventional for library discovery but offers superior REST API ergonomics and containerization. Custom indexing pipelines must be built rather than using off-the-shelf SolrMarc/VuFind harvesters.

### 2. OAI-PMH is the universal interoperability protocol for bulk metadata harvesting in academic libraries.
- **Evidence:** DSpace, Koha, EPrints, Fedora, and all major discovery platforms (VuFind, Primo, EDS, WorldCat) support OAI-PMH. Sickle (Python) and phpoaipmh (PHP) are the dominant harvester libraries. [^4][^5][^6]
- **Implication for BUET:** The OAI-PMH harvesting strategy in the V4 proposal is architecturally sound and follows global best practices.

### 3. VuFind is the most widely adopted open-source discovery layer globally, especially in developing countries.
- **Evidence:** 200+ institutions, SourceForge #1 download ranking, 8 Indian implementations (N-List, INFLIBNET, Calcutta University), LAMP-stack compatibility with Koha/DSpace. [^7][^8][^9]
- **Implication for BUET:** VuFind is the proven reference architecture for Koha + DSpace integration. BUET's custom Drupal + ES stack is a deliberate divergence that trades proven integration for modern stack flexibility.

### 4. Containerization is now the default deployment model for new digital repository installations.
- **Evidence:** DSpace 7+ provides Docker Compose files, Islandora ISLE is fully containerized, Hyku offers Docker Compose + Kubernetes Helm charts, FOLIO is Kubernetes-native. [^10][^11][^12]
- **Implication for BUET:** The Docker Compose approach in the V4 proposal aligns with modern best practices. However, DSpace's official Docker images are explicitly labeled "not production-ready" by the core team.

### 5. Drupal + Elasticsearch integration requires the Search API + Elasticsearch Connector stack, but ES 8.x compatibility with Drupal 11 is a known risk area.
- **Evidence:** Elasticsearch Connector historically lagged behind ES releases; ES 8.x removed mapping types and changed security defaults; no major library-specific Drupal distribution bundles ES out-of-the-box. [^13][^14][^15]
- **Implication for BUET:** Immediate prototyping of Drupal 11 + Elasticsearch 8.x is required before full commitment. An external harvester architecture (Python populates ES, Drupal queries it) may be safer than native Drupal indexing.

### 6. Live OPAC scraping is a legitimate engineering fallback when APIs are unavailable, but requires careful rate limiting and error handling.
- **Evidence:** BI-Library project scrapes Koha OPAC for open-access status; web scraping best practices include random delays, exponential backoff, User-Agent rotation, and off-peak scheduling. [^16][^17][^18]
- **Implication for BUET:** The HTTP DOM parsing strategy is viable but fragile. A caching layer and CSS selector monitoring should be implemented to handle Koha HTML changes.

### 7. Commercial discovery services (Primo, EDS, WorldCat) are prohibitively expensive for many developing-country institutions.
- **Evidence:** Pricing ranges from $30,000–$60,000+/year for mid-sized institutions; Indian universities report EDS costs exceeding ~$25,000/year; SPARC raised antitrust concerns about Clarivate-ProQuest consolidation. [^19][^20][^21]
- **Implication for BUET:** Self-hosted open-source stacks are the only economically viable path for BUET. The V4 proposal's decision to build a custom platform is validated by global cost data.

### 8. EZproxy remains the dominant commercial proxy solution, but OpenAthens is rapidly replacing it at major institutions.
- **Evidence:** 3,600+ EZproxy sites globally; UBC, Harvard, MSU, Delaware all migrating to OpenAthens; OpenAthens is cloud-managed SaaS with no server maintenance; Shibboleth is open-source but complex. [^22][^23][^24]
- **Implication for BUET:** A self-hosted EZproxy or minimalist nginx reverse proxy may be the most budget-appropriate path. OpenAthens SaaS subscription should be evaluated against total cost of ownership.

---

## Medium Confidence Findings (Single authoritative source or strong inference)

### 9. FOLIO is gaining traction as a next-generation Library Services Platform but is not a discovery layer itself.
- **Evidence:** Durban UT (first South African adopter), Cornell, Stanford, CU Boulder, Chalmers. FOLIO is K8s-native with modular microservices (Inventory, ERM, Codex). [^25][^26]
- **Confidence:** Medium — FOLIO adoption is still early in the Global South and requires significant IT expertise.

### 10. Koha now has native Elasticsearch support (since 2020), with ongoing improvements in version 26.x.
- **Evidence:** ByWater Solutions announced Koha ES adoption in 2020; Koha 26.05.00 includes ES mapping exports, custom MARC field indexing, and authority bulk updates. [^27][^28]
- **Confidence:** Medium — While documented, the ES integration is optional and many production Koha instances still use Zebra. BUET's specific SSL/API constraints may still prevent direct ES use.

### 11. Islandora 8+ uses Drupal + Fedora + Solr, making it the closest existing reference for a Drupal-based library stack.
- **Evidence:** Islandora ISLE is fully containerized with Drupal as the CMS layer; however, it remains Solr-first with no official Elasticsearch module. [^29][^30]
- **Confidence:** Medium — Adapting Islandora to ES would require custom module development.

---

## Low Confidence / Conflict Zone Findings

### 12. Open-source discovery TCO vs. commercial SaaS: Are hidden labor costs higher than vendor subscriptions?
- **Conflict:** Penn State and ECU documented significant hidden costs (MARC cleanup, server maintenance, Rails/PHP dependency management, ~6 extra servers). However, for developing-country institutions where commercial options cost $25K+/year, open-source is the only viable path regardless of labor cost. [^31][^32]
- **Resolution:** The conflict is context-dependent. For BUET, open-source is the only viable option due to budget constraints, but the maintenance burden must be explicitly modeled and staffed.

### 13. Is Drupal 11 + Elasticsearch 8.x a production-ready combination?
- **Conflict:** Some Drupal agencies claim ES 8.x works with Search API; others report compatibility gaps and module lag. The Elasticsearch Connector module's maintainer activity is sporadic. [^13][^14]
- **Resolution:** This requires immediate hands-on prototyping. The external-harvester pattern (Python writes to ES, Drupal reads via custom module) mitigates this risk by decoupling Drupal from ES client compatibility.

---

## Research File References

- `elibrary_wide01.md` — Open-source Discovery Platforms (VuFind, Blacklight, FOLIO, Aspen)
- `elibrary_wide02.md` — Commercial Discovery Services (Primo, EDS, WorldCat, EZproxy, OpenAthens)
- `elibrary_wide03.md` — Containerized Repository & Discovery Stacks (DSpace, Samvera, Islandora, Fedora)
- `elibrary_wide04.md` — OAI-PMH Harvesting & ETL Architectures (Sickle, phpoaipmh, scheduling, deduplication)
- `elibrary_wide05.md` — Drupal + Elasticsearch Integration (Search API, Facets, ES 8.x risks, Islandora pattern)
- `elibrary_wide06.md` — Live OPAC Scraping & E-Resource Authentication (BeautifulSoup, Playwright, EZproxy, OpenAthens, Shibboleth)

---

## Footnotes

[^1]: Elasticsearch vs. Solr: What Developers Need to Know in 2025. Last9.io. 2025-03-07. https://last9.io/blog/elasticsearch-vs-solr/
[^2]: Roy, B.K. et al. "Discovery Layer in Library Retrieval: VuFind as an Open Source Service." JISTAP, 2022. https://accesson.kr/jistap/v.10/4/3/27622
[^3]: Semantic Scholar. "An Analysis on the Comparison of Solr and Elasticsearch." https://pdfs.semanticscholar.org/9e27/e6b9afc7a2632b23c566d8bb19e7b44b4688.pdf
[^4]: Sickle Documentation. 2020. https://sickle.readthedocs.io/_/downloads/en/latest/pdf/
[^5]: phpoaipmh GitHub. https://github.com/caseyamcl/phpoaipmh
[^6]: OAI-PMH Harvesting - EIFL. https://www.eifl.net/system/files/resources/201907/repositories_checklist_july_2019__0.pdf
[^7]: VuFind Wiki. https://vufind.org/wiki/community:installations
[^8]: Chickering, F.W. & Yang, S.Q. "Evaluation and Comparison of Discovery Tools." ITAL, 2014. https://ital.corejournals.org/index.php/ital/article/download/3471/pdf_1/10968
[^9]: Bhowmick, A. & Chakrabarty, B. "Integration of Open-Source Software with Library Discovery System (VuFind)." SRELS, 2021. https://www.researchgate.net/publication/354236155
[^10]: DSpace Docker Compose. https://github.com/DSpace/DSpace/blob/main/dspace/src/main/docker-compose/README.md
[^11]: Islandora ISLE. https://github.com/Islandora-Devops/isle-dc/
[^12]: Hyku Getting Started. https://github.com/samvera/hyku/blob/main/docs/getting-started.md
[^13]: Elastic Discuss. "Drupal ElasticSearch Connector." 2022. https://discuss.elastic.co/t/drupal-elasticsearch-connector/311505
[^14]: OpenSense Labs. "Magnificent combo: Implementing Elasticsearch with Drupal." 2019. https://opensenselabs.com/blog/magnificent-combo-implementing-elasticsearch-drupal
[^15]: Elastic.co. "Elasticsearch 8.0.0 Release Notes." https://www.elastic.co/guide/en/elasticsearch/reference/8.18/release-notes-8.0.0.html
[^16]: BI-Library. "Retrieving and showing open access status within Koha OPAC." GitHub. 2023. https://github.com/BI-Library/retrieving-and-showing-open-access-status-within-Koha-OPAC
[^17]: Oxylabs. "Web Scraping Best Practices." 2024. https://oxylabs.io/blog/web-scraping-best-practices
[^18]: VuFind Summit 2020. Mukhopadhyay, P. "VuFind and Koha integration." https://vufind.org/vuFind/docs/summit2020/VuFind2020-V2_PSM.pdf
[^19]: Bill Denton. "How much do web-scale discovery services cost?" 2011. https://www.miskatonic.org/2011/11/09/how-much-do-web-scale-discovery-services-libraries-cost/
[^20]: Bhowmick & Chakrabarty. SRELS Journal, 2021. https://www.researchgate.net/publication/354236155
[^21]: SPARC. "Opposing the Merger Between Clarivate and ProQuest." FTC Letter, 2021. https://sparcopen.org/wp-content/uploads/2021/10/SPARC-FTC-Letter-in-Opposition-to-the-Clarivate-ProQuest-Merger.pdf
[^22]: Wappalyzer. "Websites using EZproxy." https://www.wappalyzer.com/technologies/reverse-proxies/ezproxy/
[^23]: UBC Library. "OpenAthens transforms user access." 2021. https://about.library.ubc.ca/2021/06/02/openathens-transforms-user-access-to-library-resources/
[^24]: ALA / OpenAthens. "What Is the Difference between Shibboleth and OpenAthens?" https://alatest.pkpps03.publicknowledgeproject.org/index.php/ltr/article/download/7849/10935
[^25]: FOLIO. https://folio.org/
[^26]: EBSCO. "EBSCO FOLIO Overview." 2025. https://www.ebsco.com/sites/default/files/acquiadam-assets/EBSCO-FOLIO-Overview.pdf
[^27]: ByWater Solutions. "Koha Adopts Elastic for Search." 2020. https://bywatersolutions.com/news/koha-adopts-elastic-for-search-functionality
[^28]: Koha 26.05.00 Release Notes. 2026-05-27. https://koha-community.org/en/koha-26-05-00-released/
[^29]: Islandora Documentation. https://islandora.github.io/documentation/
[^30]: Discovery Garden. "DG Resources: Islandora and Drupal." https://www.discoverygarden.com/resources/islandora-and-drupal-open-source-foundations-for-digital-repositories
[^31]: Tillman, R.K. "Maintenance, Labor, and the Classic Catalog." 2019. https://ruthtillman.com/talk/maintenance-labor-classic/
[^32]: Barber, M. "Customizing an Open Source Discovery Layer at East Carolina University." LRTS, 2017. https://journals.ala.org/lrts/article/view/6039/7738
