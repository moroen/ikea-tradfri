from aiohttp import web

try:
    from . import devices as Devices
    from . import routes as Routes
except ImportError:
    import devices as Devices
    from routes import return_object

import json


async def serverCommand(request):
    device = await Devices.get_device(request.app['api'], request.app['gateway'], request.match_info['id'])
    try:
        data = json.loads(await request.read())
        if data["command"] == "setstate":
            await device.set_state(int(data["value"]))
        
        return Routes.return_object(command=data["command"], status="Ok", result=device.description)

    except json.decoder.JSONDecodeError:
        return Routes.return_object(status="Error", result="Malformed request")
    except:
        raise