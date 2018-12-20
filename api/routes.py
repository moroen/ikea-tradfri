from aiohttp import web

try:
    from . import devices as Devices
except ImportError:
    import devices as Devices

import json

routes = web.RouteTableDef()

@routes.get('/')
async def index(request):
    return web.Response(text="Hello, world")
   
@routes.get('/devices')
async def listdevices(request):
    devices =[] 
    lights, outlets, groups, others = await Devices.getDevices(request.app["api"], request.app["gateway"])
        
    for aDevice in lights:
        devices.append({"DeviceID": aDevice.id, "Name": aDevice.name, "Type": "Light", "Dimmable": aDevice.light_control.can_set_dimmer, "HasWB": aDevice.light_control.can_set_temp, "HasRGB": aDevice.light_control.can_set_xy})

    return web.Response(text=json.dumps(devices))
