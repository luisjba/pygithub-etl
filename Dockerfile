FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
RUN apk add --no-cache --update \
    bash nano \
    python3 python3-dev gcc make\
    gfortran musl-dev g++ \
    libffi-dev openssl-dev \
    libxml2 libxml2-dev \
    libxslt libxslt-dev \
    libjpeg-turbo-dev zlib-dev
ENV STATIC_URL /static
ENV STATIC_PATH /var/www/etl/dashboard/static
COPY ./requirements.txt /var/www/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /var/www/requirements.txt