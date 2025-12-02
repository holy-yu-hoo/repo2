FROM nginx
RUN apt update
#RUN rm /etc/nginx/conf.d/default.conf

RUN openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048 &&\
	openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/certs/self.key -out /etc/ssl/certs/self.crt \
	-subj "/C=RU/ST=Moscow/L=Kremlin/O=yuhoo/OU=Org/CN=YH"

COPY nginx.conf /etc/nginx/conf.d
COPY ssl-params.conf /etc/nginx/ssl-params.conf