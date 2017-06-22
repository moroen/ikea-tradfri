#!/usr/bin/env python3

import argparse
import configparser
import os

from pytradfri import Gateway
from pytradfri.api.libcoap_api import api_factory

INIFILE = "{0}/tradfri.ini".format(os.path.dirname(os.path.realpath(__file__)))

config = configparser.ConfigParser()

def SaveConfig(args):

    if os.path.exists(INIFILE):
        config.read(INIFILE)
    else: 
        config["Gateway"] = {"ip": "UNDEF", "key": "UNDEF"}

    if args.gateway != None:
        config["Gateway"]["ip"] = args.gateway

    if args.key != None:
        config["Gateway"]["key"] = args.key
    
    with open(INIFILE, "w") as configfile:
        config.write(configfile)

def change_listener(device):
    print(device.name + " is now " + str(device.light_control.lights[0].state))

whiteTemps = {"cold":"f5faf6", "normal":"f1e0b5", "warm":"efd275"}

parser = argparse.ArgumentParser()
parser.add_argument("--gateway", "-g")
parser.add_argument("--key")
parser.add_argument("id", nargs='?', default=0)

subparsers = parser.add_subparsers(dest="command")
subparsers.required = True

subparsers.add_parser("on")
subparsers.add_parser("off")
subparsers.add_parser("list")
subparsers.add_parser("test")

parser_level = subparsers.add_parser("level")
parser_level.add_argument("value")

parser_colortemp = subparsers.add_parser("whitetemp")
parser_colortemp.add_argument("value", choices=['cold', 'normal', 'warm'])

args = parser.parse_args()

SaveConfig(args)

api = api_factory(config["Gateway"]["ip"], config["Gateway"]["key"])
gateway = Gateway()

device = api(gateway.get_device(args.id))

if args.command == "on":
    api(device.light_control.set_state(True))

if args.command == "off":
    api(device.light_control.set_state(False))

if args.command == "level":
    api(device.light_control.set_dimmer(int(args.value)))

if args.command == "whitetemp":
    api(device.light_control.set_hex_color(whiteTemps[args.value]))

if args.command == "list":
    devices = api(*api(gateway.get_devices()))

    for aDevice in devices:
        print(aDevice)

if args.command == "test":
    devices = api(*api(gateway.get_devices()))
    lights = [dev for dev in devices if dev.has_light_control]

    lights[0].observe(change_listener)

if args.command == "me":
    pass