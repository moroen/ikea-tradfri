#!/usr/bin/env python3

import argparse
import configparser
import os, signal
import uuid,json

from pytradfri import Gateway
from pytradfri.api.aiocoap_api import APIFactory

import asyncio, functools
import aiocoap, logging
from api import cli, devices, config, console

hostConfig = {}

logging.basicConfig(level=logging.FATAL)
 

def hexToRgb(hex):
    rgb = {}

    rgb["red"] = int(hex[:2], 16)
    rgb["green"] = int(hex[2:4],16)
    rgb["blue"] = int(hex[-2:], 16)

    return rgb






# whiteTemps = {"cold":"f5faf6", "normal":"f1e0b5", "warm":"efd275"}

async def run(args):
    
    hostConfig=await config.getConfig(args)

    api_factory = APIFactory(hostConfig["Gateway"], hostConfig["Identity"],hostConfig["Passkey"])
    api = api_factory.request
    gateway = Gateway()

    # devices_command = gateway.get_devices()
    # devices_commands = await api(devices_command)
    # devices = await api(devices_commands)
    
    if args.command == "server":
        from api import server as Server
        await Server.server()
   
    if args.command == "on":
        await devices.setDeviceState(api, gateway, args.ID, True)
        
    if args.command == "off":
        await devices.setDeviceState(api, gateway, args.ID,
         False)
        
    if args.command == "level":
         await devices.setDeviceLevel(api, gateway, args.ID, args.value)

    # if args.command == "whitetemp":
    #     api(device.light_control.set_hex_color(whiteTemps[args.value]))

    if args.command == "list":
        await console.listDevices(api, gateway)

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

    await api_factory.shutdown()

def ask_exit(signame):
    print("Received signal %s: exiting" % signame)
    loop.stop()

if __name__ == "__main__":
    args = cli.getArgs()
    if args.command == "server":
        from api import server as Server
        future = asyncio.Future()
        loop = asyncio.get_event_loop()
        loop.create_task(Server.server())

        for signame in {'SIGINT', 'SIGTERM'}:
            loop.add_signal_handler(
                getattr(signal, signame),
                functools.partial(ask_exit, signame))

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            print("Received exit, exiting")
        
    else:
        asyncio.get_event_loop().run_until_complete(run(args))
    