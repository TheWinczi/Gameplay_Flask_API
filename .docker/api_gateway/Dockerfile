FROM nginx:1.21

COPY nginx.conf /etc/nginx/nginx.conf

RUN mkdir /etc/nginx/api_gateway.d/
COPY api_gateway.d/ /etc/nginx/api_gateway.d/

