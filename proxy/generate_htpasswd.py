#!/usr/bin/env python3
"""
Generate .htpasswd entries for Nginx Basic Authentication.

Usage:
    python proxy/generate_htpasswd.py <username> <password>

Example:
    python proxy/generate_htpasswd.py buetadmin mysecurepassword

Output:
    buetadmin:$apr1$xxxxx$encryptedhash

Copy the output line into proxy/.htpasswd (one line per user).

Requirements:
    pip install passlib

Alternative (Linux/macOS with Apache):
    htpasswd -nbB buetadmin mysecurepassword
"""
import sys
import argparse

def generate_apr1(username: str, password: str) -> str:
    """Generate an Apache-style APR1-MD5 password hash."""
    try:
        from passlib.hash import apr_md5_crypt
        hashed = apr_md5_crypt.hash(password)
        return f"{username}:{hashed}"
    except ImportError:
        print("ERROR: passlib is not installed.")
        print("Install with: pip install passlib")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Generate Nginx .htpasswd entries")
    parser.add_argument("username", help="Username for proxy access")
    parser.add_argument("password", help="Password for proxy access")
    args = parser.parse_args()

    entry = generate_apr1(args.username, args.password)
    print(entry)
    print(f"\n# Append this line to proxy/.htpasswd")
    print(f"# Example: echo '{entry}' >> proxy/.htpasswd")


if __name__ == "__main__":
    main()
