#!/bin/sh
# Wait until SSL certificates exist
DOMAIN=bazmino.com
CERT_PATH=/etc/letsencrypt/live/$DOMAIN/fullchain.pem

# Generate a dummy certificate if missing (first start)
if [ ! -f "$CERT_PATH" ]; then
    echo "Creating dummy certificate for $DOMAIN..."
    mkdir -p /etc/letsencrypt/live/$DOMAIN
    openssl req -x509 -nodes -newkey rsa:2048 \
        -days 1 \
        -keyout /etc/letsencrypt/live/$DOMAIN/privkey.pem \
        -out /etc/letsencrypt/live/$DOMAIN/fullchain.pem \
        -subj "/CN=$DOMAIN"
fi

# Replace template variables
envsubst '$DOMAIN' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf

# Start Nginx
nginx -g 'daemon off;'
