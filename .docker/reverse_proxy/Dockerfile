FROM nginx:1.21

COPY nginx.conf /etc/nginx/nginx.conf

RUN mkdir /etc/nginx/reverse_proxy.d/
COPY reverse_proxy.d/ /etc/nginx/reverse_proxy.d/

RUN rm /etc/nginx/conf.d/default.conf
