## Facet: OAI-PMH Harvesting & ETL Architectures for Library Metadata

### Key Findings
- **Sickle** is the dominant Python OAI-PMH harvester library, providing a Pythonic iterator interface over all six OAI verbs and automatic deserialization of Dublin Core payloads into dictionaries [^1]. It is used in production by institutions like MIT Libraries, the Staatsbibliothek zu Berlin, and OARepo/Invenio [^2][^3].
- **PHP** has two mature harvester options: **phpoaipmh** by Casey McLaughlin (Composer/PSR-12, Guzzle/cURL, iterator-based pagination) [^4] and **phpetra/oai-pmh-tools** (framework-independent, XML/cURL adapters) [^5]. **Node.js** has **@indexdata/oai-pmh** (Index Data, Apache 2.0, async/await) [^6] and **jmaferreira/oai-pmh** (CLI-focused, npm installable) [^7].
- **Metadata mapping** between Dublin Core, MARC, and custom schemas is universally handled via **XSLT crosswalks** in both DSpace and Koha [^8][^9]. The Library of Congress maintains canonical crosswalks (DC<->MODS, MARC<->MODS) [^10]. Crosswalks are inherently lossy because DC is simple (15 elements) while MARC/MODS are granular; one-to-many and many-to-one mappings are common [^11].
- **ETL pipelines** for library metadata follow a four-stage pattern: **Harvest** (OAI-PMH with Sickle/phpoaipmh) -> **Transform** (XSLT or custom Python/JSON transformers) -> **Validate** (XML schema, JSON Schema, or Great Expectations) -> **Index** (Elasticsearch/Solr) [^12][^13]. Elasticsearch ingest pipelines can perform pre-index transformations (set, rename, on_failure handlers) [^14].
- **Incremental harvesting** uses `from`/`until` date parameters with a stored `last_harvest.txt` watermark; best practice includes an overlap window of 1-7 days to catch timezone-boundary updates [^15][^16]. **Resumption tokens** are Base64-encoded, time-limited, and opaque; harvesters must cache the last successful token and avoid mixing it with other parameters [^17].
- **Scheduling** ranges from simple **cron** (e.g., `batch-delete.sh` + `batch-import-marc.sh` in VuFind) [^18] to **Celery** (OARepo runs harvesters as background tasks) [^3] to **Apache Airflow** (enterprise DAGs with retry logic, SLAs, and backfill support) [^19]. The CORE aggregator uses a custom microservices scheduler (CHARS) to proactively harvest based on resource utilization [^20].
- **Deduplication** across multiple sources (e.g., Koha + DSpace) is typically solved by: (a) source-attribution prefixes on record IDs, (b) **merged_child_boolean** flags with source precedence lists (VuFind pattern) [^21], or (c) fingerprint hashing (MD5/SHA1 over key fields) with Elasticsearch versioning or bloom filters [^22].
- **Error handling** best practices include: exponential backoff with max retry limits (default 3-5), dead-letter queues for poison records, idempotent upserts (merge instead of blind insert), structured JSON logging, and centralized alerting via ELK/Prometheus/Grafana or Sentry [^23][^24]. OAI-PMH-specific resilience requires handling HTTP 503/429, XML validation failures, and resumption token expiry by restarting from the last successful page [^25].
- **DSpace** exposes OAI-PMH via OCLC OAICat, supports DC, MARCXML, MODS, METS, RDF, and DIDL by default, and uses XSLT crosswalks in `dspace/config/modules/oai.cfg` [^8][^26]. **Koha** acts as a Data Provider only (not a harvester) and exposes MARC21, MARCXML, and OAI-DC via configurable XSLT files; `include_items: 1` can append item-level data [^9].

### Major Players & Sources
- **Sickle (Python)**: De facto standard OAI-PMH client for Python; powers OARepo, MIT Libraries, and CORE workflows [^1][^2][^3].
- **phpoaipmh (PHP)**: Mature, PSR-12 compliant, iterator-based harvester with Guzzle/cURL transport [^4].
- **@indexdata/oai-pmh (Node.js)**: Modern async/await library from Index Data, used in FOLIO/ui-harvester-admin ecosystem [^6].
- **OARepo / Invenio**: Czech/Norwegian open-source framework providing a full harvester->transformer->writer pipeline with Celery scheduling and Sentry logging [^3].
- **MIT Libraries**: Publishes an open-source Python CLI harvester (`oai-pmh-harvester`) with Docker support and S3 output, demonstrating production-grade packaging [^2].
- **VuFind**: PHP/Solr-based discovery platform with a documented OAI-PMH harvest workflow (`harvest_oai.php`, `batch-import-marc.sh`, `last_harvest.txt`) [^18].
- **CORE (Open University, UK)**: Operates one of the world's largest OAI-PMH aggregators; published a Nature Scientific Data paper describing their microservices architecture, scheduler, and scalability challenges [^20].
- **FOLIO**: LSP with an OAI-PMH app that implements best practices for resumption tokens, deleted records, and batch sizing (100-200 records/page recommended) [^17].
- **Library of Congress**: Maintains canonical MODS<->DC and MODS<->MARC crosswalks in XSLT [^10].
- **EBSCO Discovery Service**: Aggregates institutional repositories via OAI-PMH (DC, EAD, METS, MODS) and performs custom mapping per repository [^27].

### Trends & Signals
- **Microservices + proactive scheduling**: Large-scale aggregators like CORE are moving from fixed cron schedules to resource-aware, pro-active harvesting microservices (CHARS) to improve recency and throughput [^20].
- **Elasticsearch as target index**: More institutions are adopting Elasticsearch (or OpenSearch) for metadata aggregation, using ingest pipelines for transformation and dead-letter indices for failed records [^14][^23].
- **Beyond OAI-PMH**: ResourceSync is being promoted as a successor for large-scale content harvesting because OAI-PMH is inherently sequential and lacks content-level validation [^20].
- **MODS as intermediate lingua franca**: Institutions increasingly use MODS (Metadata Object Description Schema) as a richer bridge between MARC and DC, because it is XML-native, human-readable, and supported by crosswalks [^10][^11].
- **Containerization**: MIT Libraries and OARepo both ship harvesters in Docker containers, reflecting a trend toward immutable, scheduled harvest jobs [^2][^3].
- **AI-assisted scheduling**: Emerging research suggests ML-based incremental metadata detection and reinforcement-learning schedulers to reduce unnecessary harvesting overhead [^28].

### Controversies & Conflicting Claims
- **OAI-PMH scalability**: The protocol is praised for simplicity but criticized for inherent sequentiality and lack of parallelization. CORE notes it is "ill-suited for harvesting from very large repositories" and advocates ResourceSync, yet thousands of institutions continue to rely on it exclusively [^20][^29].
- **Lossy crosswalks vs. unified schema**: Some practitioners argue Dublin Core should remain the lowest common denominator for interoperability [^11]; others (e.g., FOLIO, EBSCO) invest in richer formats (MARCXML, MODS) to preserve granularity, accepting the complexity of many-to-one mappings [^17][^27].
- **Retry and idempotency**: OpenMetadata advises DAGs should have *no* retries because heavy workflows failing mid-run incur extra costs [^30]; conversely, OAI-PMH best practices and ETL literature strongly recommend exponential backoff retries for transient network failures [^23][^24]. The resolution is context-dependent: no retries for orchestrator-level DAGs, but fine-grained retries inside the harvester HTTP client.
- **Harvester vs. Data Provider role**: Koha explicitly *cannot* act as a harvester (only a Data Provider) because MARC is its only native indexed format, limiting its role in bidirectional ETL pipelines unless middleware is built [^9]. DSpace supports both roles (provider and harvester) but its OAI-PMH server is read-only by design [^8][^26].

### Recommended Deep-Dive Areas
- **ResourceSync protocol adoption**: Because OAI-PMH has fundamental scalability limits for multi-million-record repositories, BUET should evaluate whether ResourceSync (or parallel OAI-PMH sharding) is a future-proof alternative for large-scale harvesting [^20].
- **MODS<->JSON-LD unified schema design**: Since BUET needs to merge DSpace (DC/MODS) and Koha (MARC21) metadata into Elasticsearch, designing a canonical internal JSON schema (inspired by MODS or schema.org) with explicit provenance fields would reduce crosswalk loss and simplify deduplication [^10][^21].
- **Celery + Airflow hybrid scheduling**: For a V4 microservices architecture, comparing lightweight Celery beat schedules (as used by OARepo) against full Airflow DAGs (with backfills, SLAs, and monitoring) warrants a proof-of-concept to match BUET's operational maturity [^3][^19].
- **Deduplication fingerprinting strategy**: BUET should benchmark MD5/SHA1 hashing of normalized title+author+year against source-prefixed ID merging (VuFind pattern) to choose the right deduplication approach for Koha + DSpace overlap [^21][^22].
- **Elasticsearch ingest pipelines vs. Python transformers**: Evaluating whether to transform metadata in Python (before load) or via Elasticsearch ingest pipelines (at index time) affects error handling visibility, replayability, and schema evolution complexity [^14][^23].

---

### Footnotes

[^1]: Sickle Documentation. 2020. https://sickle.readthedocs.io/_/downloads/en/latest/pdf/
[^2]: MIT Libraries. "oai-pmh-harvester: Scripts for harvesting from repositories using OAI-PMH." GitHub. 2019. https://github.com/MITLibraries/oai-pmh-harvester
[^3]: OARepo. "oarepo-oai-pmh-harvester: The package is responsible for downloading resources from the OAI-PMH server." GitHub. 2020. https://github.com/oarepo/oarepo-oai-pmh-harvester
[^4]: Casey McLaughlin. "phpoaipmh: A PHP OAI-PMH harvester client library." GitHub. 2024. https://github.com/caseyamcl/phpoaipmh
[^5]: phpetra. "oai-pmh-tools: Set of PHP tools for OAI-PMH." GitHub. https://github.com/phpetra/oai-pmh-tools
[^6]: Index Data. "oai-pmh: Simple client library for OAI-PMH written in Node." GitHub. 2022. https://github.com/indexdata/oai-pmh
[^7]: jmaferreira. "oai-pmh: OAI-PMH 2.0 harvester module for nodejs." GitHub. 2017. https://github.com/jmaferreira/oai-pmh
[^8]: Prosentient Systems. "DSpace FAQ: Does DSpace support OAI/PMH." 2025. https://www.prosentient.com.au/node/390
[^9]: Koha Community. "Web services - Koha Manual." 2026. https://koha-community.org/manual/latest/en/html/webservices.html
[^10]: Library of Congress. "Dublin Core Metadata Element Set Mapping to MODS Version 3." 2012. https://www.loc.gov/standards/mods/dcsimple-mods.html
[^11]: K. Kiramang. "A Comparative Analysis on Dublin Core (DC) and Metadata Object Description Schema (MODS)." UIN Suka. 2008. https://digilib.uin-suka.ac.id/356/1/A%20COMPARATIVE%20ANALYSIS%20ON%20DUBLIN%20CORE%20%28DC%29%20AND%20METADATA%20OBJECT%20DESCRIPTION%20SCHEMA%20%28MODS%29.pdf
[^12]: Kestra. "Best ETL Pipeline Tools in 2026." 2026. https://kestra.io/resources/data/etl-pipeline-tools
[^13]: Datafold. "ETL pipeline testing: Validate, validate, validate." 2023. https://www.datafold.com/blog/etl-testing/
[^14]: Elastic. "Ingest pipelines." Elasticsearch Docs. https://www.elastic.org.cn/docs/8.1/www.elastic.co/guide/en/elasticsearch/reference/current/ingest.html
[^15]: JCDL 2003 Tutorial. "Introduction to OAI-PMH." UIUC. 2003. https://dli.grainger.uiuc.edu/Publications/TWCole/JCDL-OAI/
[^16]: VuFind Wiki. "OAI-PMH Harvesting - indexing." 2024. https://vufind.org/wiki/indexing:oai-pmh
[^17]: FOLIO Wiki. "OAI-PMH Best Practices." 2026. https://folio-org.atlassian.net/wiki/spaces/FOLIOtips/pages/5672278/OAI-PMH+Best+Practices
[^18]: VuFind Wiki. "OAI-PMH Harvesting - indexing." 2024. https://vufind.org/wiki/indexing:oai-pmh
[^19]: Apache Airflow. "Release Notes - Airflow Documentation." 2023. https://airflow.apache.org/docs/apache-airflow/2.7.1/release_notes.html
[^20]: Knoth, Petr et al. "CORE: A Global Aggregation Service for Open Access Papers." Nature Scientific Data. 2023. https://www.nature.com/articles/s41597-023-02208-w.pdf
[^21]: VuFind Wiki. "indexing:deduplication." 2023. https://vufind.org/wiki/indexing:deduplication
[^22]: Elastic Discuss. "Indexing-time document deduplication." 2011. https://discuss.elastic.co/t/indexing-time-document-deduplication/4579
[^23]: Milvus AI Quick Reference. "What are best practices for logging and monitoring ETL processes?" 2026. https://milvus.io/ai-quick-reference/what-are-best-practices-for-logging-and-monitoring-etl-processes
[^24]: IJCTT. "Best Practices for Error Handling, Monitoring, and Recovery." 2025. https://www.ijcttjournal.org/2025/Volume-73%20Issue-4/IJCTT-V73I4P120.pdf
[^25]: Clinical Journal of Nursing Care and Practice. "OAI-PMH Best Practices for Harvesters." 2025. https://www.nursingpracticejournal.com/cjncp/oai-pmh
[^26]: DSpace GitHub. "dspace/config/modules/oai.cfg." https://github.com/DSpace/DSpace/blob/main/dspace/config/modules/oai.cfg
[^27]: EBSCO. "EBSCO Discovery Service Tech Sheet - Institutional Repository Integration." https://www.ebsco.com/sites/default/files/acquiadam-assets/EBSCO-Discovery-Service-Tech-Sheet.pdf
[^28]: RSIS International. "Distributed harvesting pipelines and AI for OAI-PMH." IJRIAS. 2025. https://www.rsisinternational.org/journals/ijrias/DigitalLibrary/volume-10-issue-7/724-736.pdf
[^29]: DISIT. "Assessing Open Archive OAI-PMH implementations." DMS 2010. https://www.disit.org/disitmn/articoli/DMS2010-OAI-PMH-final-v9-1.pdf
[^30]: OpenMetadata. "Metadata Ingestion Best Practices." 2026. https://docs.open-metadata.org/v1.12.x/connectors/ingestion/best-practices
