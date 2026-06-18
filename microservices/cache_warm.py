#!/usr/bin/env python3
import json
from datetime import datetime, timezone

import utils

POPULAR_BIBLIONUMBERS = ["1", "2", "3", "4", "5", "10", "20", "50", "100"]


def warm_cache():
    redis = utils.get_redis_client()
    for bib in POPULAR_BIBLIONUMBERS:
        cache_key = f"koha_status:{bib}"
        if redis.exists(cache_key):
            continue
        try:
            parsed = utils.scrape_koha_status(bib)
            result = {
                "biblionumber": bib,
                "status": parsed["status"],
                "location": parsed["location"],
                "call_number": parsed["call_number"],
                "barcode": parsed["barcode"],
                "due_date": parsed["due_date"],
                "cached": False,
                "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            }
            redis.setex(cache_key, 600, json.dumps(result))
            utils.log_message("info", f"Warmed cache for {bib}")
        except Exception as e:
            utils.log_message("warning", f"Cache warm failed for {bib}: {e}")


if __name__ == "__main__":
    warm_cache()
