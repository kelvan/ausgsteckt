FROM nginx

RUN apt-get update && apt-get install wait-for-it

COPY nginx.conf /etc/nginx/conf.d/default

EXPOSE 80
