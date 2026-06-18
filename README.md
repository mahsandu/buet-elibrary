# BUET E-Library V4

BUET E-Library V4 is a modern, containerized digital library discovery platform for Bangladesh University of Engineering and Technology (BUET). It unifies search across Koha (physical collections) and DSpace (digital theses/repositories) using Elasticsearch, Drupal 11, and Python microservices.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                     Host Machine                        │
│  ┌─────────────┐                                        │
│  │   Nginx     │  Port 80 / 443 (Public)                │
│  │  (Alpine)   │◄───────── Users / Admins               │
│  └──────┬──────┘                                        │
│         │                                               │
│  ┌──────┴──────┐    ┌──────────────┐   ┌──────────┐   │
│  │   Drupal    │◄──►│ Elasticsearch│   │  Redis   │   │
│  │  11-fpm     │    │   8.10.2     │   │  7-alpine│   │
│  └──────┬──────┘    └──────────────┘   └──────────┘   │
│         │                                              │
│  ┌──────┴──────┐    ┌────────────────┐                 │
│  │   MariaDB   │    │  Microservices │                 │
│  │   10.6      │    │  (Python)      │                 │
│  └─────────────┘    └────────────────┘                 │
│                                                         │
│  Networks: elib_network (internal) + elib_public        │
└─────────────────────────────────────────────────────────┘
```

- **Nginx**: Reverse proxy and SSL termination. Only public-facing service.
- **Drupal 11**: Discovery frontend and CMS. Queries Elasticsearch for search.
- **Elasticsearch 8.10.2**: Unified search index for Koha + DSpace metadata.
- **MariaDB 10.6**: Drupal's relational database.
- **Python Microservices**: OAI-PMH harvesters, live OPAC scrapers, and ETL pipelines.
- **Redis 7**: TTL cache for live scraper status to avoid hammering the Koha OPAC.

---

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 1.29+ (or `docker compose` v2+)
- **8 GB RAM minimum** (Elasticsearch allocates 2 GB heap; Drupal + MariaDB need ~2 GB)
- Git
- Optional: OpenSSL for generating self-signed certificates

---

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/buet/elibrary-v4.git
   cd elibrary-v4
   ```

2. Copy and configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your real credentials and OAI-PMH endpoints
   ```

3. Start the stack:
   ```bash
   docker-compose up -d
   # or: docker compose up -d
   ```

4. Verify services:
   ```bash
   docker-compose ps
   curl http://localhost/health
   curl http://localhost:9200/_cluster/health
   ```

5. Install Drupal (first run only):
   - Visit `http://localhost` and follow the Drupal installer.
   - Use the MariaDB credentials from `.env`.

---

## Service Descriptions

| Service | Image | Role | Ports |
|---|---|---|---|
| `nginx` | `nginx:alpine` | Reverse proxy, static file serving, SSL | 80, 443 |
| `drupal` | `drupal:11-fpm` | Discovery frontend, CMS, search UI | — (internal) |
| `elasticsearch` | `elasticsearch:8.10.2` | Full-text search index, faceted queries | — (internal) |
| `mariadb` | `mariadb:10.6` | Drupal database, user sessions, config | — (internal) |
| `microservices` | Build from `./microservices` | OAI-PMH harvest, ETL, live status scraping | — (internal) |
| `redis` | `redis:7-alpine` | Scraped status cache with TTL | — (internal) |

---

## OAI-PMH Harvester Setup

Before harvesting metadata, ensure your source systems expose OAI-PMH:

### Koha

1. Enable OAI-PMH in Koha Administration:
   - **System preference**: `OAI-PMH` → set to `Enable`.
   - Define `OAI-PMH:AutoUpdate` and `OAI-PMH:MaxCount` as needed.
2. Verify the endpoint:
   ```
   https://<koha-host>/cgi-bin/koha/oai.pl?verb=Identify
   ```
3. If Koha uses a self-signed certificate, set `VERIFY_SSL=false` in `.env`.

### DSpace

1. Enable OAI-PMH in `dspace.cfg` (or `local.cfg`):
   ```properties
   oai.enabled = true
   oai.url = ${dspace.server.url}/oai
   ```
2. Restart Tomcat / DSpace backend.
3. Verify:
   ```
   https://<dspace-host>/oai/request?verb=Identify
   ```

### Running the Harvester

The microservices container exposes harvester endpoints. Trigger a full harvest:
```bash
curl -X POST http://microservices:5000/harvest \
  -H "Content-Type: application/json" \
  -d '{"source":"koha","from":"2024-01-01"}'
```

---

## Elasticsearch Index Initialization

1. Wait for Elasticsearch to be healthy:
   ```bash
   docker-compose exec elasticsearch curl -s http://localhost:9200/_cluster/health
   ```

2. Create the initial index and mapping (run from microservices or locally):
   ```bash
   curl -X PUT "http://localhost:9200/buet_catalog" \
     -H "Content-Type: application/json" \
     -d @research/es_mapping.json
   ```
   *(If `es_mapping.json` is provided by the Research/Backend worker.)*

3. The harvester microservice will populate documents automatically after the first run.

---

## Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| `Elasticsearch exited with code 78` | `vm.max_map_count` too low | `sudo sysctl -w vm.max_map_count=262144` |
| Drupal shows "Database connection error" | MariaDB not ready or wrong credentials | Check `docker-compose logs mariadb` and `.env` values |
| `docker-compose config` fails with build error | `./microservices` has no Dockerfile | Add a `Dockerfile` in `microservices/` (owned by Backend worker) |
| Nginx returns 502 Bad Gateway | Drupal PHP-FPM not listening | Verify `drupal` container is running and on `elib_network` |
| Live status never updates | Scraper cache is stale | `docker-compose exec redis redis-cli FLUSHDB` |
| Koha harvest fails with SSL error | Self-signed cert blocked | Set `VERIFY_SSL=false` in `.env` |

---

## Security Notes

- **Development**: SSL is disabled/self-signed, Elasticsearch has `xpack.security.enabled=false`, and Drupal debug mode may be on. Do **not** expose port 9200 to the public internet.
- **Production**:
  - Enable Elasticsearch security (native users + TLS).
  - Replace self-signed certificates with Let's Encrypt or institutional CA certs.
  - Move secrets out of `.env` into a Docker secret manager or vault.
  - Restrict Nginx to TLS 1.2+ and strong cipher suites.
  - Run `docker-compose exec drupal drush cr` to clear caches after config changes.

---

## Research Summary

The V4 architecture was informed by cross-dimensional analysis of **six international library platforms and ecosystems**:

1. **VuFind** (Villanova) — The most widely deployed open-source discovery layer; primary reference for OAI-PMH → Solr/ES indexing patterns.
2. **Blacklight** (Stanford/UVA) — Highly customizable Rails-based engine; studied for its minimal, API-first skeleton.
3. **Aspen Discovery** (ByWater) — VuFind fork with strong e-content and mobile support; evaluated for public-library-style features.
4. **FOLIO** (Open Library Foundation) — Cloud-native LSP with microservices; assessed for long-term backend migration potential.
5. **DSpace** (LYRASIS/MIT) — Institutional repository platform; OAI-PMH provider for digital theses.
6. **Koha** (Koha Community) — Dominant open-source ILS; physical collection backend and OAI-PMH source.

Key takeaways: BUET adopts an **external harvester pattern** (Python → Elasticsearch → Drupal) to avoid forcing Drupal to index massive MARC/DC catalogs directly. This pattern is proven in production by OARepo, MIT Libraries, and CORE.

---

## License

This project is developed for Bangladesh University of Engineering and Technology (BUET). Internal use only unless otherwise specified.
