# Custom Module Notes — `buet_elibrary`

These notes provide the technical blueprint for a custom Drupal module that acts as the bridge between Drupal 11 and the external `buet_unified_catalog` Elasticsearch index.

---

## Module Overview

**Module name:** `buet_elibrary`  
**Location:** `web/modules/custom/buet_elibrary/`  
**Dependencies:** `drupal:system`, `drupal:node` (optional), `drupal:views` (optional)

**Responsibilities:**
1. Proxy Elasticsearch queries through a custom REST route (`/api/search`).
2. Provide a block plugin (`buet_live_status`) that renders live availability via AJAX.
3. Define a `hook_theme()` entry for `live_status` Twig template.
4. Attach JavaScript behavior for `data-biblio` attribute binding.
5. Provide a custom field formatter for `target_uri` that generates direct Koha / DSpace links.
6. Include update hooks for schema changes.

---

## 1. `buet_elibrary.info.yml`

```yaml
name: 'BUET E-Library'
type: module
description: 'Custom integration for BUET E-Library search, live status, and e-resources.'
core_version_requirement: ^11
package: BUET
version: 1.0.0
dependencies:
  - drupal:system
```

---

## 2. `buet_elibrary.module`

```php
<?php

use Drupal\Core\Routing\RouteMatchInterface;

/**
 * Implements hook_theme().
 */
function buet_elibrary_theme($existing, $type, $theme, $path) {
  return [
    'live_status' => [
      'variables' => [
        'biblionumber' => NULL,
        'status' => NULL,
        'message' => NULL,
      ],
      'template' => 'live-status',
    ],
  ];
}

/**
 * Implements hook_preprocess_HOOK() for live_status.
 */
function buet_elibrary_preprocess_live_status(&$variables) {
  // Ensure safe defaults if data is missing.
  $variables['#attached']['library'][] = 'buet_elibrary/live_status';
}

/**
 * Implements hook_help().
 */
function buet_elibrary_help($route_name, RouteMatchInterface $route_match) {
  switch ($route_name) {
    case 'help.page.buet_elibrary':
      return '<p>BUET E-Library custom module for Elasticsearch integration and live status.</p>';
  }
}

/**
 * Implements hook_update_N() — example schema update.
 */
function buet_elibrary_update_10001(&$sandbox) {
  \Drupal::messenger()->addStatus('BUET E-Library schema updated to 1.0.1.');
}
```

---

## 3. `BuetSearchController.php`

**Path:** `src/Controller/BuetSearchController.php`

```php
<?php

namespace Drupal\buet_elibrary\Controller;

use Drupal\Core\Controller\ControllerBase;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\DependencyInjection\ContainerInterface;
use Drupal\Core\Cache\CacheBackendInterface;
use GuzzleHttp\ClientInterface;

class BuetSearchController extends ControllerBase {

  protected $httpClient;
  protected $cache;

  const ES_INDEX = 'buet_unified_catalog';
  const ES_HOST = 'http://elasticsearch:9200';
  const CACHE_BIN = 'buet_elibrary.search';

  public function __construct(ClientInterface $http_client, CacheBackendInterface $cache) {
    $this->httpClient = $http_client;
    $this->cache = $cache;
  }

  public static function create(ContainerInterface $container) {
    return new static(
      $container->get('http_client'),
      $container->get('cache.default')
    );
  }

  /**
   * Proxies a search query to Elasticsearch with caching.
   */
  public function search(Request $request) {
    $query = $request->query->get('q', '');
    $from = (int) $request->query->get('from', 0);
    $size = (int) $request->query->get('size', 20);
    $filters = $request->query->all('filters'); // e.g., format_type, subjects

    $cache_key = 'search:' . md5(serialize($request->query->all()));
    if ($cache = $this->cache->get($cache_key)) {
      return new JsonResponse($cache->data);
    }

    $esQuery = [
      'query' => [
        'bool' => [
          'must' => [
            'multi_match' => [
              'query' => $query,
              'fields' => ['title^3', 'creator^2', 'subjects', 'description'],
            ],
          ],
          'filter' => [],
        ],
      ],
      'from' => $from,
      'size' => $size,
      'highlight' => [
        'fields' => [
          'title' => new \stdClass(),
          'description' => new \stdClass(),
        ],
      ],
    ];

    // Build term filters from facet selections.
    foreach ($filters as $field => $values) {
      $values = is_array($values) ? $values : [$values];
      $esQuery['query']['bool']['filter'][] = [
        'terms' => [$field => $values],
      ];
    }

    try {
      $response = $this->httpClient->request('POST', self::ES_HOST . '/' . self::ES_INDEX . '/_search', [
        'headers' => ['Content-Type' => 'application/json'],
        'json' => $esQuery,
        'timeout' => 10,
      ]);
      $data = json_decode($response->getBody(), TRUE);
    } catch (\Exception $e) {
      return new JsonResponse(['error' => 'Search failed', 'message' => $e->getMessage()], 500);
    }

    // Cache successful responses for 5 minutes.
    $this->cache->set($cache_key, $data, time() + 300, [self::CACHE_BIN]);

    return new JsonResponse($data);
  }
}
```

**Route registration** (`buet_elibrary.routing.yml`):

```yaml
buet_elibrary.api_search:
  path: '/api/search'
  defaults:
    _controller: '\Drupal\buet_elibrary\Controller\BuetSearchController::search'
    _title: 'Catalog Search'
  requirements:
    _permission: 'access content'
  methods: [GET]
```

---

## 4. `LiveStatusBlock.php`

**Path:** `src/Plugin/Block/LiveStatusBlock.php`

```php
<?php

namespace Drupal\buet_elibrary\Plugin\Block;

use Drupal\Core\Block\BlockBase;
use Drupal\Core\Form\FormStateInterface;

/**
 * Provides a block that renders live availability status via AJAX.
 *
 * @Block(
 *   id = "buet_live_status",
 *   admin_label = @Translation("BUET Live Status"),
 *   category = @Translation("BUET E-Library"),
 * )
 */
class LiveStatusBlock extends BlockBase {

  public function defaultConfiguration() {
    return [
      'biblionumber' => '',
    ] + parent::defaultConfiguration();
  }

  public function blockForm($form, FormStateInterface $form_state) {
    $form['biblionumber'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Biblionumber'),
      '#default_value' => $this->configuration['biblionumber'],
      '#description' => $this->t('Enter the Koha biblionumber to check status for.'),
    ];
    return $form;
  }

  public function blockSubmit($form, FormStateInterface $form_state) {
    $this->configuration['biblionumber'] = $form_state->getValue('biblionumber');
  }

  public function build() {
    $biblio = $this->configuration['biblionumber'];
    if (empty($biblio)) {
      return ['#markup' => $this->t('No biblionumber configured.')];
    }

    return [
      '#theme' => 'live_status',
      '#biblionumber' => $biblio,
      '#attached' => [
        'library' => ['buet_elibrary/live_status'],
      ],
    ];
  }

  public function getCacheMaxAge() {
    // Do not cache; status changes in real time.
    return 0;
  }
}
```

---

## 5. `buet-elibrary.js`

**Path:** `js/buet-elibrary.js`

```javascript
/**
 * @file
 * Drupal behavior for live status AJAX loading.
 */
(function (Drupal, once) {
  'use strict';

  Drupal.behaviors.buetLiveStatus = {
    attach: function (context, settings) {
      once('buet-live-status', '[data-biblio]', context).forEach(function (element) {
        var biblio = element.getAttribute('data-biblio');
        if (!biblio) {
          return;
        }

        // Show loading state.
        element.querySelector('.status-loading').textContent = Drupal.t('Checking availability...');

        // Fetch status via Drupal proxy or direct microservice.
        var endpoint = (settings.buet_elibrary && settings.buet_elibrary.statusEndpoint)
          ? settings.buet_elibrary.statusEndpoint
          : '/buet/live-status/' + biblio;

        fetch(endpoint)
          .then(function (response) {
            if (!response.ok) {
              throw new Error('Status request failed');
            }
            return response.json();
          })
          .then(function (data) {
            var statusText = data.status || Drupal.t('Unknown');
            var message = data.message || '';

            // Update text nodes safely (no innerHTML).
            var statusEl = element.querySelector('.status-text');
            if (statusEl) {
              statusEl.textContent = statusText;
            }
            var msgEl = element.querySelector('.status-message');
            if (msgEl && message) {
              msgEl.textContent = message;
            }

            // Add CSS class for styling (e.g., green/red).
            element.classList.add('status-' + (data.status_key || 'unknown'));
          })
          .catch(function (error) {
            var statusEl = element.querySelector('.status-text');
            if (statusEl) {
              statusEl.textContent = Drupal.t('Unavailable');
            }
            console.error('Live status error:', error);
          });
      });
    }
  };

})(Drupal, once);
```

**Library declaration** (`buet_elibrary.libraries.yml`):

```yaml
live_status:
  version: 1.x
  js:
    js/buet-elibrary.js: {}
  dependencies:
    - core/drupal
    - core/once
    - core/drupalSettings
```

---

## 6. `live-status.html.twig`

**Path:** `templates/live-status.html.twig`

```twig
{#
/**
 * @file
 * Template for live availability status.
 *
 * Available variables:
 * - biblionumber: The Koha biblionumber.
 * - status: Pre-rendered status text (if backend provided it).
 * - message: Additional message (if any).
 */
#}
<div id="live-status" data-biblio="{{ biblionumber }}" class="live-status-wrapper">
  <span class="status-loading">{{ 'Checking availability...'|t }}</span>
  <span class="status-text" style="display: none;"></span>
  <span class="status-message" style="display: none;"></span>
</div>
```

> **Security note:** The template uses `|t` for static strings and `{{ biblionumber }}` is auto-escaped by Twig. Never use `|raw` on external JSON data.

---

## 7. Custom Field Formatter for `target_uri`

**Path:** `src/Plugin/Field/FieldFormatter/TargetUriFormatter.php`

```php
<?php

namespace Drupal\buet_elibrary\Plugin\Field\FieldFormatter;

use Drupal\Core\Field\FieldItemListInterface;
use Drupal\Core\Field\FormatterBase;

/**
 * Plugin implementation for a direct Koha / DSpace link formatter.
 *
 * @FieldFormatter(
 *   id = "buet_target_uri",
 *   label = @Translation("BUET Target URI Link"),
 *   field_types = {"string", "link"},
 * )
 */
class TargetUriFormatter extends FormatterBase {

  public function viewElements(FieldItemListInterface $items, $langcode) {
    $elements = [];
    foreach ($items as $delta => $item) {
      $uri = $item->value ?? $item->uri ?? '';
      $source = (strpos($uri, 'koha') !== false) ? 'Koha OPAC' : 'DSpace';

      $elements[$delta] = [
        '#type' => 'link',
        '#title' => $this->t('View in @source', ['@source' => $source]),
        '#url' => \Drupal\Core\Url::fromUri($uri),
        '#attributes' => [
          'class' => ['target-uri-link', 'source-' . strtolower($source)],
          'target' => '_blank',
        ],
      ];
    }
    return $elements;
  }
}
```

---

## 8. Update Hooks for Schema Changes

When adding new fields or changing the module schema, implement `hook_update_N()` in `buet_elibrary.install`:

```php
<?php

/**
 * Implements hook_install().
 */
function buet_elibrary_install($is_syncing) {
  \Drupal::messenger()->addStatus('BUET E-Library module installed.');
}

/**
 * Update 10002 — add default config for live status endpoint.
 */
function buet_elibrary_update_10002(&$sandbox) {
  \Drupal::configFactory()->getEditable('buet_elibrary.settings')
    ->set('status_endpoint', 'http://live_status:5000/status')
    ->save();
}
```

---

## 9. Directory Structure Summary

```
web/modules/custom/buet_elibrary/
├── buet_elibrary.info.yml
├── buet_elibrary.module
├── buet_elibrary.routing.yml
├── buet_elibrary.libraries.yml
├── buet_elibrary.install
├── js/
│   └── buet-elibrary.js
├── src/
│   ├── Controller/
│   │   └── BuetSearchController.php
│   ├── Plugin/
│   │   ├── Block/
│   │   │   └── LiveStatusBlock.php
│   │   └── Field/
│   │       └── FieldFormatter/
│   │           └── TargetUriFormatter.php
│   └── ...
├── templates/
│   └── live-status.html.twig
```

---

## 10. Integration Checklist

- [ ] Module enabled (`drush en buet_elibrary`)
- [ ] Route `/api/search` returns ES JSON
- [ ] Block `buet_live_status` placed and renders `data-biblio` div
- [ ] JavaScript library attached and loads status without `innerHTML`
- [ ] Twig template escapes all output
- [ ] Field formatter available on `target_uri` fields
- [ ] Caching configured for search proxy (5 min default)
- [ ] Live status block has `getCacheMaxAge() = 0` (no cache)

---

*Version: 1.0 — BUET E-Library V4 Search & CMS Worker*
