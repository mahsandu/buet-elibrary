# Elasticsearch Setup for BUET E-Library V4

This directory contains the schema and setup script for the unified search index in Elasticsearch 8.10.2.

## Files

- `schema.json` — Index mapping for `buet_unified_catalog`
- `setup_index.py` — Python script to create / reset the index

## Quick Start

Run the setup script from the repo root:

```bash
python elasticsearch/setup_index.py
```

Force-delete an existing index without prompting:

```bash
python elasticsearch/setup_index.py --force
```

Skip alias creation:

```bash
python elasticsearch/setup_index.py --no-alias
```

Point to a different ES host:

```bash
python elasticsearch/setup_index.py --host http://localhost:9200
```

## Verify the Index

```bash
curl http://localhost:9200/buet_unified_catalog
```

Check mappings:

```bash
curl http://localhost:9200/buet_unified_catalog/_mapping?pretty
```

## Delete and Recreate

```bash
curl -X DELETE http://localhost:9200/buet_unified_catalog
python elasticsearch/setup_index.py
```

## Performance Tips

### Bulk Indexing

During large harvest operations set `refresh_interval` to `-1` to disable refreshes and speed up ingestion:

```bash
curl -X PUT http://localhost:9200/buet_unified_catalog/_settings \
  -H 'Content-Type: application/json' \
  -d '{"refresh_interval": "-1"}'
```

Restore to normal after the bulk load:

```bash
curl -X PUT http://localhost:9200/buet_unified_catalog/_settings \
  -H 'Content-Type: application/json' \
  -d '{"refresh_interval": "1s"}'
```

### Bulk Sizing

- Use batches of **500–2,000** documents per `_bulk` request.
- Monitor heap usage; a single-node dev instance with 1 GB heap handles ~1–2 k docs comfortably.
- If full-text (`full_text`) is populated, reduce batch size to **300–500**.

### Single-Node Deployment (ES 8.x)

ES 8.x bootstraps security features by default. In a single-node Docker stack you may need to disable some production checks:

- Set `discovery.type: single-node` in `elasticsearch.yml`
- Set `xpack.security.enabled: false` for local development (enable + configure TLS/certs for production)
- Set `ES_JAVA_OPTS=-Xms1g -Xmx1g` to constrain memory

```yaml
# docker-compose snippet
elasticsearch:
  image: docker.elastic.co/elasticsearch/elasticsearch:8.10.2
  environment:
    - discovery.type=single-node
    - xpack.security.enabled=false
    - "ES_JAVA_OPTS=-Xms1g -Xmx1g"
  ports:
    - "9200:9200"
```

## Notes

- The alias `buet_search` is optional but recommended; it lets Drupal and harvesters reference a stable name while the underlying index can be re-created during re-indexing.
- `fingerprint` is an MD5 hash used by the harvester to flag potential duplicates across Koha and DSpace.
- `full_text` is reserved for future OCR/PDF text extraction and is not populated by the initial harvester.
