from pytradfri import Gateway
from pytradfri.api.aiocoap_api import APIFactory

import asyncio
import aiocoap, logging

async def getDevices(api, gateway):
    devices = await api(await api(gateway.get_devices()))

    lights = []
    outlets = []
    others = []
    groups = []

    for aDevice in sorted(devices, key=lambda device: device.id):
        if aDevice.has_light_control:
            lights.append(aDevice)
        elif aDevice.has_socket_control:
            outlets.append(aDevice)
        else:
            others.append(aDevice)

    groups = await api(await api(gateway.get_groups()))

    return (lights, outlets, groups, others)    


    print ("Lights:")
    for aDevice in sorted(devices, key=lambda device: device.id):
        if aDevice.has_light_control:
            print("{0}: {1} ({2}) - {3}".format(aDevice.id, aDevice.name, aDevice.device_info.model_number, aDevice.light_control.lights[0].state))
        elif aDevice.has_socket_control:
            outlets.append(aDevice)
        else:
            others.append(aDevice)

    print("\nSockets:")
    for aDevice in sorted(outlets, key=lambda device: device.id):
        print("{0}: {1} ({2}) - {3}".format(aDevice.id, aDevice.name, aDevice.device_info.model_number, aDevice.socket_control.sockets[0].state))

    print ("\nDevices:")
    for aDevice in sorted(others, key=lambda device: device.id):
            print("{0}: {1} ({2})".format(aDevice.id, aDevice.name, aDevice.device_info.model_number))

    print("\nGroups:")
    groups = await api(await api(gateway.get_groups()))
    for aGroup in groups:
        print(aGroup)