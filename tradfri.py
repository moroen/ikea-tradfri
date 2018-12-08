#!/usr/bin/env python3

import argparse
import configparser
import os
import uuid,json

from pytradfri import Gateway
from pytradfri.api.aiocoap_api import APIFactory

import asyncio

# INIFILE = "{0}/tradfri.ini".format(os.path.dirname(os.path.realpath(__file__)))

# config = configparser.ConfigParser()

hostConfig = {}

def GetConfig(args=None):
    hostConfig = {}

    CONFIGFILE = "{0}/config.json".format(os.path.dirname(os.path.realpath(__file__)))
 
    if args.command=="config":
        identity = uuid.uuid4().hex
        api_factory = APIFactory(host=args.IP, psk_id=identity)

        psk = api_factory.generate_psk(args.KEY)
        hostConfig["Gateway"] = args.IP
        hostConfig["Identity"] = identity
        hostConfig["Passkey"] = psk

        with open('config.json', 'w') as outfile:
            json.dump(hostConfig, outfile)

        print("Config created!")

        return hostConfig
    elif os.path.isfile(CONFIGFILE):
        with open(CONFIGFILE) as json_data_file:
            hostConfig = json.load(json_data_file)
        return hostConfig
    else:
        print ("Fatal: No config.json found")
        exit()


async def listDevices(api, gateway):
    devices = await api(await api(gateway.get_devices()))

    outlets = []
    others = []

    print ("Lights:")
    for aDevice in devices:
        if aDevice.has_light_control:
            print("{0}: {1} ({2}) - {3}".format(aDevice.id, aDevice.name, aDevice.device_info.model_number, aDevice.light_control.lights[0].state))
        elif aDevice.has_socket_control:
            outlets.append(aDevice)
        else:
            others.append(aDevice)

    print("\nSockets:")
    for aDevice in outlets:
        print("{0}: {1} ({2}) - {3}".format(aDevice.id, aDevice.name, aDevice.device_info.model_number, aDevice.socket_control.sockets[0].state))

    print ("\nDevices:")
    for aDevice in others:
            print("{0}: {1} ({2})".format(aDevice.id, aDevice.name, aDevice.device_info.model_number))

    print("\nGroups:")
    groups = api(api(gateway.get_groups()))
    for aGroup in groups:
        print(aGroup)



def hexToRgb(hex):
    rgb = {}

    rgb["red"] = int(hex[:2], 16)
    rgb["green"] = int(hex[2:4],16)
    rgb["blue"] = int(hex[-2:], 16)

    return rgb


async def setDeviceState(device, state):
    if device.has_light_control:
        api(device.light_control.set_state(state))
    elif device.has_socket_control:
        api(device.socket_control.set_state(state))



# whiteTemps = {"cold":"f5faf6", "normal":"f1e0b5", "warm":"efd275"}

async def run(args):
    hostConfig=GetConfig(args)

    print(hostConfig)

    api_factory = APIFactory(hostConfig["Gateway"], hostConfig["Identity"],hostConfig["Passkey"])
    api = api_factory.request
    gateway = Gateway()

    devices_command = gateway.get_devices()
    devices_commands = await api(devices_command)
    devices = await api(devices_commands)
    
    print(devices)

    await api_factory.shutdown()

    # try:
    #     device = api(gateway.get_device(args.ID))
    # except AttributeError:
    #     pass

    # if args.command == "on":
    #     setDeviceState(device, True)
        
    # if args.command == "off":
    #     setDeviceState(device, False)
        
    # if args.command == "level":
    #     api(device.light_control.set_dimmer(int(args.value)))

    # if args.command == "whitetemp":
    #     api(device.light_control.set_hex_color(whiteTemps[args.value]))

    # if args.command == "list":
    #     await listDevices(api, gateway)

    # if args.command == "hex":
    #     api(device.light_control.set_hex_color(args.value))
        
    # if args.command == "rgb":
    #     rgb = hexToRgb(args.value)
    #     api(device.light_control.set_rgb_color(rgb["red"], rgb["green"], rgb["blue"]))

    # if args.command == "showhex":
    #     print(device.light_control.lights[0].hex_color)

    # if args.command == "test":
    #     #   api(device.light_control.set_rgb_color(0,0,))
    #     # print(device.light_control.lights[0].hex_color)
    #     api(device.light_control.set_kelvin_color(1667))
    #     # print(device.light_control.min_kelvin)

    # if args.command == "me":
    #     pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = False

    parser_config = subparsers.add_parser("config")
    parser_config.add_argument("IP")
    parser_config.add_argument("KEY")
    subparsers.add_parser("on").add_argument("ID")


    subparsers.add_parser("off").add_argument("ID")

    subparsers.add_parser("list")
    subparsers.add_parser("showhex")

    parser_level = subparsers.add_parser("level")
    parser_level.add_argument("value")

    parser_colortemp = subparsers.add_parser("whitetemp")
    parser_colortemp.add_argument("value", choices=['cold', 'normal', 'warm'])

    parser_hex = subparsers.add_parser("hex")
    parser_hex.add_argument("value")

    parser_rgb = subparsers.add_parser("rgb")
    parser_rgb.add_argument("value")

    args = parser.parse_args()

    asyncio.get_event_loop().run_until_complete(run(args))