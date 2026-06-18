#!/usr/bin/env python3
import json
import threading
from datetime import datetime, timezone

from flask import Flask, jsonify

import utils

app = Flask(__name__)
semaphore = threading.Semaphore(5)


@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/api/status/<biblionumber>")
def get_status(biblionumber):
    with semaphore:
        redis_client = utils.get_redis_client()
        cache_key = f"koha_status:{biblionumber}"

        cached = redis_client.get(cache_key)
        if cached:
            try:
                data = json.loads(cached)
                data["cached"] = True
                return jsonify(data)
            except Exception:
                pass

        try:
            parsed = utils.scrape_koha_status(biblionumber)
        except Exception as e:
            utils.log_message("error", f"Scraping failed for {biblionumber}: {e}")
            return jsonify(
                {
                    "biblionumber": biblionumber,
                    "status": "unknown",
                    "error": str(e),
                    "cached": False,
                    "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                }
            ), 503

        result = {
            "biblionumber": biblionumber,
            "status": parsed["status"],
            "location": parsed["location"],
            "call_number": parsed["call_number"],
            "barcode": parsed["barcode"],
            "due_date": parsed["due_date"],
            "cached": False,
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        }

        try:
            redis_client.setex(cache_key, 600, json.dumps(result))
        except Exception as e:
            utils.log_message("warning", f"Redis cache failed: {e}")

        return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
