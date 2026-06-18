# Drupal Configuration Guide — BUET E-Library V4

This guide covers installing, configuring, and securing Drupal 11 as the search and CMS frontend for the BUET E-Library.

---

## 1. Drupal 11 Installation

### Option A: Composer-based (recommended for custom modules)

```bash
cd /var/www/html
drush site:install standard \
  --db-url='mysql://drupal:drupal_password@mariadb:3306/drupal_db' \
  --site-name='BUET E-Library' \
  --account-name=admin \
  --account-pass=admin_password
```

Or using Composer inside the container:

```bash
composer create-project drupal/recommended-project:11.x drupal
cd drupal
composer require drush/drush
```

### Option B: Official Drupal Docker Image

```yaml
# docker-compose.yml snippet
  drupal:
    image: drupal:11-apache
    volumes:
      - drupal_modules:/var/www/html/modules
      - drupal_profiles:/var/www/html/profiles
      - drupal_themes:/var/www/html/themes
      - drupal_sites:/var/www/html/sites
    ports:
      - "8080:80"
    depends_on:
      - mariadb
```

After first run, copy `sites/default/default.settings.php` to `sites/default/settings.php`, set write permissions, and run the web installer.

---

## 2. Database Setup (MariaDB)

Create the database and user before installing Drupal:

```sql
CREATE DATABASE drupal_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'drupal'@'%' IDENTIFIED BY 'drupal_password';
GRANT ALL PRIVILEGES ON drupal_db.* TO 'drupal'@'%';
FLUSH PRIVILEGES;
```

Connection string for Drupal:

```php
$databases['default']['default'] = [
  'database' => 'drupal_db',
  'username' => 'drupal',
  'password' => 'drupal_password',
  'prefix' => '',
  'host' => 'mariadb',
  'port' => '3306',
  'driver' => 'mysql',
  'charset' => 'utf8mb4',
  'collation' => 'utf8mb4_general_ci',
];
```

---

## 3. Search API Configuration

### 3.1 Install Required Modules

```bash
composer require drupal/search_api drupal/elasticsearch_connector drupal/facets
```

Enable via Drush or Admin UI:

```bash
drush en search_api elasticsearch_connector facets -y
```

### 3.2 Create Search API Server

1. Navigate to **Configuration > Search and metadata > Search API**.
2. Click **Add server**.
3. Name: **BUET Elasticsearch**
4. Backend: **Elasticsearch**
5. Cluster URL: `http://elasticsearch:9200`
6. Save.

### 3.3 Create Search API Index

1. Click **Add index**.
2. Name: **Unified Catalog**
3. Datasource: **External index** (if available) or **Custom** (see fallback below).
4. Server: **BUET Elasticsearch**
5. Index name: `buet_unified_catalog` (or alias `buet_search`).

Map the fields from the Elasticsearch mapping to Drupal fields:

| Drupal Field | ES Field | Type |
|--------------|----------|------|
| Title | `title` | Text |
| Creator | `creator` | Text |
| Subjects | `subjects` | Keyword (multi-value) |
| Format | `format_type` | Keyword |
| Publish Date | `publish_date` | Date |
| Source | `source_system` | Keyword |
| Link | `target_uri` | Keyword (URL) |

### 3.4 Fallback: Custom JSON/HTTP Approach (CRITICAL)

> **Elasticsearch Connector** may not yet support Elasticsearch 8.x + Drupal 11. If you encounter compatibility errors, use the fallback architecture documented below.

**Architecture:**
- Drupal **does not** index directly into Elasticsearch.
- Python harvesters populate `buet_unified_catalog` (external process).
- Drupal queries ES via a **custom REST route** or **custom Search API datasource** that sends raw HTTP JSON to `http://elasticsearch:9200/buet_unified_catalog/_search`.

**Implementation sketch:**

1. Create a custom module `buet_elibrary` (see `custom_module_notes.md`).
2. Implement a controller `BuetSearchController` that accepts a query string, forwards it to ES, and returns formatted results.
3. Expose the route as `/api/search` or use it inside a custom Search API datasource plugin.
4. Render results using a Drupal View that calls this custom endpoint, or build a custom page with Twig templates.

> **Benefits:** Decouples Drupal from ES client libraries; any ES version works as long as the HTTP API is stable.

---

## 4. Faceted Navigation

Install and configure the **Facets** module:

```bash
drush en facets -y
```

### Create Facet Sources

1. Go to **Configuration > Search and metadata > Facets**.
2. Add facets tied to the **Unified Catalog** Search API index.
3. Available facets:
   - `format_type` — "Physical Book" vs "Digital Thesis/Article"
   - `subjects` — list of subject keywords
   - `publish_date` — date range or year histogram
   - `source_system` — "koha" vs "dspace"

### Place Facet Blocks

1. Go to **Structure > Block layout**.
2. Place each facet block into a sidebar region (e.g., **Sidebar first**).
3. Configure visibility so blocks appear only on the search page.

---

## 5. Live Status Integration

The live availability status (checked-out, on-shelf, etc.) is served by a microservice (`live_status.py`). Drupal must call this service safely and render the response via template (not raw HTML injection).

### Front-End Pattern

In your Twig template (e.g., for a search result or node display), output a placeholder `<div>` with a `data-biblio` attribute:

```html
<div id="live-status" data-biblio="{{ biblionumber }}">
  <span class="status-loading">Checking availability...</span>
</div>
```

### JavaScript Behavior

Attach a Drupal behavior that reads `data-biblio` and makes an AJAX call to the microservice endpoint (proxied through Drupal or directly if CORS allows). See `custom_module_notes.md` for the full JS snippet.

### Back-End Proxy (Optional)

If the microservice is not exposed publicly, create a Drupal route that forwards the request:

```php
// Route: /buet/live-status/{biblionumber}
// Controller fetches JSON from http://live_status:5000/status/{biblionumber}
// Returns JSON to the browser
```

This keeps the microservice URL internal and adds Drupal caching if desired.

### XSS Mitigation

- The microservice must return **JSON only** (`Content-Type: application/json`).
- Drupal renders the JSON in Twig using `|escape` or `|json_encode` filters.
- Never use `.html()` or `innerHTML` with the raw response; update text nodes or use a safe template rendering library.

---

## 6. E-Resource Module (Phase 2)

Create a content type **Subscribed Database** for e-resources (IEEE, Elsevier, ACM, etc.):

### Content Type Fields

| Field | Type | Description |
|-------|------|-------------|
| Title | Text | Database name |
| Provider | Taxonomy term | IEEE, Elsevier, Springer, etc. |
| Access URL | Link | Direct link or proxy URL |
| Subject Areas | Taxonomy term | Engineering, CSE, EEE, etc. |
| Description | Long text | Usage notes |
| Logo | Image | Provider logo |

### Taxonomy Vocabularies

- **E-Resource Providers** — IEEE Xplore, ScienceDirect, SpringerLink, etc.
- **Subject Areas** — aligned with BUET departments

### Proxy Links

Store institutional proxy prefixes (e.g., `https://login.buet.ac.bd/login?url=`) and prepend them dynamically when rendering the link, or store the full proxied URL in the field.

---

## 7. Security Notes

### Admin Path Protection

Keep Drupal admin paths (`/admin`, `/user/login`, `/user/register`) behind Nginx or an upstream reverse proxy. Example Nginx snippet:

```nginx
location ~ ^/(admin|user) {
    # Restrict by IP if desired
    # allow 10.0.0.0/8;
    # deny all;

    proxy_pass http://drupal:8080;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

### HTTPS

- Terminate TLS at Nginx.
- Set `trusted_host_patterns` in `settings.php`:

```php
$settings['trusted_host_patterns'] = [
  '^elibrary\.buet\.ac\.bd$',
];
```

- Enable HSTS headers in Nginx.

### Module Updates

- Pin module versions in `composer.json`.
- Run `composer update` inside a test container before production.
- Subscribe to Drupal security advisories (https://www.drupal.org/security).
- Use `drush pm:security` to check for known vulnerabilities.

---

## Quick Reference

| Task | Drush / Command |
|------|-----------------|
| Clear cache | `drush cr` |
| Enable module | `drush en module_name -y` |
| Export config | `drush cex -y` |
| Import config | `drush cim -y` |
| Check ES status | `curl http://elasticsearch:9200/_cluster/health` |
| Check index mapping | `curl http://elasticsearch:9200/buet_unified_catalog/_mapping` |

---

*Maintained by the Search & CMS Worker — BUET E-Library V4*
