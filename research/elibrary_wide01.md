## Facet: Open-source Discovery Platforms

### Key Findings
- The major open-source discovery platforms are **VuFind** (PHP/Apache Solr/LAMP), **Blacklight** (Ruby on Rails/Apache Solr), **Aspen Discovery** (PHP/Solr, forked from VuFind), and **eXtensible Catalog** (XC). FOLIO is not a discovery layer but a full Library Services Platform (LSP) with modular microservices architecture. [^1][^2][^3]
- **VuFind integrates with Koha** primarily via **OAI-PMH** for harvesting bibliographic records into its Solr index, and via **ILS drivers** (Koha driver, KohaILSDI driver, REST API, or MultiBackend driver) for real-time item status, holds, and patron authentication. [^4][^5][^6]
- **VuFind integrates with DSpace** through **OAI-PMH** metadata harvesting; DSpace exposes Dublin Core or MARC metadata via OAI, which VuFind harvests, transforms, and indexes into Solr. [^7][^8]
- **Blacklight** is architecturally different from VuFind: it is a **Ruby on Rails engine** rather than a standalone PHP application. It provides a more minimal, highly customizable "skeleton" framework where most advanced features must be built locally. [^9][^10]
- **FOLIO** is a **cloud-native, microservices-based Library Services Platform** built on Kubernetes, Vert.x, and PostgreSQL. It is not a discovery layer itself but a backend platform that can interoperate with discovery layers (e.g., EBSCO Discovery Service, VuFind). Its core abstraction layer is **Codex**, which unifies metadata across formats. [^11][^12][^13]
- **Containerized deployments** exist for VuFind (Docker support is documented, and a community Docker image exists: `dainst/vufind-docker`), and Blacklight-based stacks are increasingly dockerized (e.g., Temple University's Rails + Blacklight + Postgres + Solr setup). FOLIO itself is designed for Kubernetes/container orchestration. [^14][^15][^16]
- **Customization and maintenance burden** for open-source discovery layers is significant. East Carolina University reported that implementing VuFind required extensive MARC mapping cleanup, cataloging error remediation, and many hours of development to match existing OPAC features. Blacklight is even more "barebones" and requires substantial local development to reach feature parity with VuFind. [^17][^18]
- **In developing countries / South Asia**, VuFind is the most widely adopted open-source discovery layer due to its LAMP stack compatibility with Koha and DSpace. India has multiple implementations (e.g., N-List, INFLIBNET, Calcutta University model). The cost of commercial systems (e.g., EDS at ~$25,000/year) makes open-source alternatives essential. [^19][^20][^21]
- **Three generations of Koha-VuFind connectivity** have emerged: (1) direct database calls, (2) ILS-DI protocol-based connections, and (3) REST API + OAuth2-based interactions via the MultiBackend driver. The REST approach is the most secure and scalable, especially for union catalogues. [^5][^6]
- **Aspen Discovery** (forked from VuFind via Pika) is gaining strong traction in North American public libraries, especially with Koha. It offers native FRBR grouping, e-content integration, and a companion mobile app (LiDA). ByWater Solutions and Open Fifth are major support providers. [^22][^23][^24]
- **DSpace 7+ uses Solr as a prerequisite** (not embedded) for its internal search and OAI-PMH provider, but it does not act as a unified discovery layer for external ILS data. When combined with VuFind, DSpace acts as a metadata source while VuFind provides the unified index. [^7][^25]
- **Solr vs. Elasticsearch**: Most open-source discovery layers (VuFind, Blacklight, Aspen) are built on Apache Solr. BUET's choice of Elasticsearch is atypical for the library domain but offers superior distributed search and REST API ergonomics. DSpace has experimented with Elasticsearch for statistics but retains Solr for core search. [^25][^26]
- **FOLIO adoption in the Global South** is nascent. Durban University of Technology became the first South African university to adopt FOLIO in 2022. Most developing-country institutions still rely on Koha + VuFind or Koha + Aspen due to lower infrastructure requirements. [^27][^28]
- **Maintenance burden specifics**: A Penn State analysis noted that maintaining a Ruby-based discovery layer (Blacklight) requires balancing Solr index server capacity, writing custom extraction scripts from the ILS, managing Rails dependencies, and providing QA/dev environments—adding ~6 servers to the environment. [^18]
- **Query forwarding / Bento-box search**: Advanced VuFind implementations (e.g., Calcutta University prototype) support query forwarding to external databases (DOAJ, OJS, NDLTD) and Bento-box result grouping—features not always available in commercial discovery layers. [^19][^29]

### Major Players & Sources
- **VuFind** (Villanova University / vufind.org): The most widely deployed open-source discovery layer. ~200+ institutions globally. LAMP stack, PHP, Apache Solr. Strongest in academic libraries and developing countries. [^1][^19]
- **Blacklight** (University of Virginia / Stanford / projectblacklight.org): Ruby on Rails engine over Solr. Highly flexible but requires more development. Predominant in Hydra/Samvera digital repository ecosystems and large research universities. [^2][^9][^10]
- **Aspen Discovery** (ByWater Solutions / Marmot Library Network): Forked from VuFind via Pika. Designed for public libraries. Strong e-content integration, FRBR grouping, mobile app. Rapidly growing adoption in North America. [^22][^23][^24]
- **eXtensible Catalog (XC)** (University of Rochester): FRBR/RDA-focused, metadata management toolkit. Less widely adopted as a discovery layer but influential in standards. [^1][^3]
- **FOLIO** (Open Library Foundation / EBSCO / Index Data): Open-source Library Services Platform, not a discovery layer. Modular, microservices, cloud-native. Adopted by Cornell, Stanford, CU Boulder, Chalmers, Durban UT. [^11][^12][^13][^27]
- **Pika** (Marmot Library Network): Predecessor to Aspen, a VuFind fork for consortia. Still referenced in migration paths. [^24]
- **Koha** (Koha Community / ByWater / Open Fifth): The dominant open-source ILS. 15,000+ libraries. Provides the MARC/OAI-PMH backend that discovery layers harvest from. [^22][^23]
- **DSpace** (LYRASIS / MIT): Leading open-source institutional repository. OAI-PMH source for discovery layers. Version 7+ modernized the REST API and Solr architecture. [^7][^25]
- **Open Fifth / ByWater Solutions / Equinox**: Major commercial support providers for open-source library stacks (Koha, VuFind, Aspen, FOLIO). They offer hosting, migration, and training—critical for institutional adoption. [^22][^23][^24]

### Trends & Signals
- **Trend toward LAMP-stack compatibility in developing countries**: Because Koha and DSpace are LAMP-based, VuFind (also LAMP) is the natural fit. This "stack homogeneity" reduces integration friction and server costs. [^19][^20]
- **Trend from discovery layers to Library Services Platforms**: FOLIO represents a shift from "overlay" discovery layers to unified backend platforms that manage both print and electronic resources. However, FOLIO still requires a separate discovery layer for patron-facing search. [^11][^12]
- **Trend toward containerization and cloud hosting**: ByWater Solutions and others now host Koha + Aspen in the cloud. FOLIO is Kubernetes-native. VuFind Docker images exist but are less mature. [^14][^15][^16]
- **Trend of FRBRization and record grouping**: Aspen and commercial systems group all formats of a title into one result. VuFind supports deduplication/merge records but requires configuration. Blacklight does not do this out-of-the-box. [^22][^24]
- **Signal: South Asian adoption is VuFind-centric**, with India leading in research and prototype development (University of Kalyani, Calcutta University, INFLIBNET). There is a visible "Koha movement" and an emerging "VuFind movement" in India. [^19][^20][^21]
- **Signal: FOLIO is gaining ground in elite Global South institutions** (e.g., Durban UT, University of the West Indies), but its microservices complexity creates a barrier for resource-constrained libraries. [^27][^28]
- **Signal: REST APIs are replacing OAI-PMH for real-time integration**, though OAI-PMH remains the workhorse for bulk indexing. The Koha REST API (OAuth2) is now the preferred method for secure VuFind-Koha integration. [^5][^6]
- **Signal: Full-text indexing (Apache Tika) is becoming a differentiator** for open-source discovery systems in developing countries, enabling local ETD/IR content to be searchable at the full-text level—something not always offered by commercial web-scale discovery. [^8][^19][^29]

### Controversies & Conflicting Claims
- **VuFind vs. Blacklight superiority**: Some evaluations (e.g., Chickering & Yang 2014) ranked Blacklight lowest among discovery tools (6/16 advanced features), while VuFind scored 10/16. However, Blacklight advocates argue that its minimalism is a feature, not a bug, enabling deeper local customization. [^1][^9]
- **Open-source TCO vs. commercial**: Some studies claim open-source discovery is "free" and thus ideal for developing countries. Others (e.g., Penn State, ECU) document that the **hidden labor costs** (staff time for customization, MARC cleanup, server maintenance) can exceed commercial SaaS subscriptions when local expertise is scarce. [^17][^18]
- **FOLIO: revolutionary vs. over-engineered?**: Proponents highlight its microservices agility, vendor neutrality, and API-first design. Critics note the steep learning curve, complex migration, and need for strong IT support—making it questionable for small or under-resourced libraries. [^11][^12][^13]
- **Containerization readiness**: VuFind officially documents Docker support, but the community Docker image (`dainst/vufind-docker`) is not officially maintained by the VuFind project. FOLIO is Kubernetes-native, while Blacklight deployments are typically custom-Dockerized per institution. [^14][^15][^16]
- **Solr vs. Elasticsearch for library discovery**: The library open-source ecosystem is overwhelmingly Solr-based (VuFind, Blacklight, DSpace, Aspen). BUET's choice of Elasticsearch is unconventional and may require building custom indexing pipelines rather than using off-the-shelf SolrMarc/VuFind harvesters. [^25][^26]
- **Is Aspen truly open-source?**: Aspen is open-source (GPL) but its development is heavily influenced by ByWater Solutions. Some in the community view it as a "vendor-led" open-source project, unlike the more community-governed VuFind and Koha. [^22][^24]

### Recommended Deep-Dive Areas
- **Elasticsearch integration with VuFind/Blacklight**: Because the entire open-source library ecosystem is Solr-centric, BUET must investigate how to adapt VuFind's Solr schema or replace it with Elasticsearch. This is a high-risk architectural divergence requiring custom engineering. [^25][^26]
- **OAI-PMH harvester design for BUET**: Since BUET plans Python microservices for OAI-PMH harvesting, a deep-dive into the Koha OAI-PMH provider configuration, DSpace OAI-PMH endpoint, and MARC-to-Elasticsearch indexing pipeline is warranted. The existing `harvest_oai.php` in VuFind could be a reference model. [^4][^7][^8]
- **MultiBackend driver / REST API integration for Koha**: If BUET needs to support multiple Koha instances (e.g., departmental libraries), the MultiBackend driver with OAuth2 REST API is the most secure and scalable pattern. [^5][^6]
- **Drupal 11 as a discovery front-end**: BUET plans Drupal 11 + Elasticsearch. This is a non-standard stack. Research is needed on how Drupal's Search API module can integrate with Elasticsearch and whether it can replicate faceted navigation, relevance ranking, and real-time availability lookups from an ILS. [^19]
- **FOLIO as a long-term backend option**: If BUET eventually needs a unified print/electronic management platform, FOLIO's modular architecture (Inventory, ERM, Codex) should be evaluated. However, this is a multi-year commitment requiring significant migration effort. [^11][^12][^13]
- **Aspen Discovery as a public-library alternative**: If BUET's e-library serves a public-facing or multi-format audience, Aspen's e-content integration and mobile app may be worth comparing against VuFind. [^22][^24]
- **Developing-country support ecosystem**: BUET should assess whether local support providers exist for Koha/VuFind in Bangladesh, or whether contracts with international vendors (ByWater, Open Fifth, Equinox) are feasible. [^22][^23][^28]
- **Maintenance burden modeling**: Before selecting an open-source stack, BUET should model the total cost of ownership, including staffing for PHP/Ruby development, Solr/Elasticsearch administration, Drupal theming, and ongoing MARC metadata cleanup. [^17][^18]

---

[^1]: Chickering, F. W., & Yang, S. Q. "Evaluation and Comparison of Discovery Tools: An Update." *Information Technology and Libraries*, June 2014. https://ital.corejournals.org/index.php/ital/article/download/3471/pdf_1/10968

[^2]: GitHub. "projectblacklight/blacklight." Description and installation docs. https://github.com/projectblacklight/blacklight

[^3]: Breeding, M. (2015). "Discovery Functionality." *Library Technology Reports*, 50(1), 5-32. Referenced in multiple comparison studies.

[^4]: VuFind Documentation. "indexing:koha." VuFind Wiki, 2025. https://vufind.org/wiki/indexing:koha

[^5]: Mukhopadhyay, P. "VuFind and Koha integration: a comparison of three generations of connectivity approaches." VuFind Summit 2020. https://vufind.org/vuFind/docs/summit2020/VuFind202009-V2_PSM.pdf

[^6]: Seneviratne, T. M., & Kodikara, R. C. "VuFind integration with Koha Multiple Instances." NatlibSYMPO 2022. http://www.natlib.lk/pdf/NatlibSYMPO2022_Con_Proc.pdf

[^7]: VuFind Documentation. "indexing:dspace." VuFind Wiki, 2024. https://vufind.org/wiki/indexing:dspace

[^8]: Bhowmick, A., & Chakrabarty, B. "Integration of Open-Source Software (Koha, Greenstone and DSpace) with Library Discovery System (VuFind): A Future Library Solution." *SRELS Journal of Information Management*, Vol 58(4), August 2021. https://www.researchgate.net/publication/354236155

[^9]: Cramer, T. "Blacklight at Stanford: A Highly Leveraged, Reusable, Discovery Engine." Stanford University Libraries, December 2009. https://www.cni.org/wp-content/uploads/2022/08/cni_blacklight_cramer.pdf

[^10]: Virginia Tech. "Front-End Team Final Report" (Blacklight architecture). https://vtechworks.lib.vt.edu/server/api/core/bitstreams/29ca4333-a093-4b28-adfd-5819b5384db7/content

[^11]: FOLIO. "Future of Libraries is Open." Official site. https://folio.org/

[^12]: Librarianship Studies. "FOLIO: The Open-Source Library Services Platform Revolutionizing Library Management." 2026. https://www.librarianshipstudies.com/2025/11/folio-open-source-library-services.html

[^13]: EBSCO. "Understanding the Difference Between FOLIO and EBSCO FOLIO." 2025. https://about.ebsco.com/resources/folio-vs-ebsco-folio-library-services-platform

[^14]: VuFind Documentation. "installation." Docker note. https://vufind.org/wiki/installation

[^15]: GitHub. "dainst/vufind-docker." Community Docker image. https://github.com/dainst/vufind-docker

[^16]: Temple University. "Technology stack" (Blacklight + Docker + Postgres + Solr). https://scholarshare.temple.edu/server/api/core/bitstreams/e372b8ed-5643-4574-92e2-db52b990fdba/content

[^17]: Barber, M. "Customizing an Open Source Discovery Layer at East Carolina University Libraries." *LRTS*, 2017. https://journals.ala.org/lrts/article/view/6039/7738

[^18]: Tillman, R. K. "Maintenance, Labor, and the Classic Catalog." 2019. https://ruthtillman.com/talk/maintenance-labor-classic/

[^19]: Roy, B. K., Mukhopadhyay, P., & Biswas, A. "Discovery Layer in Library Retrieval: VuFind as an Open Source Service for Academic Libraries in Developing Countries." *Journal of Information Science Theory and Practice*, 10(4), 2022. https://accesson.kr/jistap/v.10/4/3/27622

[^20]: Saha, S., & Mandal, S. "E-Discovery Tools and Applications in Modern Libraries." IGI Global. Referenced in Roy et al. 2022.

[^21]: ResearchGate. "Integration of Open-Source Software (Koha, Greenstone and DSpace) with Library Discovery System (VuFind)." 2021. https://www.researchgate.net/publication/354236155

[^22]: Library Journal. "Open for Growth: Open Source Platforms on the Rise." 2022. https://www.libraryjournal.com/story/Open-for-Growth-Open-Source-Platforms-on-the-Rise

[^23]: ByWater Solutions. Multiple Aspen/Koha implementation press releases. https://librarytechnology.org/document/27534

[^24]: Open Fifth. "Corporate Social Responsibility" (product list). https://openfifth.co.uk/wp-content/uploads/2025/04/Open-Fifth-Corporate-Social-Responsibility-Signed-1.pdf

[^25]: LYRASIS Wiki. "DSpace 7 Upgraded from Solr 4 to Solr 7 -- Q & A." https://wiki.lyrasis.org/pages/viewpage.action?pageId=112528818

[^26]: Semantic Scholar. "An Analysis on the Comparison of the Performance and Configuration Features of Big Data Tools Solr and Elasticsearch." https://pdfs.semanticscholar.org/9e27/e6b9afc7a2632b23c566d8bb19e7b44b4688.pdf

[^27]: EBSCO. "Durban University of Technology Becomes First University in South Africa to Adopt the FOLIO Library Services Platform." Referenced in ITAL 2026 article. https://ital.corejournals.org/index.php/ital/article/view/17398

[^28]: ByWater Solutions. "FOLIO support." https://bywatersolutions.com/products/folio

[^29]: Mukhopadhyay, P. "Automatic Geographic Name Authority from Scratch..." VuFind Summit 2021. https://vufind.org/wiki/community:conferences:summit_2021
