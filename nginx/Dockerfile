FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx-app.conf /etc/nginx/conf.d/

RUN mkdir /var/www
RUN mkdir /var/www/certbot

EXPOSE 80 443
