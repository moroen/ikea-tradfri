#!/usr/bin/env python3

import sys
import pytradfri

import argparse

IP = '192.168.1.129'
KEY = 'tuGqA6Er3snmeWsB'

api = pytradfri.coap_cli.api_factory(IP, KEY)
gateway = pytradfri.gateway.Gateway(api)
devices = gateway.get_devices()
lights = [dev for dev in devices if dev.has_light_control]

parser = argparse.ArgumentParser()
parser.add_argument("--gateway", "-g", default=IP)
parser.add_argument("--key", default=KEY)
parser.add_argument("id")


subparsers = parser.add_subparsers(dest="command")
subparsers.required = True

parser_on = subparsers.add_parser("on")

parser_off = subparsers.add_parser("off")

parser_level = subparsers.add_parser("level")
parser_level.add_argument("value")

args = parser.parse_args()

if args.command == "on":
    #lights[int(args.id)].light_control.set_dimmer(50)
    lights[int(args.id)].light_control.set_state(True)

if args.command == "off":
    #lights[int(args.id)].light_control.set_dimmer(0)
    lights[int(args.id)].light_control.set_state(False)

if args.command == "level":
    lights[int(args.id)].light_control.set_dimmer(int(args.value))
