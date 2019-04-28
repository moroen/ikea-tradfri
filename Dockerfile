FROM alpine:latest

ARG ip=localhost
ARG key=key

RUN apk add python3 python3-dev gcc musl-dev git autoconf

WORKDIR /root

RUN git clone -b development https://github.com/moroen/ikea-tradfri.git

WORKDIR /root/ikea-tradfri

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN python3 setup.py install

EXPOSE 1234
EXPOSE 8085

RUN echo $ip $key

RUN ./tradfri config $ip $key

WORKDIR /root
RUN rm -rf ikea-tradfri
CMD tradfri server --host=0.0.0.0