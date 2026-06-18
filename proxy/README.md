# BUET Library E-Resource Proxy

## Overview

This proxy provides **off-campus access** to subscribed e-resources (IEEE, Elsevier, JSTOR, Springer, Wiley, ACM) by forwarding user requests through the university's institutional IP range. It is designed as a **self-hosted, free alternative** to commercial proxies like EZproxy or OpenAthens, suitable for developing-country institutions with budget constraints.

**Two implementations are provided:**

| Proxy | Technology | Best For |
|-------|-----------|----------|
| **Nginx Proxy** | `nginx:alpine` with `sub_filter` | Production, simple databases, high performance |
| **Python Proxy** | Flask + BeautifulSoup | Complex databases, better URL rewriting, development/testing |

## Architecture

```
Off-Campus User
      │
      ▼ (authenticated request)
┌─────────────┐
│  Nginx      │  Port 8080  ──►  Basic Auth (user/password)
│  Proxy      │  ──►  IP-based auth to databases (institutional IP)
└─────────────┘
      │
      ▼ (forwarded request)
┌─────────────────────────────────┐
│  IEEE / Elsevier / JSTOR / ...  │  (sees BUET institutional IP)
└─────────────────────────────────┘
      │
      ▼ (response with rewritten URLs)
Back to User
```

## How It Works

1. **User Authentication**: Off-campus users access the proxy at `https://proxy.buet.ac.bd:8080/ieee/`
2. **Basic Auth**: Nginx prompts for username/password (stored in `proxy/.htpasswd`)
3. **IP Proxying**: The request is forwarded to IEEE from the BUET server IP (institutional range)
4. **URL Rewriting**: `sub_filter` rewrites absolute URLs in HTML/CSS/JS so subsequent clicks stay within the proxy
5. **Cookie Handling**: `proxy_cookie_domain` and `proxy_cookie_path` ensure session cookies work through the proxy

## Quick Start

### 1. Generate User Credentials

```bash
# Option A: Using the Python script (works on Windows/Linux/macOS)
python proxy/generate_htpasswd.py buetadmin mysecurepassword
# Copy the output line into proxy/.htpasswd

# Option B: Using htpasswd (Linux/macOS with Apache)
htpasswd -nbB buetadmin mysecurepassword >> proxy/.htpasswd

# Option C: Using openssl (universal, generates bcrypt)
# Install passlib: pip install passlib
# Then use Option A
```

Create `proxy/.htpasswd` with at least one line:
```
buetadmin:$apr1$xxxxx$encryptedhash
```

### 2. Start the Proxy Service

The proxy is already configured in `docker-compose.yml`. Just start it:

```bash
docker-compose up -d proxy
```

Or start all services together:
```bash
docker-compose up -d
```

### 3. Verify the Proxy

```bash
# Check health
curl http://localhost:8080/health
# Expected: proxy-healthy

# Check database listing (no auth needed for root)
curl http://localhost:8080/

# Access IEEE (requires auth)
curl -u buetadmin:mysecurepassword http://localhost:8080/ieee/
```

### 4. Configure DNS / Firewall

- The proxy runs on port `8080` by default
- Ensure the server firewall allows inbound TCP 8080
- Point a DNS record (e.g., `proxy.buet.ac.bd`) to the server IP
- For HTTPS: add SSL certificate to Nginx (see SSL Setup below)

## Available Databases

| Proxy Path | Database | Base URL |
|-----------|----------|----------|
| `/ieee/` | IEEE Xplore | `https://ieeexplore.ieee.org` |
| `/elsevier/` | Elsevier ScienceDirect | `https://www.sciencedirect.com` |
| `/jstor/` | JSTOR | `https://www.jstor.org` |
| `/springer/` | SpringerLink | `https://link.springer.com` |
| `/wiley/` | Wiley Online Library | `https://onlinelibrary.wiley.com` |
| `/acm/` | ACM Digital Library | `https://dl.acm.org` |

## SSL Setup (HTTPS)

For production, the proxy should use HTTPS. Two approaches:

### Option A: Let's Encrypt (Recommended)

Use `certbot` to obtain a free SSL certificate:

```bash
# Install certbot
sudo apt install certbot

# Obtain certificate (replace with your domain)
sudo certbot certonly --standalone -d proxy.buet.ac.bd

# The certificate will be at:
# /etc/letsencrypt/live/proxy.buet.ac.bd/fullchain.pem
# /etc/letsencrypt/live/proxy.buet.ac.bd/privkey.pem

# Mount these into the proxy container in docker-compose.yml:
# volumes:
#   - /etc/letsencrypt:/etc/letsencrypt:ro

# Then uncomment the SSL server block in proxy/nginx-proxy.conf
```

### Option B: Self-Signed Certificate (Development)

```bash
# Generate self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout proxy/ssl/nginx.key \
  -out proxy/ssl/nginx.crt \
  -subj "/CN=proxy.buet.ac.bd"
```

Then mount the certificates in `docker-compose.yml`.

## Python Proxy (Alternative)

The Nginx proxy uses `sub_filter` for URL rewriting, which is fast but limited. For databases with complex JavaScript or dynamic content, the **Python Proxy** provides more thorough rewriting via BeautifulSoup.

### Running the Python Proxy

```bash
# Standalone (development)
cd microservices
python proxy_server.py
# Runs on http://localhost:5001

# With Docker (add to docker-compose.yml as a separate service)
# Or use Gunicorn:
gunicorn -w 2 -b 0.0.0.0:5001 proxy_server:app
```

### Switching Between Nginx and Python Proxy

In `docker-compose.yml`, the proxy service uses `nginx-proxy.conf` by default. To switch to the Python proxy, you would need to either:

1. Replace the proxy service image with the microservices image running in proxy mode
2. Or add a second proxy service on a different port

## Limitations vs. EZproxy

| Feature | Nginx Proxy | Python Proxy | EZproxy (Commercial) |
|--------|-------------|--------------|-------------------|
| URL Rewriting | `sub_filter` (basic) | BeautifulSoup (thorough) | Native (comprehensive) |
| JavaScript Rewriting | Limited | Limited | Full |
| Cookie Management | Basic | Basic | Advanced |
| Database Stanzas | Manual config | JSON config | 3,600+ pre-built |
| Authentication | Basic Auth | Basic Auth | LDAP, SAML, OAuth |
| Cost | Free | Free | ~$100/mo or license |
| Maintenance | Manual URL updates | Manual URL updates | Vendor-managed stanzas |

**Recommendation:** Use the Nginx/Python proxy for **light e-resource portfolios** (6-10 databases). If BUET subscribes to **20+ databases** or requires **SAML/SSO authentication**, consider migrating to **self-hosted EZproxy** or **OpenAthens**.

## Adding a New Database

To add a new database to the Nginx proxy, edit `proxy/nginx-proxy.conf` and add a new location block:

```nginx
location /newdb/ {
    proxy_pass https://www.newdb.com/;
    proxy_set_header Host www.newdb.com;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header Accept-Encoding "";

    proxy_cookie_domain www.newdb.com $host;
    proxy_cookie_path / /newdb/;

    sub_filter 'https://www.newdb.com/' '/newdb/';
    sub_filter 'https://www.newdb.com' '/newdb';
    sub_filter_once off;
    sub_filter_types text/html text/css application/javascript;

    proxy_redirect https://www.newdb.com/ /newdb/;
}
```

Then reload Nginx:
```bash
docker-compose exec proxy nginx -s reload
```

## Security Considerations

1. **Basic Auth is NOT as secure as SSO**: Passwords are sent with every request. For production, consider integrating with BUET's LDAP/Active Directory.
2. **HTTPS is mandatory**: Never expose the proxy over HTTP in production. Use Let's Encrypt or a proper certificate.
3. **Rate Limiting**: The Nginx proxy does not have built-in rate limiting. Add `limit_req` zones if you expect high traffic.
4. **Access Logs**: Monitor `/var/log/nginx/access.log` for abuse. Logs are forwarded to the host via Docker.
5. **IP Restrictions**: If possible, restrict proxy access to known BUET IP ranges at the firewall level (e.g., allow only Bangladeshi IP blocks for off-campus users).

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| "Database not found" | Path mismatch | Check `/ieee/` vs `/ieee` (trailing slash) |
| Images not loading | URL rewriting missed | Add `sub_filter` for image domains |
| Login fails on database | Cookie domain mismatch | Check `proxy_cookie_domain` directive |
| CSS broken | `Accept-Encoding` not stripped | Ensure `proxy_set_header Accept-Encoding ""` |
| SSL handshake error | Certificate issue | Check `proxy_ssl_server_name on` |

## Integration with Drupal

The Drupal frontend can link to databases via the proxy:

```html
<!-- In Drupal template -->
<a href="https://proxy.buet.ac.bd:8080/ieee/" target="_blank">
  IEEE Xplore (Off-Campus)
</a>
```

For on-campus users, link directly to the database (no proxy needed):

```html
<a href="https://ieeexplore.ieee.org/" target="_blank">
  IEEE Xplore (On-Campus)
</a>
```

A JavaScript snippet can detect the user's IP and switch automatically:

```javascript
// Auto-detect: if IP is not in BUET range, use proxy
const isOnCampus = /* check IP range */;
const ieeeLink = isOnCampus 
  ? 'https://ieeexplore.ieee.org/' 
  : 'https://proxy.buet.ac.bd:8080/ieee/';
```

## EZproxy Migration Path

If BUET later adopts **EZproxy**, the transition is straightforward:

1. Install EZproxy on the host (outside Docker) or on a dedicated VM
2. Update DNS: `proxy.buet.ac.bd` → EZproxy server IP
3. Migrate user credentials from `.htpasswd` to EZproxy's `user.txt`
4. Import database stanzas from OCLC's stanza library
5. The Drupal links remain unchanged (they point to `proxy.buet.ac.bd`, which now resolves to EZproxy)

## Reference

- [Nginx Reverse Proxy Guide](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/)
- [EZproxy Documentation](https://help.oclc.org/Metadata_Collection/EZproxy)
- [OpenAthens for Institutions](https://www.openathens.net/)
- [Shibboleth Identity Provider](https://shibboleth.atlassian.net/)
