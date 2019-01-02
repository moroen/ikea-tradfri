from pytradfri import Gateway
from pytradfri.api.aiocoap_api import APIFactory

import asyncio
import aiocoap, logging
import json

class ikea_device(object):
    _device = None
    
    def __init__(self, device, api):
        self._device = device
        self.api = api
        #self.deviceID = device.id
        #self.deviceName = device.name
        #self.modelNumber = device.device_info.model_number
        # self.lastState = device.light_control.lights[0].state
        # self.lastLevel = device.light_control.lights[0].dimmer
        # self.lastWB = device.light_control.lights[0].hex_color
        
    @property
    def device_id(self):
        return self._device.id

    @property
    def device_name(self):
        return self._device.name

    @property
    def device_type(self):
        if self._device.has_light_control:
            return "Light"
        if self._device.has_socket_control:
            return "Outlet"

    @property
    def state(self):
        if self._device.has_light_control:
            return self._device.light_control.lights[0].state
        if self._device.has_socket_control:
            return self._device.socket_control.sockets[0].state

    @property
    def device_dimmable(self):
        if self._device.has_light_control:
            return self._device.light_control.can_set_dimmer
        else:
            return False

    @property
    def level(self):
        if not self.device_dimmable:
            return None
        
        return self._device.light_control.lights[0].dimmer
        

    @property
    def device_has_wb(self):
        if self._device.has_light_control:
            return self._device.light_control.can_set_temp
        else:
            return False

    @property
    def device_has_rgb(self):
        if self._device.has_light_control:
            return self._device.light_control.can_set_xy
        else:
            return False

    @property 
    def description(self):
        return {"DeviceID": self.device_id, "Name": self.device_name, "State": self.state, "Level": self.level, "Type": self.device_type, "Dimmable": self.device_dimmable, 
            "HasWB": self.device_has_wb, "HasRGB": self.device_has_rgb}

    async def set_state(self, state):
        if self._device.has_light_control:
            await self.api(self._device.light_control.set_state(state))
        elif self._device.has_socket_control:
            await self.api(self._device.socket_control.set_state(state))

        await self.refresh()

    async def refresh(self):
        gateway = Gateway()
        self.__init__(await self.api(gateway.get_device(int(self.device_id))), self.api)



async def get_device(api, gateway, id):
    targetDevice = await api(gateway.get_device(int(id)))
    return ikea_device(targetDevice, api)

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
