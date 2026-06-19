# BUET E-Library V4

BUET E-Library V4 is a modern, containerized digital library discovery platform for Bangladesh University of Engineering and Technology (BUET). It unifies search across Koha (physical collections) and DSpace (digital theses/repositories) using Elasticsearch, Drupal 11, and Python microservices.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                     Host Machine                        │
│  ┌─────────────┐   ┌─────────────┐                      │
│  │   Nginx     │   │   Proxy     │                      │
│  │  (Alpine)   │   │  (Alpine)   │                      │
│  │  Port 80/443│   │  Port 8080  │                      │
│  └──────┬──────┘   └─────────────┘                      │
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
   curl http://localhost:8080/health
   ```

5. Install Drupal (first run only):
   - Visit `http://localhost` and follow the Drupal installer.
   - Use the MariaDB credentials from `.env`.

---

## Service Descriptions

| Service | Image | Role | Ports |
|---|---|---|---|
| `proxy` | `nginx:alpine` | E-resource proxy for off-campus database access | 8080 |
| `federated` | Build from `./microservices` | Federated search gateway (external DB APIs) | — (internal) |
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

## E-Resource Proxy (Off-Campus Access)

The proxy service provides **off-campus access** to subscribed databases (IEEE, Elsevier, JSTOR, Springer, Wiley, ACM) by forwarding requests through the university's institutional IP range. It is a **self-hosted, free alternative** to commercial proxies like EZproxy or OpenAthens.

### Supported Databases

| Proxy Path | Database | URL |
|---|---|---|
| `/ieee/` | IEEE Xplore | `https://ieeexplore.ieee.org` |
| `/elsevier/` | Elsevier ScienceDirect | `https://www.sciencedirect.com` |
| `/jstor/` | JSTOR | `https://www.jstor.org` |
| `/springer/` | SpringerLink | `https://link.springer.com` |
| `/wiley/` | Wiley Online Library | `https://onlinelibrary.wiley.com` |
| `/acm/` | ACM Digital Library | `https://dl.acm.org` |

### Setup

1. **Generate user credentials** (one time):
   ```bash
   python proxy/generate_htpasswd.py buetadmin mysecurepassword
   # Copy the output line into proxy/.htpasswd
   ```

2. **Start the proxy** (included in the stack):
   ```bash
   docker-compose up -d proxy
   ```

3. **Verify**:
   ```bash
   curl http://localhost:8080/health
   # Expected: proxy-healthy
   ```

4. **Access a database** (authenticated):
   ```bash
   curl -u buetadmin:mysecurepassword http://localhost:8080/ieee/
   ```

### HTTPS (Production)

For production, obtain a free certificate via Let's Encrypt:
```bash
sudo certbot certonly --standalone -d proxy.buet.ac.bd
# Mount the certificates into the proxy container (see proxy/README.md)
```

### Comparison with Commercial Proxies

| Feature | Nginx Proxy | EZproxy | OpenAthens |
|--------|-------------|---------|------------|
| Cost | Free | ~$100/mo or license | SaaS subscription |
| URL Rewriting | `sub_filter` (basic) | Full (comprehensive) | Cloud-managed |
| Auth | Basic Auth | LDAP, SAML, OAuth | SAML SSO |
| Best For | 6-10 databases | 20+ databases | Enterprise |

**Full documentation:** [`proxy/README.md`](proxy/README.md)

---

## Federated Search (Global Scholarly Content)

The **Federated Search Gateway** queries external scholarly databases in parallel and merges results with the local unified index (Elasticsearch). This provides BUET users with access to global research beyond institutional holdings.

### Architecture

```
User Query → Drupal → Federated Gateway → Crossref + OpenAlex + CORE + IEEE + Elsevier
                                      → Results merged and deduplicated by DOI
                                      → Displayed alongside local Koha/DSpace results
```

### Supported Sources

| Source | API | Free? | Key Required? |
|--------|-----|-------|---------------|
| **Crossref** | `https://api.crossref.org/works` | Yes | No |
| **OpenAlex** | `https://api.openalex.org/works` | Yes | No |
| **CORE** | `https://api.core.ac.uk/v3/search/works` | Yes | Free key |
| **IEEE Xplore** | `https://ieeexplore.ieee.org/gateway/inspec/api` | Limited | Yes |
| **Elsevier Scopus** | `https://api.elsevier.com/content/search/scopus` | Limited | Yes |

### Quick Start

1. **Enable free sources** (no configuration needed):
   ```bash
   # Crossref and OpenAlex are enabled by default
   curl "http://localhost:5002/api/federated/search?q=machine+learning&limit=5"
   ```

2. **Add CORE API key** (optional, free):
   - Register at https://core.ac.uk/services/api
   - Add to `.env`: `CORE_API_KEY=your-key`

3. **Add IEEE / Elsevier** (optional, requires institutional keys):
   - IEEE: https://developer.ieee.org/
   - Elsevier: https://dev.elsevier.com/
   - Add to `.env`:
     ```bash
     IEEE_API_KEY=your-ieee-key
     ELSEVIER_API_KEY=your-elsevier-key
     ```

### API Endpoints

```bash
# Search all enabled sources
curl "http://localhost:5002/api/federated/search?q=machine+learning&limit=5"

# Search specific sources
curl "http://localhost:5002/api/federated/search?q=machine+learning&sources=crossref,openalex"

# List available sources
curl "http://localhost:5002/api/federated/sources"
```

### Integration with Drupal

The federated search results can be displayed alongside local Elasticsearch results via:

1. **Custom Drupal Controller** — calls the gateway and renders themed output
2. **JavaScript Meta-Search** — queries APIs directly from the browser (CORS limitations apply)
3. **React/Vue Component** — decoupled frontend that queries both ES and federated APIs in parallel

**Full documentation:** [`docs/federated_search_guide.md`](docs/federated_search_guide.md)

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
| Proxy asks for login but rejects credentials | `.htpasswd` file is empty or missing | Run `python proxy/generate_htpasswd.py <user> <pass>` and append to `proxy/.htpasswd` |
| Proxy images/CSS not loading | URL rewriting missed asset domains | Add `sub_filter` directives for the missing domain in `proxy/nginx-proxy.conf` |
| Database says "not authorized" through proxy | IP not in institutional range | Ensure the proxy server is hosted on a BUET network IP |
| Proxy returns 502/504 | Upstream database is blocking the proxy | Check `proxy_cookie_domain` and `proxy_set_header` settings |

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
