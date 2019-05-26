# Python Script for controlling IKEA - Tradfri lights


## Requirements
Recommended python version: 3.5.3 - 3.7.3

## Pre install
Latest version of PIP and setuptools are needed:
```shell
$ pip install --upgrade pip
$ pip install --upgrade setuptools
```

## Setup
```shell
$ python3 setup.py install
```

## Configure connection

```shell
./tradfri config <IP> <KEY>
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