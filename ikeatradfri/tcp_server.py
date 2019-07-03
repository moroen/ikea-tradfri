import asyncio
import json
import logging
import signal


from . import config, devices as Devices, exceptions, signal_handler
from .server_commands import return_object, connect_to_gateway

from pytradfri import error as Error

HOST = "127.0.0.1"
PORT = 1234

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class tcp_server:
    _api = None
    _gateway = None
    _api_factory = None

    _server = None

    _transition_time = 10

    def __init__(self):
        self._hostConfig = None

    async def handle_echo(self, reader, writer):
        logger.info("Connected from {}".format(writer.get_extra_info("peername")))
        while True:

            data = await reader.readline()
            if data:

                message = data.decode("utf-8")
                addr = writer.get_extra_info("peername")

                if self._hostConfig["Verbosity"] > 0:
                    logger.info("Received {} from {}".format(message, addr))

                command = json.loads(message)

                if command["action"] == "initGateway":
                    returnData = await self.init_gateway(command)

                elif command["action"] == "getDevices":
                    returnData = await self.send_devices_list(command)

                elif command["action"] == "setState":
                    returnData = await self.set_state(command)

                elif command["action"] == "setLevel":
                    returnData = await self.set_level(command)

                elif command["action"] == "setHex":
                    returnData = await self.set_hex(command)

                elif command["action"] == "getChanges":
                    returnData = await self.send_changes(command)

                else:
                    returnData = return_object(
                        action=command["action"],
                        status="Error",
                        result="Unknown command",
                    )

                if self._hostConfig["Verbosity"] > 0:
                    logger.info("Sending: {0}".format(returnData.json))

                writer.write(returnData.json)
                await writer.drain()

            else:
                logger.info("Closing connection")
                writer.close()
                return

    async def init_gateway(self, command):
        try:
            self._api, self._gateway, self._api_factory = await connect_to_gateway(
                self._hostConfig
            )
            return return_object("initGateway", status="Ok")
        except exceptions.ConfigNotFound:
            return return_object(
                "initGateway", status="Error", result="Config-file not found"
            )

    async def send_devices_list(self, command):
        try:
            lights, sockets, groups, others = await Devices.get_devices(
                self._api, self._gateway
            )

            devices = []

            for aDevice in lights:
                devices.append(aDevice.description)

            for aDevice in sockets:
                devices.append(aDevice.description)

            if command["groups"] == "True":
                for aGroup in groups:
                    devices.append(aGroup.description)

            if command["battery_levels"] == "True":
                for aDevice in others:
                    devices.append(aDevice.description)

            return return_object(action="getDevices", status="Ok", result=devices)

        except Error.ServerError:
            return return_object("getDevices", status="Error", result="Server error")

    async def send_changes(self, command):
        try:
            lights, sockets, groups, others = await Devices.get_devices(
                self._api, self._gateway
            )

            devices = []

            for aDevice in lights:
                devices.append(aDevice.description)

            for aDevice in sockets:
                devices.append(aDevice.description)

            if command["groups"] == "True":
                for aGroup in groups:
                    devices.append(aGroup.description)

            if command["battery_levels"] == "True":
                for aDevice in others:
                    devices.append(aDevice.description)

            return return_object(action="getChanges", status="Ok", result=devices)

        except Error.ServerError:
            return return_object("getDevices", status="Error", result="Server error")

    async def set_state(self, command):
        device = await Devices.get_device(self._api, self._gateway, command["deviceID"])
        target_state = None

        if command["state"] == "On":
            target_state = True
        elif command["state"] == "Off":
            target_state = False

        await device.set_state(target_state)

        devices = []
        description = device.description
        if description["Type"] == "Group":
            description["State"] = target_state

        devices.append(description)
        return return_object(action="setState", status="Ok", result=devices)

    async def set_level(self, command):
        device = await Devices.get_device(self._api, self._gateway, command["deviceID"])

        await device.set_level(command["level"], transition_time=self._transition_time)

        devices = []

        description = device.description
        if description["Type"] == "Group":
            # Groups return set level.
            description["Level"] = command["level"]

        devices.append(description)
        return return_object(action="setLevel", status="Ok", result=devices)

    async def set_hex(self, command):
        device = await Devices.get_device(self._api, self._gateway, command["deviceID"])
        await device.set_hex(command["hex"], transition_time=self._transition_time)
        await device.refresh()

        devices = []
        devices.append(device.description)
        return return_object(action="setHex", status="Ok", result=devices)

    async def main(self, hostConfig):
        # loop = asyncio.get_event_loop()
        self._hostConfig = hostConfig

        self._server = await asyncio.start_server(
            self.handle_echo, hostConfig["Server_ip"], hostConfig["Tcp_port"]
        )

        addr = self._server.sockets[0].getsockname()
        logger.info(
            "Starting IKEA-Tradfri TCP server on {0}:{1}".format(addr[0], addr[1])
        )

        # loop.run_until_complete(self._server)
