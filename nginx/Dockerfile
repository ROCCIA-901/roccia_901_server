FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
RUN apt-get update && apt-get install -y logrotate

COPY nginx-app.conf /etc/nginx/conf.d/
COPY nginx /etc/logrotate.d/

EXPOSE 80
