# AGENT_SPEC: BUET E-Library V4 Implementation

## User Goal
Build a complete, runnable project scaffold for the BUET E-Library V4 platform based on the research-validated architecture.

## Shared Contract

### Stack & Technology Choices
- **Orchestration:** Docker Compose 3.8
- **Discovery Engine:** Elasticsearch 8.10.2 (single-node for V4, `xpack.security.enabled=false` for development)
- **CMS/Frontend:** Drupal 11 (PHP-FPM, requires MariaDB 10.6+)
- **Reverse Proxy:** Nginx (Alpine, SSL termination, public exposure)
- **Microservices:** Python 3.11 (Alpine) with requests, beautifulsoup4, sickle, redis, flask
- **Cache:** Redis 7 (Alpine) for scraper status caching and Drupal cache
- **Network:** `elib_network` (bridge), all internal services communicate here
- **Workspace:** `D:\BUET\elibrary\buet-elibrary` (Git Bash: `/d/BUET/elibrary/buet-elibrary`)

### Critical Design Decisions (from Research)
1. **MariaDB is required** — Drupal 11 needs a relational database. The original V4 proposal omitted this.
2. **Redis is required** — For live scraper caching (TTL 10 min) and optional Drupal cache.
3. **Nginx is required** — Only the frontend is exposed publicly; all other services are internal.
4. **External Harvester Pattern** — Python microservices populate ES directly; Drupal only queries ES (read-only).
5. **XSS Mitigation** — `live_status.py` returns structured JSON, never raw HTML. Drupal renders via template.
6. **Source-prefixed IDs** — `koha_{biblionumber}` and `dspace_{handle}` to prevent collisions.
7. **Fingerprint for deduplication** — MD5 of normalized title+author+year to flag duplicates in UI.
8. **E-resource proxy deferred to Phase 2** — Focus on discovery layer first.

### File Ownership
- **Infrastructure Worker** (`docker-compose.yml`, `.env.example`, `nginx/`, `README.md`)
- **Microservices Worker** (`microservices/` — all Python scripts, Dockerfile, requirements.txt, cron config)
- **Search & CMS Worker** (`elasticsearch/` — schema + setup script; `drupal/` — config notes)

### Validation
- `docker-compose config` must be valid
- `python -m py_compile` must pass for all .py files
- JSON/YAML must be valid
- README must be complete with setup instructions

## Forbidden Areas
- Do not modify files in `research/` or `plan.md`
- Do not use absolute paths outside the workspace
- Do not install dependencies outside the managed runtime
- Do not expose Elasticsearch port 9200 publicly (internal only)
