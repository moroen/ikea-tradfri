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

async def setDeviceState(api, gateway, id, state):
    device = await api(gateway.get_device(str(id)))

    if device.has_light_control:
        await api(device.light_control.set_state(state))
    elif device.has_socket_control:
        await api(device.socket_control.set_state(state))

async def setDeviceLevel(api, gateway, id, value):
    device = await api(gateway.get_device(str(id)))
    await api(device.light_control.set_dimmer(int(value)))
