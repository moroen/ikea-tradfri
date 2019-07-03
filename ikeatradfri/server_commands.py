import json

try:
    from . import devices as Devices
except ImportError:
    import devices as Devices


from pytradfri import Gateway
from pytradfri.api.aiocoap_api import APIFactory
from pytradfri import error as pyerror


class return_object:
    def __init__(self, action=None, status="Error", result=None):
        self._action = action
        self._status = status
        self._result = result

    @property
    def json(self):
        if self._result is not None:
            return json.dumps(
                {"action": self._action, "status": self._status, "result": self._result}
            ).encode("utf-8")
        else:
            return json.dumps({"action": self._action, "status": self._status}).encode(
                "utf-8"
            )


async def connect_to_gateway(hostConfig):

    api_factory = APIFactory(
        hostConfig["Gateway"], hostConfig["Identity"], hostConfig["Passkey"]
    )
    api = api_factory.request
    gateway = Gateway()

    return api, gateway, api_factory


async def serverCommand(request):
    device = await Devices.get_device(
        request.app["api"], request.app["gateway"], request.match_info["id"]
    )

    try:
        data = json.loads(await request.read())
        if data["command"] == "setstate":
            await device.set_state(int(data["value"]))
        elif data["command"] == "setlevel":
            await device.set_level(int(data["value"]))
        else:
            return return_object(
                action=data["command"], status="Error", result="Unknown command"
            )

        return return_object(
            action=data["command"], status="Ok", result=device.description
        )
    except json.decoder.JSONDecodeError:
        return return_object(status="Error", result="Malformed request")
    except Devices.UnsupportedDeviceCommand:
        return return_object(
            action=data["command"], status="Error", result="Unsupported command"
        )
    except BaseException:
        raise
