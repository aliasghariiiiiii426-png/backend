#!/bin/sh

set -e

DOMAIN=${DOMAIN}

# Paths for the certificates
CERT_PATH="/etc/letsencrypt/live/$DOMAIN/fullchain.pem"
KEY_PATH="/etc/letsencrypt/live/$DOMAIN/privkey.pem"

# Create dummy certificate if not exists
if [ ! -f "$CERT_PATH" ] || [ ! -f "$KEY_PATH" ]; then
  echo "Creating dummy certificate for $DOMAIN..."
  mkdir -p /etc/letsencrypt/live/$DOMAIN
  openssl req -x509 -nodes -days 1 \
    -subj "/CN=localhost" \
    -newkey rsa:2048 \
    -keyout "$KEY_PATH" \
    -out "$CERT_PATH"
fi

# Start nginx
nginx -g "daemon off;"
