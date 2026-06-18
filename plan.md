# BUET E-Library Platform — Execution Plan

**Objective:** Build a full technical implementation scaffold for the BUET E-Library V4 platform, grounded in research of international reference architectures.

**Anchor Date:** 2026-06-18  
**Workspace:** `D:\BUET\elibrary\buet-elibrary`

---

## Stage 1 — Research: International E-Library Platforms
**Skill:** `deep-research-swarm` (Route A: Wide Search)  
**Goal:** Discover and document 5–8 international e-library / digital discovery platforms that use similar architectural patterns (Elasticsearch/Solr, decoupled CMS, OAI-PMH harvesters, microservices, containerized deployment). Extract design patterns, technology stacks, and lessons learned.

**Research Dimensions (tentative, to be refined after Phase 1W):**
1. Open-source discovery layer platforms (e.g., VuFind, Blacklight, FOLIO)
2. Commercial/enterprise discovery platforms (e.g., EBSCO Discovery Service, Primo, Summon)
3. Containerized academic repository stacks (e.g., DSpace-GLAM, Samvera, Islandora)
4. OAI-PMH + ETL + search index architectures
5. Drupal + Elasticsearch integration patterns in libraries
6. Live OPAC scraping / availability proxy patterns
7. E-resource proxy and authentication workflows (EZproxy, Shibboleth, OpenAthens)
8. Microservices orchestration in library environments (Docker Compose, K8s)
9. Koha + Elasticsearch integration projects (Koha ES plugin, external indexing)
10. Institutional repository discovery interfaces (DSpace + Elasticsearch experiments)

**Output:** All research artifacts saved under `D:\BUET\elibrary\buet-elibrary\research\`

---

## Stage 2 — Implementation: Full Project Scaffolding
**Skill:** `swarm-coding` (multi-agent mode)  
**Goal:** Generate the complete, runnable project scaffold based on the V4 proposal and implementation guide, incorporating lessons from Stage 1 research.

**Deliverables:**
1. `docker-compose.yml` — Complete orchestration (ES, Drupal + MariaDB, Nginx, microservices)
2. `microservices/` directory — Python ETL harvesters + Live Status API
3. `elasticsearch/` — Index initialization schema + setup script
4. `drupal/` — Drupal configuration notes / scaffold
5. `nginx/` — Reverse proxy configuration
6. `.env.example` — Environment variables template
7. `README.md` — Setup and deployment guide

**Quality gates:**
- Docker Compose must be valid and complete (no missing services like DB)
- Python scripts must include proper error handling, logging, and SSL bypass
- XSS risk in live_status.py must be mitigated (structured text extraction, not raw HTML passthrough)
- All paths must be relative and workspace-contained

---

## Stage 3 — Validation & Integration
**Goal:** Verify all files are present, syntactically correct, and consistent with the V4 architecture.

**Checks:**
- `docker-compose config` validation
- Python syntax check (`python -m py_compile`)
- JSON/YAML schema validation
- README completeness
- Integration of research findings into recommendations

---

## Progressive Skill Loading
- Stage 1 begins: load `deep-research-swarm`
- Stage 2 begins: load `swarm-coding`
- No skills loaded before their stage starts.
