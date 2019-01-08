from aiohttp import web

try:
    from . import devices as Devices
except ImportError:
    import devices as Devices
    from routes import return_object

import json

def return_object(command=None, status=None, result=None):
    retObj = {}
    if not command is None:
        retObj["command"]=command
    if not status is None:
        retObj["status"]=status
    if not result is None:
        retObj["result"]=result

    return retObj

async def serverCommand(request):
    device = await Devices.get_device(request.app['api'], request.app['gateway'], request.match_info['id'])

    try:
        data = json.loads(await request.read())
        if data["command"] == "setstate":
            await device.set_state(int(data["value"]))
        elif data["command"] == "setlevel":
            await device.set_level(int(data["value"])) 
        else:      
            return return_object(command=data["command"], status="Error", result="Unknown command")
        
        return return_object(command=data["command"], status="Ok", result=device.description)
    except json.decoder.JSONDecodeError:
        return return_object(status="Error", result="Malformed request")
    except Devices.UnsupportedDeviceCommand:
        return return_object(command=data["command"], status="Error", result="Unsupported command")
    except:
        raise