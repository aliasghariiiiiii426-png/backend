FROM nginx:alpine

RUN apk add --no-cache bash openssl curl

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY default.conf /etc/nginx/conf.d/default.conf
