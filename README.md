Python Script for controlling IKEA - Tradfri lights


# Requirements
Requires https://github.com/ggravlingen/pytradfri
Please use the libcoap (sync)-version of the library, instructions for installing it can be found in the repository readme.

# Usage
```shell
./tradfri.py --help
```


The script needs the gateway IP and key, this can be set with the --gateway and --key options. This is only needed on first use, run the command from the directory the script is located, and the ini-file will be created:

```shell
./tradfri.py --gateway IP --key KEY list
```

# Domoticz
Use from on and off action of a virtual switch
```
script://python/tradfri.py <id> on/off
```
