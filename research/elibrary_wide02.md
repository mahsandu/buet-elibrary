## Facet: Commercial Discovery Services

### Key Findings

- The major commercial web-scale discovery platforms are **Ex Libris Primo/Summon** (now Clarivate), **EBSCO Discovery Service (EDS)**, **OCLC WorldCat Discovery**, and **SirsiDynix Enterprise**. A fifth player, **AquaBrowser Library** (acquired by ProQuest), pioneered the visual discovery layer but is now considered legacy[^1].

- **Primo** offers two deployment models: **Primo Classic** (managed via Primo Back Office, available for local installation or hosted cloud) and **Primo VE** (a unified cloud-native model tightly integrated with Ex Libris Alma). Primo VE is deployed on the "Higher-Ed Platform" with monthly releases, while Primo Classic follows quarterly service packs[^2].

- **Primo Central Discovery Index (CDI)** — now simply the **Central Discovery Index (CDI)** — is the unified index powering both Primo and Summon. It contains over **5.1 billion records** and is hosted exclusively by Ex Libris in the cloud. Local content (OPAC, repositories) is merged with CDI at query time[^3].

- **EBSCO Discovery Service (EDS)** is the most widely deployed index-based discovery service, installed at over **16,000 libraries** globally. It relies on a proprietary **Central Index** compiled from EBSCOhost databases, third-party publishers, and open-access sources. EDS is ILS-agnostic and offers integration via a plugin (for Koha, etc.), OAI-PMH harvesting, or the EDS API for embedding into external interfaces[^4].

- **EDS institutional repository integration** supports Dublin Core, EAD, METS, MODS, and OAI-PMH. EBSCO analyzes each IR individually for optimized loading and display, indicating that IR integration is not fully automated but customized per deployment[^5].

- **WorldCat Discovery Services (WDS)** is a **cloud-only suite** (SaaS) combining FirstSearch and WorldCat Local. It offers a central index of ~1 billion articles/e-books plus the WorldCat bibliographic database. OCLC describes its model as "cooperative SaaS" — all libraries share the same hardware, services, and data, benefiting from network effects rather than isolated tenant hosting[^6].

- **Index-based discovery** (Summon, Primo, EDS, WorldCat) pre-harvests content into a unified central index, enabling consistent relevance ranking, fast response times, and cross-source faceting. **Federated search** (MetaLib, WebFeat, 360 Search) sends queries to remote databases in real time and aggregates results, suffering from slow response times, inconsistent ranking, and limited deduplication[^7].

- **Pricing for commercial discovery services** is generally **subscription-based** and scaled by institution size (FTE — Full-Time Equivalent). Reported figures range from roughly **$30,000–$60,000 per year** for Primo, EDS, and Summon at mid-sized institutions, with larger universities potentially paying more. Implementation fees add $3,000–$10,000. Pricing is notoriously opaque and negotiated individually[^8].

- **AquaBrowser Library** follows a **decoupled architecture**: it harvests data from the ILS into its own search engine ("Igor") and can run locally or via vendor-hosted SaaS. It is distinguished by visual word-cloud "constellations" for exploratory search. However, it is primarily a **discovery interface** rather than a web-scale index, relying on local index plus optional federated search connectors[^9].

- **Hybrid open-source + commercial models** are increasingly common. **Columbia University** uses **Blacklight** (open-source) as the front-end discovery layer with **EBSCO Discovery Service** as the back-end index. **Texas State University** uses **FOLIO** (open-source LSP) integrated with EDS. **VuFind** supports connectors to Summon, EDS, and WorldCat APIs, allowing libraries to blend open-source interfaces with commercial indexes[^10].

- **EBSCO FOLIO** represents the most prominent **commercially-supported open-source LSP** strategy. EBSCO provides hosting, implementation, and integrates EDS natively, offering a hybrid model where the core platform is open-source but discovery and analytics are proprietary SaaS[^11].

- **SirsiDynix Enterprise** is a cloud-based discovery platform that can operate as a **unified catalog** (interfiling physical and digital assets) and also integrates with **EBSCO Discovery Service** via a "Publication Placard" that surfaces EDS article results within the Enterprise interface. It supports federated search targets and responsive design[^12].

- **Ex Libris operates a private cloud** with data centers in Chicago, Amsterdam, Singapore, and Beijing. Alma, Primo VE, and Summon are available **exclusively as SaaS**; Primo Classic still supports local installation but most new implementations are hosted. Ex Libris holds ISO 27001 and ISO 27018 certifications for cloud security[^13].

- **Relevance ranking** differs fundamentally between architectures: unified index services apply a single algorithm (e.g., EDS blends EBSCO subject indexing with usage data; Primo uses FRBR grouping and a "value score"). Federated search cannot achieve balanced cross-source ranking because each remote database uses its own algorithm[^14].

- **Market consolidation** has concentrated the discovery space under a few entities. **Clarivate** acquired **ProQuest** (which had previously acquired Ex Libris and Innovative Interfaces). SPARC and others raised antitrust concerns that this creates an "effective monopoly" in library services platforms, with ProQuest/Ex Libris holding **~72% of academic LSP market share** and **84% among ARL institutions**[^15].

### Major Players & Sources

- **Ex Libris / Clarivate**: Market leader in academic discovery via Primo, Summon, and the Central Discovery Index (CDI). Primo VE is the cloud-native Alma-integrated model; Primo Classic remains for non-Alma customers. Source of the largest unified discovery index (5B+ records)[^3].

- **EBSCO Information Services**: Operator of EDS (16,000+ sites). Distinguishes itself via deep subject indexing (CINAHL, MEDLINE) and a multipronged integration strategy with ILS vendors. Also the primary commercial sponsor and hosting provider for the open-source **FOLIO** platform[^4][^11].

- **OCLC**: Non-profit cooperative offering WorldCat Discovery as a cloud suite. Strengths include global interlibrary loan integration, the WorldCat bibliographic database, and a neutral platform aggregating content from competing providers (EBSCO, Gale, ProQuest)[^6].

- **SirsiDynix**: Provides **Enterprise** (cloud-based discovery) and **eResource Central** for digital lending. Tightly integrated with Symphony/Horizon ILS, but also supports third-party EDS integration. Strong in public libraries and consortia[^12].

- **ProQuest / Serials Solutions (historical)**: Launched **Summon** in 2009 as the first pure unified-index discovery service. Summon and Primo now share the same CDI backend following Ex Libris/ProQuest consolidation. **AquaBrowser** was an early visual discovery layer acquired by ProQuest in 2008[^1][^9].

- **Medialab Solutions BV**: Original developer of **AquaBrowser Library** (2002). Now part of ProQuest. The "Igor" search engine and word-cloud "constellation" interface were distinctive features, though the product is now considered legacy in the web-scale era[^9].

- **Open-source alternatives**: **VuFind** (Villanova, PHP/Solr) and **Blacklight** (UVA, Ruby/Solr) are the dominant open-source discovery interfaces. They can be combined with commercial indexes via APIs, or used with local Solr indexes for institutional repositories and catalogs[^10].

### Trends & Signals

- **Shift from local to cloud-only SaaS**: Ex Libris has "thoroughly embraced SaaS as the strategic deployment model." Alma and Primo VE are cloud-only; Primo Classic local installs are declining. OCLC WorldCat Discovery and EBSCO EDS are also hosted SaaS. This reduces library IT burden but increases vendor lock-in[^13].

- **Convergence of LSP and discovery**: Primo VE merges back-end Alma and front-end Primo into a single platform. EBSCO positions FOLIO + EDS as an integrated ecosystem. The boundary between the library management system and the discovery layer is dissolving[^2][^11].

- **Open-source front-ends with commercial back-end indexes**: A growing pattern (e.g., Columbia's Blacklight + EDS, Villanova's VuFind + Summon) allows libraries to retain custom UI control while leveraging the billion-record indexes of commercial vendors. This is a pragmatic hybrid for institutions with development capacity[^10].

- **Unified index overtaking federated search**: MetaLib and WebFeat-style federated search are considered legacy. The industry consensus is that unified index + relevance ranking provides a superior user experience, though a hybrid approach (unified index for most content, federated search for real-time targets) may be the practical future[^7].

- **Linked data and BIBFRAME**: OCLC is enhancing WorldCat with linked data entities. EBSCO offers BiblioGraph (BIBFRAME-based). Ex Libris has been moving toward linked data in Primo. This signals a long-term shift from MARC-centric discovery to graph-based resource description[^11].

- **Pricing opacity and value-based concerns**: Pricing is scaled by FTE but libraries report significant variation. Developing-country institutions (e.g., in India) report EDS costs exceeding ~$25,000/year, which is prohibitive for many, driving interest in open-source alternatives like VuFind[^8].

### Controversies & Conflicting Claims

- **Monopoly and market consolidation**: SPARC filed objections with the FTC opposing the Clarivate-ProQuest merger, arguing it creates an "effective monopoly" in academic LSPs (72% market share) and neutralizes competition. Clarivate/ProQuest defenders argue it creates a stronger competitor to Elsevier. The FTC did not block the merger, which closed in 2021[^15].

- **Content neutrality of discovery algorithms**: Librarians have raised concerns that vendors owning both discovery platforms and content (e.g., ProQuest/Clarivate owns ProQuest content + Primo/Summon; EBSCO owns databases + EDS) could subtly prioritize their own content in relevance rankings. Vendors deny this, but algorithms are opaque, making verification difficult[^15].

- **Primo vs. Summon future**: After ProQuest acquired Ex Libris, speculation emerged that Summon would be sunset in favor of Primo. Ex Libris has stated that "Summon has hundreds of satisfied customers and will continue to be one of Ex Libris' flagship discovery products." However, both now share the same CDI, and functional parity efforts suggest long-term convergence rather than dual development tracks[^2].

- **FOLIO as genuine open source vs. EBSCO ecosystem lock-in**: FOLIO is community-led and open-source, but critics note that EBSCO's dominant role in funding, hosting, and integrating EDS creates a "soft lock-in" where FOLIO implementations almost always adopt EDS. EBSCO counters that FOLIO APIs allow any discovery integration, though in practice most adopters use EDS[^11].

- **Unified index staleness vs. federated search freshness**: Proponents of unified index (Summon, Primo, EDS) claim it is the only way to achieve meaningful relevance ranking and fast performance. Federated search advocates note that unified indexes can lag behind live catalog updates, and real-time availability checking requires supplemental API calls. Both EDS and Primo use RTAC (real-time availability checking) APIs to mitigate this[^7].

- **OCLC's cooperative model vs. commercial competition**: OCLC positions itself as a neutral non-profit, but its WorldCat Discovery competes directly with commercial discovery services. Some critics argue that OCLC's cooperative data model creates dependency on WorldCat and restricts competitive alternatives, while supporters argue it provides essential global infrastructure[^6].

### Recommended Deep-Dive Areas

- **Primo VE vs. Primo Classic technical architecture**: Understanding the exact differences in back-office management, Alma integration, real-time publishing workflows, and customization APIs is critical for any institution considering migration. Primo VE's cloud-only model has implications for local customization that differ significantly from Primo Classic[^2].

- **EDS API and integration patterns with Koha/DSpace**: EBSCO provides extensive documentation on OAI-PMH, Z39.50, and API integration. A technical deep-dive should map the exact data flows, authentication mechanisms (SSO/OpenAthens), and RTAC implementation for a LAMP-stack environment like BUET's[^4][^5].

- **FOLIO + EDS as a reference hybrid architecture**: For a Python/Elasticsearch/Drupal shop, EBSCO FOLIO's modular microservices architecture (Okapi gateway, app-based modules) and its native EDS integration represent the closest real-world analog to a hybrid open-source/commercial stack. Studying FOLIO's API surface and data models would be directly applicable[^11].

- **Central Discovery Index (CDI) licensing and content coverage**: The CDI is the largest scholarly index available, but its value depends on a library's licensed content. Understanding how "holdings management" works, how EBSCO/Primo determine full-text availability, and how much control libraries have over result ranking is essential for procurement evaluation[^3].

- **Cost modeling for developing-country institutions**: Existing pricing data is fragmented and North American/European-centric. A dedicated study should solicit quotes from EBSCO, Ex Libris, and OCLC for a South Asian university context, comparing TCO against a self-hosted VuFind/Elasticsearch stack[^8].

- **Federated search as a complement, not a replacement**: Given BUET's use of multiple disparate sources (Koha, DSpace, external databases), a hybrid architecture using a unified index for local + major commercial content, plus federated connectors for real-time targets (e.g., live government repositories), may be optimal. Research should evaluate modern federated search connectors for Solr/Elasticsearch[^7].

- **Market consolidation risk assessment**: With Clarivate/ProQuest controlling the majority of the academic LSP and discovery market, BUET should evaluate vendor stability, multi-year contract risks, and contingency planning. A scenario analysis of what happens if Primo/Summon or Alma pricing/terms change post-consolidation would be prudent[^15].

---

[^1]: Marshall Breeding, "Library Resource Discovery Products," *Library Technology Reports*, January 2014. https://journals.ala.org/index.php/ltr/article/viewFile/5779/7236

[^2]: Ex Libris, "Frequently Asked Questions for Primo VE," Knowledge Center, July 2025. https://knowledge.exlibrisgroup.com/Primo/Product_Documentation/020Primo_VE/Primo_VE_(English)/020FAQs/Frequently_Asked_Questions_for_Primo_VE

[^3]: IGeLU, "Primo enhancements timeline," 2024. https://igelu.org/products-and-initiatives/product-working-groups/primo/primo-enhancements/; and TRU Environmental Scan, "Primo and Summon," 2023. https://tru.arcabc.ca/_flysystem/repo-bin/2023-08/tru_6235.pdf

[^4]: EBSCO, "EBSCO Discovery Service Tech Sheet," 2025. https://www.ebsco.com/sites/default/files/acquiadam-assets/EBSCO-Discovery-Service-Tech-Sheet.pdf; and Marshall Breeding, "Index-Based Discovery Services: Current Players and Products," *Library Technology Reports*, November 2019. https://journals.ala.org/index.php/ltr/article/view/6874/9255

[^5]: EBSCO, "EBSCO Discovery Service Institutional Repository Integration Guide," 2025. https://www.ebsco.com/sites/default/files/acquiadam-assets/EBSCO-Discovery-Service-Tech-Sheet.pdf

[^6]: OCLC, "OCLC introduces WorldCat Discovery Services," January 2014. http://www.stm-publishing.com/oclc-introduces-worldcat-discovery-services/; and Clarivate, "Welcome to the cloud," Ex Libris Cloud Statement, April 2026. https://clarivate.com/information-security/statements/welcome-to-the-cloud/

[^7]: Chetan S. Sonawane, "Library Discovery System: An Integrated Approach to Resource Discovery," *Informatics Studies*, 2017. http://eprints.rclis.org/32499/1/54-244-1-PB.pdf; and Sharon Q. Yang and Kurt Wagner, "Evaluation and Comparison of Discovery Tools," *ProQuest*, 2025. https://www.proquest.com/scholarly-journals/evaluation-comparison-discovery-tools-update/docview/1547993777/se-2

[^8]: Bill Denton, "How much do web-scale discovery services for libraries cost?" *Miskatonic University Press*, November 2011. https://www.miskatonic.org/2011/11/09/how-much-do-web-scale-discovery-services-libraries-cost/; and Anupam Bhowmick and Baishakhi Chakrabarty, "Integration of Open-Source Software with Library Discovery System (VuFind)," *SRELS Journal*, August 2021. https://www.researchgate.net/publication/354236155

[^9]: Marshall Breeding, "AquaBrowser," *Library Technology Reports*, July 2007. https://journals.ala.org/ltr/article/download/4542/5336; and ProQuest, "AquaBrowser Becomes Top Discovery Layer for Libraries," July 2009. https://about.proquest.com/en/news/2009/AquaBrowser-Becomes-Top-Discovery-Layer-for-Libraries/

[^10]: Graham Seaman, "Adapting VuFind as a Front-end to a Commercial Discovery System," *Ariadne*, Issue 68. http://www.ariadne.ac.uk/issue/68/seaman/; and EBSCO, "EDS Integration with Open Source Front-Ends," 2025. https://www.ebsco.com/zh-tw/node/84546

[^11]: EBSCO, "EBSCO FOLIO Overview," 2025. https://www.ebsco.com/sites/default/files/acquiadam-assets/EBSCO-FOLIO-Overview.pdf; and Columbia University Libraries, "Go Live with EBSCO FOLIO," August 2025. https://about.ebsco.com/news-center/press-releases/columbia-university-libraries-modernize-library-infrastructure-ebsco-folio

[^12]: SirsiDynix, "Enterprise," 2025. https://www.sirsidynix.com/enterprise/; and SoftwareOne, "SirsiDynix Enterprise Product Page." https://platform.softwareone.com/product/sirsidynix-enterprise/PCP-4872-8321

[^13]: Ex Libris, "Technical Requirements for Alma and Discovery Implementation," May 2026. https://knowledge.exlibrisgroup.com/Alma/Implementation_and_Migration/Implementation_Guides/03Technical_Requirements_for_Alma_and_Discovery_Implementation; and Marshall Breeding, "Ex Libris Expands International Operations," *Library Technology*, December 2016. https://librarytechnology.org/document/22268

[^14]: Yang and Wagner, "Evaluation and Comparison of Discovery Tools," 2025. https://www.proquest.com/scholarly-journals/evaluation-comparison-discovery-tools-update/docview/1547993777/se-2

[^15]: SPARC, "Opposing the Merger Between Clarivate PLC and ProQuest LLC," FTC Letter, October 2021. https://sparcopen.org/wp-content/uploads/2021/10/SPARC-FTC-Letter-in-Opposition-to-the-Clarivate-ProQuest-Merger.pdf; and Roger Schonfeld, "The New Clarivate Science," *The Scholarly Kitchen*, December 2021. https://scholarlykitchen.sspnet.org/2021/12/09/new-clarivate-science/
