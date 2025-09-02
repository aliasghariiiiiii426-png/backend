FROM nginx:alpine

RUN apk add --no-cache bash openssl curl certbot certbot-nginx

COPY default.conf /etc/nginx/conf.d/default.conf
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
