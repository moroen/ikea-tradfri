FROM alpine:latest

RUN apk add python3 python3-dev gcc musl-dev git autoconf

WORKDIR /root

RUN git clone -b development https://github.com/moroen/ikea-tradfri.git

WORKDIR /root/ikea-tradfri

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN python3 setup.py install