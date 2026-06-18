#!/bin/sh
set -e

# Wait for Elasticsearch
echo "Waiting for Elasticsearch at http://elasticsearch:9200..."
until /usr/local/bin/python -c "import urllib.request; urllib.request.urlopen('http://elasticsearch:9200/_cluster/health', timeout=5)" > /dev/null 2>&1; do
    sleep 2
done
echo "Elasticsearch is available."

# Wait for Redis
echo "Waiting for Redis at redis:6379..."
until /usr/local/bin/python -c "import socket; s=socket.socket(); s.settimeout(5); s.connect(('redis', 6379)); s.close()" > /dev/null 2>&1; do
    sleep 2
done
echo "Redis is available."

if [ "$MODE" = "harvester" ]; then
    echo "Starting cron daemon in foreground..."
    /usr/sbin/crond -f -c /app/crontabs
elif [ "$MODE" = "api" ] || [ -z "$MODE" ]; then
    echo "Starting Gunicorn API server..."
    /usr/local/bin/gunicorn -w 2 -b 0.0.0.0:5000 live_status:app
else
    echo "Unknown MODE: $MODE. Use 'harvester' or 'api'."
    exit 1
fi
