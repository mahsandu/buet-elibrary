FROM python:3.11-alpine

# Install build dependencies and curl for healthcheck
RUN apk add --no-cache gcc musl-dev libxml2-dev libxslt-dev curl

# Create non-root user
RUN adduser -D appuser

# Set working directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY *.py ./
COPY crontab ./
COPY entrypoint.sh ./
RUN chmod +x entrypoint.sh

# Set up crontab directory for appuser
RUN mkdir -p /app/crontabs && cp crontab /app/crontabs/appuser && chown -R appuser:appuser /app/crontabs

# Healthcheck for Flask API
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Switch to non-root user
USER appuser

EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]
