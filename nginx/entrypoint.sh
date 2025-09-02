#!/bin/bash
set -e

DOMAIN=yourdomain.com
WEBROOT=/var/www/certbot
CERT_PATH=/etc/letsencrypt/live/$DOMAIN/fullchain.pem

# Create dummy certificate if it doesn't exist
if [ ! -f "$CERT_PATH" ]; then
  echo "Creating dummy certificate for $DOMAIN..."
  mkdir -p /etc/letsencrypt/live/$DOMAIN
  openssl req -x509 -nodes -newkey rsa:2048 \
    -days 1 \
    -keyout /etc/letsencrypt/live/$DOMAIN/privkey.pem \
    -out /etc/letsencrypt/live/$DOMAIN/fullchain.pem \
    -subj "/CN=localhost"
fi

# Start nginx in background
nginx &

# Wait for certbot to run (or manually)
while true; do
  sleep 12h & wait $${!}
  certbot renew --webroot -w "$WEBROOT"
  nginx -s reload
done
