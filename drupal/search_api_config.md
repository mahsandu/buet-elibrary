# Search API Configuration — Step-by-Step

This document provides precise, copy-pasteable steps for configuring Drupal Search API to use the `buet_unified_catalog` Elasticsearch index.

---

## 1. Install Modules

Run inside the Drupal container or host with Composer:

```bash
composer require drupal/search_api drupal/elasticsearch_connector drupal/facets
```

Enable with Drush:

```bash
drush en search_api elasticsearch_connector facets -y
drush cr
```

Or enable via the Admin UI:
- **Extend > List** — check *Search API*, *Elasticsearch Connector*, *Facets*, then click **Install**.

---

## 2. Create a Search API Server

1. Go to **Configuration > Search and metadata > Search API** (`/admin/config/search/search-api`).
2. Click **Add server**.
3. Fill the form:
   - **Server name:** `BUET Elasticsearch`
   - **Backend:** `Elasticsearch` (from the *Elasticsearch Connector* module)
   - **Cluster:** `http://elasticsearch:9200`
   - **Optional:** Set timeout to `30` seconds if the network is slow.
4. Click **Save**.

Verify connectivity: the server status should show a green checkmark. If it fails, check that the Elasticsearch container is reachable from Drupal (`docker exec drupal curl http://elasticsearch:9200`).

---

## 3. Create a Search API Index

1. On the Search API page, click **Add index**.
2. Fill the form:
   - **Index name:** `Unified Catalog`
   - **Datasource(s):**
     - If *Elasticsearch Connector* exposes an **External index** datasource, select it.
     - Otherwise, select **Content** (or **Custom** if you are building the fallback module) and adjust later.
   - **Server:** `BUET Elasticsearch`
3. If using the *External index* datasource, set the index machine name to `buet_unified_catalog` (or `buet_search` if using the alias).
4. Save and proceed to **Fields**.

---

## 4. Map Fields

On the index **Fields** tab, add the following fields (use the **Add fields** button) and map them to the Elasticsearch properties:

| Label | Machine name | Type | ES Property | Notes |
|-------|--------------|------|-------------|-------|
| Title | `title` | Text | `title` | Full-text searchable |
| Creator | `creator` | Text | `creator` | Multi-value if several authors |
| Subjects | `subjects` | Text (Keyword) | `subjects` | Keyword array; use as facet |
| Format Type | `format_type` | Text (Keyword) | `format_type` | Facet: "Physical Book" / "Digital Thesis/Article" |
| Publish Date | `publish_date` | Date | `publish_date` | Use for range filters |
| Source System | `source_system` | Text (Keyword) | `source_system` | Facet: "koha" / "dspace" |
| Target URI | `target_uri` | Text (URL) | `target_uri` | Render as link |
| Fingerprint | `fingerprint` | Text (Keyword) | `fingerprint` | Internal dedup flag |
| Language | `language` | Text (Keyword) | `language` | Optional facet |
| Description | `description` | Text | `description` | Full-text searchable |

**Indexing notes:**
- Do **not** index `id` or `full_text` in Drupal unless you need them for display or advanced search.
- Set `title` as the **Title field** (primary label) in the index settings so Views use it automatically.
- Mark `subjects`, `format_type`, `source_system`, and `publish_date` as **Indexed** for facets.

---

## 5. Configure Facets

### 5.1 Add Facets

1. Go to **Configuration > Search and metadata > Facets** (`/admin/config/search/facets`).
2. Click **Add facet**.
3. For each facet below:
   - Select the **Unified Catalog** index as the source.
   - Choose the corresponding field.
   - Configure widget (e.g., **Checkbox**, **Links**, **Date range**).

| Facet Label | Field | Widget | URL alias |
|-------------|-------|--------|-----------|
| Format | `format_type` | Checkbox | `format` |
| Subjects | `subjects` | Checkbox | `subject` |
| Publish Year | `publish_date` | Date range / Links | `year` |
| Source | `source_system` | Links | `source` |

### 5.2 Place Facet Blocks

1. Go to **Structure > Block layout** (`/admin/structure/block`).
2. Click **Place block** in the sidebar region (e.g., **Sidebar first**).
3. Add each facet block:
   - **Facet: Format**
   - **Facet: Subjects**
   - **Facet: Publish Year**
   - **Facet: Source**
4. Configure visibility:
   - Show only on page(s): `/search*` (or your custom search page path).
5. Save.

---

## 6. Create a Search View

### 6.1 Add a View

1. Go to **Structure > Views > Add view** (`/admin/structure/views/add`).
2. Fill the wizard:
   - **View name:** `Catalog Search`
   - **Show:** `Search API index: Unified Catalog`
   - **Create a page:** checked
   - **Page title:** `Search the Catalog`
   - **Path:** `/search`
   - **Display format:** `Unformatted list` of **Rendered entity** (or **Fields** if you prefer custom output)
3. Click **Save and edit**.

### 6.2 Add Exposed Filters (Search Form)

1. In the View editor, under **Filters**, click **Add**.
2. Add the **Search: Fulltext search** filter (or keyword filters for `title`, `creator`, `subjects`).
3. Check **Expose this filter to visitors**.
4. Set:
   - **Label:** `Search`
   - **Operator:** `Contains any word`
   - **Required:** No
5. Rearrange so the exposed filters appear above the results (already default for page displays).

### 6.3 Add Fields (if using Fields display)

If you chose **Fields** instead of **Rendered entity**, add these fields:

- `title` — linked to `target_uri` (or set a custom URL field)
- `creator`
- `publish_date` — format as `Y`
- `format_type` — use as badge/tag
- `subjects` — comma-separated or tag list
- `target_uri` — render as "View Details" button

### 6.4 Configure Paging

- **Use pager:** Full
- **Items per page:** 20

### 6.5 Save and Test

1. Click **Save**.
2. Visit `/search` and test:
   - Keyword search in the exposed filter box.
   - Facet blocks on the sidebar should narrow results.
   - Paging should work correctly.

---

## 7. Fallback / Custom Approach (If Elasticsearch Connector Fails)

If the connector is incompatible with ES 8.x:

1. **Disable or uninstall** `elasticsearch_connector`.
2. Enable the custom module `buet_elibrary` (see `custom_module_notes.md`).
3. Create a **Search API Server** using the **Database** backend as a placeholder, or use a custom datasource plugin in `buet_elibrary`.
4. In the custom module, implement `BuetSearchController` to proxy queries to `http://elasticsearch:9200/buet_unified_catalog/_search`.
5. Build a View that uses a **REST Export** or **Page** display fed by the custom controller.
6. Attach facet blocks manually by querying ES aggregations in the controller and passing them to a Twig template or block plugin.

> See `drupal/custom_module_notes.md` for code-level implementation details.

---

## 8. Post-Configuration Checklist

- [ ] Search API Server shows green status
- [ ] Index fields are mapped correctly
- [ ] Facet blocks appear on `/search` and filter results
- [ ] Exposed search box returns expected results
- [ ] Paging works on large result sets
- [ ] URLs are clean (Pathauto enabled if needed)
- [ ] Caching is configured (Dynamic Page Cache + BigPipe for authenticated users)

---

*Version: 1.0 — BUET E-Library V4 Search & CMS Worker*
