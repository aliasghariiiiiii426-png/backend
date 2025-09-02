#!/bin/bash
set -e

DOMAIN=bazmino.com
WEBROOT=/var/www/certbot
CERT_PATH=/etc/letsencrypt/live/$DOMAIN/fullchain.pem

# Create dummy cert if missing
if [ ! -f "$CERT_PATH" ]; then
    echo "[nginx] Creating dummy certificate for $DOMAIN..."
    mkdir -p /etc/letsencrypt/live/$DOMAIN
    openssl req -x509 -nodes -newkey rsa:2048 \
        -days 1 \
        -keyout /etc/letsencrypt/live/$DOMAIN/privkey.pem \
        -out /etc/letsencrypt/live/$DOMAIN/fullchain.pem \
        -subj "/CN=localhost"
fi

# Start nginx
nginx &

# Auto replace dummy cert every 12h
while true; do
    sleep 12h & wait $${!}
    echo "[certbot] Obtaining/renewing real certificate..."
    certbot certonly --webroot -w "$WEBROOT" -d "$DOMAIN" --non-interactive --agree-tos -m you@example.com || true
    nginx -s reload
done
