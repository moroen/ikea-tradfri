FROM alpine:latest

ARG ip=localhost
ARG key=key

COPY . /root/
WORKDIR /root

RUN apk add --no-cache python3 python3-dev gcc musl-dev git autoconf
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt
RUN python3 setup.py install
RUN tradfri config $ip $key
RUN apk del autoconf git musl-dev gcc
RUN rm -rf /root/*

EXPOSE 1234
EXPOSE 8085
CMD tradfri server --host=0.0.0.0