FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine
RUN apk add --no-cache --update \
    bash nano \
    python3 python3-dev gcc make\
    gfortran musl-dev g++ \
    libffi-dev openssl-dev \
    libxml2 libxml2-dev \
    libxslt libxslt-dev \
    libjpeg-turbo-dev zlib-dev
RUN pip install --upgrade pip
RUN pip install pandas
ENV STATIC_URL /static
COPY ./requirements.txt /var/www/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /var/www/requirements.txt