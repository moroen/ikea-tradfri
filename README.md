# Python Script for controlling IKEA - Tradfri lights


## Requirements
Recommended python version: 3.6.x - 3.7.x, 3.5.3 also supported, but will be deprecated.

## Install dependencies
```shell
$ sudo apt install build-essential autoconf 
```

## Setup
```shell
$ python3 setup.py install
```

The script needs the gateway IP and key, this can be set with the config gateway option. This is only needed on first use.

```shell
./tradfri.py config gateway IP KEY
```


## Usage
```shell
./tradfri.py --help
```

### List all devices
```shell
./tradfri list
```

### Controll a light
```shell
./tradfri on <ID>
./tradfri off <ID>
./tradfri level <ID> <LEVEL> (Level: 0-254)
./tradfri wb <ID> <WHITEBALANCE> (Whitebalance: cold/normal/warm)
```

## Using docker

### Build docker image
```shell
$ docker build --no-cache --build-arg ip=IP --build-arg key=KEY -t tradfri:latest . 
```
IP = the ip-adress of the IKEA gateway, KEY = the master key found on the underside of the gateway.

### Run docker image
```shell
$ docker run -d -p 1234:1234 -p 8085:8085 tradfri:latest
```

### Test docker-adapter
Test the adapter using curl (or another browser)
```shell
$ curl docker-host-ip:8085/devices
```
