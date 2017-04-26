#!/usr/bin/env python3

import sys
import pytradfri

import argparse

IP = '192.168.1.129'
KEY = 'NOT_REAL'

whiteTemps = {"cold":"f5faf6", "normal":"f1e0b5", "warm":"efd275"}

api = pytradfri.coap_cli.api_factory(IP, KEY)
gateway = pytradfri.gateway.Gateway(api)

parser = argparse.ArgumentParser()
parser.add_argument("--gateway", "-g", default=IP)
parser.add_argument("--key", default=KEY)
parser.add_argument("id")


subparsers = parser.add_subparsers(dest="command")
subparsers.required = True

subparsers.add_parser("on")
subparsers.add_parser("off")

parser_level = subparsers.add_parser("level")
parser_level.add_argument("value")

parser_colortemp = subparsers.add_parser("whitetemp")
parser_colortemp.add_argument("value", choices=['cold', 'normal', 'warm'])

args = parser.parse_args()

device = gateway.get_device(int(args.id))

if args.command == "on":
    device.light_control.set_state(True)

if args.command == "off":
    device.light_control.set_state(False)

if args.command == "level":
    device.light_control.set_dimmer(int(args.value))

if args.command == "whitetemp":
    device.light_control.set_hex_color(whiteTemps[args.value])
