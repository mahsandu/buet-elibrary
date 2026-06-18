## Facet: Containerized Repository & Discovery Stacks

### Key Findings
- **DSpace 7+** is split into a Java-based backend (REST API, OAI-PMH, SWORD) and an Angular-based frontend (dspace-angular). Official Docker Compose configurations include `docker-compose.yml` for the backend, `docker-compose-cli.yml` for CLI tasks, and `docker-compose-angular.yml` for the frontend. Core services orchestrated are: `dspace` (backend/Tomcat), `dspace-angular` (frontend/Node.js), `dspacedb` (PostgreSQL), and `dspacesolr` (Apache Solr). [^1][^2][^3]
- DSpace's official Docker images are **explicitly labeled "not production ready"** by the DSpace core team; institutions are advised to build their own images borrowing concepts from the official ones. However, DSpaceDirect at LYRASIS runs the public demo site (demo.dspace.org) on Docker, validating the images for production-like scenarios. [^3][^4]
- **Samvera/Hyku** is a multi-tenant digital repository built on Hyrax (Ruby on Rails). The containerized stack includes: PostgreSQL, Redis, Sidekiq (background workers), Solr, Fedora (or Postgres via Valkyrie), and the Rails web app. Hyku distributes both `docker-compose.yml` (development) and `docker-compose.production.yml` (production). [^5][^6][^7]
- **Islandora 8+** (ISLE - Islandora Enterprise) is fully containerized via Docker Compose. It integrates Drupal as the frontend/CMS, Fedora 6 as the persistence layer, and adds Blazegraph (triplestore), Solr, ActiveMQ, Cantaloupe (IIIF image server), and Traefik (reverse proxy). The `isle-dc` project generates `docker-compose.yml` from a `.env` configuration file. [^8][^9][^10]
- **VuFind** is a PHP/Apache Solr discovery layer. While official Docker Compose references are less mature than DSpace/Islandora, VuFind requires Apache, PHP, Solr, and MySQL/MariaDB/PostgreSQL. Some institutions deploy VuFind alongside DSpace via OAI-PMH harvesting, with VuFind's Solr on a separate port (e.g., 8984) to avoid conflict. [^11][^12][^13]
- **OAI-PMH** remains the primary interoperability mechanism in containerized environments. DSpace exposes OAI-PMH via the `oai` webapp; VuFind harvests via `harvest_oai.php` and `batch-import-xsl.sh`. In Docker setups, OAI-PMH endpoints are exposed through the reverse proxy or via internal container networking. [^13][^14][^15]
- **Resource requirements** vary significantly: DSpace minimal production needs ~3-4GB RAM (1GB Tomcat + 1GB PostgreSQL + OS overhead), mid-range 5-6GB, high-end 9-10GB+ with 1TB+ storage. Islandora ISLE recommends **16-32GB RAM** for production, minimum 2 CPUs, and 30-50GB OS overhead plus collection storage. Solr/Elasticsearch alone typically require 2-4GB RAM minimum. [^16][^17][^18]
- **Networking patterns** across these stacks use Docker internal networks (`dspacenet`, `isle-internal`, bridge networks) with reverse proxies (Traefik, Nginx, Apache) for TLS termination and routing. Health checks (`depends_on` with `condition: service_healthy`) are used to prevent race conditions during startup. [^1][^8][^19]
- **Security patterns** include: secrets mounted as files (Islandora `secrets/live/` directory), non-root container users, read-only root filesystems, `no-new-privileges`, TLS via Traefik/Apache, and `restart: unless-stopped` policies. [^8][^19][^20]
- **Storage patterns** use named Docker volumes for persistence (PostgreSQL data, Solr cores, Fedora repository, assetstores). Islandora supports bind mounts for large data disks. DSpace uses `docker-compose down -v` to destroy volumes, or persistent volumes for production data retention. [^1][^8][^10]
- **Migration patterns** from DSpace to Islandora often involve Python scripts using the DSpace REST API, crosswalking Dublin Core to Islandora fields, and using Islandora Workbench for CSV-based bulk ingestion. Dockerized Islandora (ISLE) was specifically chosen by some institutions to avoid OS compatibility issues (e.g., RHEL vs Ubuntu). [^21][^22]
- **Kubernetes adoption** is growing but not universal. Hyku relies on Hyrax Helm charts. DSpace has community Kubernetes experiments (e.g., Azure Container Registry deployments) but no official Helm chart. Islandora's `isle-dc` is Docker Compose-first, though Kubernetes deployment is possible with custom manifests. [^5][^23][^24]

### Major Players & Sources
- **DSpace (LYRASIS/DSpace Foundation)**: The most widely deployed open-source repository (2,000+ institutions). Provides official Docker Compose files and images, but cautions they are development-only. [^1][^3][^4]
- **Samvera Community (Hyku/Hyrax)**: Ruby on Rails ecosystem used by Yale, UCLA, British Library, Emory, and others. Hyku adds multi-tenancy to Hyrax. Offers both Docker Compose and Kubernetes (Helm) deployment paths. [^5][^6][^7][^24]
- **Islandora Foundation**: Drupal-based digital repository framework, widely used in academic libraries. ISLE (Islandora Enterprise) provides full Docker containerization. Version 8+ is a ground-up rewrite with modern microservices. [^8][^9][^10]
- **Fedora Commons**: The underlying persistence layer for Samvera and Islandora. Fedora 6 supports OCFL (Oxford Common File Layout) and is containerized in both stacks. [^7][^10]
- **VuFind (Villanova University)**: Mature PHP discovery layer with Solr. Strong integration with library ILS systems. Less containerization maturity than DSpace/Islandora. [^11][^12][^13]
- **Blacklight (Project Blacklight/Spotlight)**: Ruby on Rails discovery interface, often used with Samvera but also standalone. GeoBlacklight and Spotlight are popular extensions. [^7][^12]
- **SoftServ/Notch8 (HykuUP)**: Commercial service providers for Samvera/Hyku hosting and deployment optimization. [^6][^25]
- **Lyrasis/DSpaceDirect**: Hosts the official DSpace demo site on Docker, providing real-world validation of containerized DSpace. [^4]

### Trends & Signals
- **Containerization is now the default** for new Islandora 8+ deployments (ISLE) and increasingly common for DSpace 7+ and Hyku. The "works on my machine" problem is driving adoption, especially for distributed teams. [^21][^22][^26]
- **Separation of frontend and backend** is a strong architectural trend. DSpace 7+ explicitly splits Angular UI from Java REST API. Islandora uses Drupal as a decoupled frontend. This enables independent scaling and containerization. [^1][^2][^8]
- **Solr externalization** is mandatory in modern stacks. DSpace 7+ moved from embedded Solr 4 to standalone Solr 8+ as a prerequisite. Islandora and Hyku both run Solr as separate containers. [^3][^27]
- **Valkyrie abstraction in Samvera** allows swapping persistence backends (Fedora 6, PostgreSQL, S3) without changing application code, making containerized deployments more flexible and cloud-native. [^7][^24]
- **Kubernetes and Helm** are gaining traction for production digital repositories, but Docker Compose remains the dominant deployment tool for smaller institutions and development/staging. [^5][^23][^28]
- **Security hardening** is an emerging focus: non-root containers, read-only filesystems, dropped capabilities, secrets management, and network policies are being added to repository deployment manifests. [^19][^20][^28]
- **OAI-PMH and REST APIs** remain critical for interoperability between containerized services. DSpace's REST API is the foundation for the Angular UI, while OAI-PMH enables cross-repository harvesting. [^13][^14][^15]

### Controversies & Conflicting Claims
- **"Production-ready" Docker images**: DSpace core developers explicitly state their official Docker images are **not production-ready** and recommend building custom images. However, LYRASIS/DSpaceDirect runs production demo sites using these same images, creating ambiguity for adopters. [^3][^4]
- **Fedora vs PostgreSQL for metadata**: The Samvera community has moved toward Valkyrie adapters that allow PostgreSQL to replace Fedora for metadata storage, while Fedora remains for file storage. Some purists argue this diminishes Fedora's role as a linked-data repository; pragmatists argue it improves performance and simplifies operations. [^7][^24]
- **Islandora 7 vs 8 migration**: The jump from Islandora 7 to 8 is so large (complete architectural rewrite) that some institutions view it as a new implementation rather than an upgrade. Texas State University chose to migrate from DSpace to Islandora 8 rather than face the DSpace 7 upgrade, but found Docker/Drupal to be new technologies requiring unexpected learning time. [^21][^22]
- **Kubernetes vs Docker Compose**: Enterprise and DevOps teams prefer Kubernetes for production, but many library IT departments lack K8s expertise. Hyku's Helm charts exist but are considered complex; DSpace has no official K8s support. Docker Compose is often the pragmatic choice for academic institutions. [^5][^23][^28]
- **Resource overhead**: Some argue that containerized stacks (especially Islandora with 10+ services) are too heavy for small institutions. Islandora ISLE requires 16-32GB RAM for production, while a minimal DSpace instance can run on 3-4GB. The trade-off between feature richness and operational cost is debated. [^16][^17][^18]

### Recommended Deep-Dive Areas
- **DSpace custom Docker image production pipeline**: Given the official images' "not production-ready" warning, BUET should investigate building hardened DSpace images with multi-stage builds, non-root users, vulnerability scanning, and pinned base images. This warrants depth because DSpace is the most mature repository option and aligns with BUET's E-Library goals. [^3][^19][^20]
- **Islandora ISLE multi-service orchestration**: The ISLE stack (Drupal, Fedora, Solr, Blazegraph, ActiveMQ, Cantaloupe, Traefik) is the most complex but also the most complete containerized reference. Studying its `docker-compose.yml` generation, S6 Overlay service supervision, and secrets management would provide a template for BUET's own multi-service stack. [^8][^9][^10]
- **Hyku multi-tenancy and Kubernetes Helm charts**: If BUET needs to host multiple departmental libraries under one infrastructure, Hyku's multi-tenant architecture and Helm charts are relevant. The Hyrax Helm chart structure and `ops/review-deploy.tmpl.yaml` should be examined. [^5][^6][^28]
- **OAI-PMH harvesting in containerized environments**: Since BUET plans to run both a repository (DSpace/Islandora) and a discovery layer (Drupal/VuFind), understanding how to expose and harvest OAI-PMH endpoints between containers (networking, cron jobs, volume mounts for harvested data) is operationally critical. [^13][^14][^15]
- **Elasticsearch/Solr container resource planning**: BUET's stack explicitly includes Elasticsearch. Understanding JVM heap sizing, `vm.max_map_count` requirements, volume persistence for indexes, and backup/restore procedures for Solr/Elasticsearch in Docker is essential for performance and data durability. [^27][^29]
- **Migration tooling from DSpace to Drupal/Islandora**: If BUET considers future migration or integration, tools like Islandora Workbench (CSV bulk import), Python REST API scripts, and metadata crosswalks (Dublin Core to Drupal fields) should be evaluated. [^21][^22]

### References

[^1]: DSpace/dspace-angular GitHub Repository. "DSpace User Interface built on Angular." https://github.com/DSpace/dspace-angular

[^2]: DSpace/DSpace GitHub Repository. "Docker Compose files for DSpace Backend." https://github.com/DSpace/DSpace/blob/main/dspace/src/main/docker-compose/README.md

[^3]: Fossies Archive. "DSpace 8.1 docker-compose/README.md." https://fossies.org/linux/DSpace-dspace/dspace/src/main/docker-compose/README.md

[^4]: DSpace.org. "New Demo Site for DSpace (Docker-based platform)." 2023-08-25. https://dspace.org/22762-2/

[^5]: samvera/hyku GitHub Repository. "Getting Started with Hyku." https://github.com/samvera/hyku/blob/main/docs/getting-started.md

[^6]: SoftServ. "Samvera Repository Solutions / HykuUP." https://softserv.scientist.com/service/samvera-repository-solutions/

[^7]: Samvera Wiki. "The Hyrax and Hyku Technology Stack." https://samvera.atlassian.net/wiki/x/u4Cch

[^8]: Islandora-Devops/isle-dc GitHub Repository. "ISLE 8 - Dockerized Islandora 8 Deployment." https://github.com/Islandora-Devops/isle-dc/

[^9]: Islandora-Devops/isle-buildkit GitHub Repository. "Docker images for Islandora." https://github.com/islandora-Devops/isle-buildkit

[^10]: Islandora Documentation. "Docker Modifications - Site Template." https://islandora.github.io/documentation/installation/docker/site-template/docker-modifications/

[^11]: VuFind Documentation. "Installation: Notes." https://vufind.org/wiki/installation:notes

[^12]: ResearchGate. "TFM Repositorio Digital con DSPACE y VUFIND." 2022-06-28. https://www.researchgate.net/publication/362429737

[^13]: VuFind Wiki. "Administration: Fault Tolerance and Load Balancing (MariaDB Galera, SolrCloud)." https://vufind.org/wiki/administration:fault_tolerance_and_load_balancing

[^14]: EIFL. "How to make your OA repository work really well - OAI-PMH checklist." July 2019. https://www.eifl.net/system/files/resources/201907/repositories_checklist_july_2019__0.pdf

[^15]: IJLIS. "Harvesting Full-Text and Metadata of OpenDOAR through DSpace OAI-PMH." https://www.ijlis.org/articles/harvesting-full-text-and-metadata-of-opendoar-through-dspace-oaipmh

[^16]: Unirepos. "Minimal DSpace System Requirements." 2021-06-30. https://www.unirepos.com/en_US/blog/our-blog-1/minimal-dspace-system-requirements-110

[^17]: EIFL. "DSpace Installation - Hardware Requirements." https://www.eifl.net/system/files/resources/201604/eifl_-_01_-_dspace_installation.pdf

[^18]: Islandora Collaboration Group. "ISLE Hardware Requirements." https://islandora-collaboration-group.github.io/ISLE/install/host-hardware-requirements/

[^19]: mykolaaleksandrov.dev. "Docker Production Best Practices: Security, Optimization & Monitoring." 2026-02-12. https://mykolaaleksandrov.dev/posts/2026/02/docker-production-best-practices/

[^20]: blog.ploetzli.ch. "Docker Deployment Best Practices." 2024-08-01. https://blog.ploetzli.ch/2024/docker-deployment-best-practices/

[^21]: TDL IR. "Migration from Dspace to Islandora version 8 (Todd Peters, Texas State University)." https://tdl-ir.tdl.org/bitstreams/81be4436-c291-4821-8b4c-0fc28e70c568/download

[^22]: ILRI GitHub. "dspace-drupal-module (CGSpace importer for Drupal)." https://github.com/ilri/dspace-drupal-module

[^23]: Dspace7-Kubernetes GitHub. "DSpace 7 Kubernetes deployment." https://github.com/Deunitato/Dspace7-Kubernetes

[^24]: Emory University / Fedora Repository. "Emory's Migration to Fedora 6 with Hyrax." 2025-04-17. https://fedorarepository.org/fedora-implementations-emory-university-libraries/

[^25]: Notch8. "Self-Hosting vs Managed Repositories: Hyrax, Hyku and HykuUP." 2025-08-29. https://www.notch8.com/post/self-hosting-vs-managed-repositories-hyrax-hyku-and-hykuup-explained

[^26]: August Infotech. "CI/CD for Enterprise Drupal: Offshore Implementation Guide." 2025-08-13. https://www.augustinfotech.com/podcast/ci-cd-for-enterprise-drupal-offshore-implementation-guide-for-2025/

[^27]: LYRASIS Wiki. "Upgrading Solr Server for DSpace / DSpace 7 Upgraded from Solr 4 to Solr 7." https://wiki.lyrasis.org/display/DSPACE/Upgrading+Solr+Server+for+DSpace

[^28]: WeKnora GitHub Issue #478. "Add Helm chart for Kubernetes deployment." 2025-12-24. https://github.com/Tencent/WeKnora/issues/478

[^29]: elk-docker ReadTheDocs. "Elasticsearch Docker Prerequisites (4GB RAM, vm.max_map_count)." https://elk-docker.readthedocs.io/

[^30]: DSpace-Labs/DSpace-Docker-Images. "Docker Compose Startup Options (DSpace 4-7)." https://github.com/DSpace-Labs/DSpace-Docker-Images/blob/master/docker-compose-files/dspace-compose/ComposeFiles.md
