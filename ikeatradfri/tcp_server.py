import asyncio
import json
import logging
import signal


from . import config, devices as Devices, exceptions
from .server_commands import return_object

from pytradfri import error as Error


class tcp_server():
    _api = None
    _gateway = None
    _api_factory = None

    _server = None

    _transition_time = 10

    def __init__(self, autostart=True):
        if autostart:
            self.start_tcp_server()

    async def handle_echo(self, reader, writer):
        while True:

            data = await reader.readline()
            if data:

                message = data.decode("utf-8")
                addr = writer.get_extra_info('peername')

                logging.info(f"Received {message!r} from {addr!r}")

                command = json.loads(message)

                if command["action"] == "initGateway":
                    returnData = await self.init_gateway(command)

                elif command['action'] == "getDevices":
                    returnData = await self.send_devices_list(command)

                elif command["action"] == "setState":
                    returnData = await self.set_state(command)

                elif command["action"] == "setLevel":
                    returnData = await self.set_level(command)

                elif command["action"] == "setHex":
                    returnData = await self.set_hex(command)

                else:
                    returnData = return_object(
                        action=command['action'],
                        status="Error",
                        result="Unknown command")

                logging.info("Sending: {0}".format(returnData.json))
                writer.write(returnData.json)
                await writer.drain()

            else:
                logging.info("Closing connection")
                writer.close()
                return

    async def init_gateway(self, command):
        self._api, self._gateway, self._api_factory = \
            await config.connectToGateway()
        return return_object("initGateway", status="Ok")

    async def send_devices_list(self, command):
        try:
            lights, sockets, groups, others = await Devices.getDevices(
                self._api, self._gateway)

            devices = []

            for aDevice in lights:
                devices.append({"DeviceID": aDevice.id,
                                "Name": aDevice.name,
                                "Type": "Light",
                                "Dimmable":
                                aDevice.light_control.can_set_dimmer,
                                "HasWB": aDevice.light_control.can_set_temp,
                                "HasRGB": aDevice.light_control.can_set_xy,
                                "State": aDevice.light_control.lights[0].state,
                                "Level":
                                aDevice.light_control.lights[0].dimmer,
                                "Hex":
                                aDevice.light_control.lights[0].hex_color})

            for aDevice in sockets:
                devices.append({"DeviceID": aDevice.id,
                                "Name": aDevice.name,
                                "Type": "Outlet",
                                "Dimmable": False,
                                "HasWB": False,
                                "HasRGB": False,
                                "State":
                                aDevice.socket_control.sockets[0].state})

            for aGroup in groups:
                devices.append({"DeviceID": aGroup.id,
                                "Name": aGroup.name,
                                "Type": "Group",
                                "Dimmable": True,
                                "HasWB": False,
                                "HasRGB": False,
                                "State": aGroup.state,
                                "Level": aGroup.dimmer})

            for aDevice in others:
                devices.append({"DeviceID": aDevice.id,
                                "Name": aDevice.name,
                                "Type": "Battery_Level",
                                "Dimmable": False,
                                "HasWB": False,
                                "Level": aDevice.device_info.battery_level})

            return return_object(
                action="getDevices",
                status="Ok",
                result=devices)

        except Error.ServerError:
            return return_object(
                "getDevices",
                status="Error",
                result="Server error")

    async def set_state(self, command):
        device = await Devices.get_device(
            self._api, self._gateway, command["deviceID"])
        if command["state"] == "On":
            await device.set_state(True)
        elif command["state"] == "Off":
            await device.set_state(False)

        await device.refresh()

        devices = []
        devices.append(device.description)
        return return_object(action="setState", status="Ok", result=devices)

    async def set_level(self, command):
        device = await Devices.get_device(
            self._api, self._gateway, command["deviceID"])

        await device.set_level(command["level"],
                               transition_time=self._transition_time)
        await device.refresh()

        devices = []
        devices.append(device.description)
        return return_object(action="setLevel", status="Ok", result=devices)

    async def set_hex(self, command):
        device = await Devices.get_device(self._api, self._gateway,
                                          command["deviceID"])
        await device.set_hex(command["hex"],
                             transition_time=self._transition_time)
        await device.refresh()

        devices = []
        devices.append(device.description)
        return return_object(action="setHex", status="Ok", result=devices)

    async def handle_signals(self, loop):
        for signame in {'SIGINT', 'SIGTERM'}:
            logging.debug("Registering {}".format(signame))
            loop.add_signal_handler(
                getattr(signal, signame),
                lambda: asyncio.ensure_future(self.ask_exit(signame)))

    async def ask_exit(self, signame):
        global _run_server
        logging.info("Received signal %s: exiting" % signame)
        loop = asyncio.get_event_loop()

        logging.info("Stopping TCP-server")
        self._server.close()
        await self._server.wait_closed()
        await asyncio.sleep(1)
        loop.close()

    def start_tcp_server(self):
        loop = asyncio.get_event_loop()

        loop.create_task(config.getConfig())
        loop.create_task(self.handle_signals(loop))
        coro = asyncio.start_server(
            self.handle_echo, '127.0.0.1', 1234, loop=loop)

        try:
            server = loop.run_until_complete(coro)
        except exceptions.ConfigNotFound:
            logging.error("SgiteConfig-file not found")

        # Serve requests until Ctrl+C is pressed
        logging.info('Serving on {}'.format(server.sockets[0].getsockname()))
        # try:
        loop.run_forever()
        # except KeyboardInterrupt:
        #    pass

        # Close the server
        # server.close()
        # loop.run_until_complete(server.wait_closed())
        # loop.close()

    async def main(self):
        loop = asyncio.get_event_loop()
        await self.handle_signals(loop)

        await config.getConfig()

        self._server = await asyncio.start_server(
            self.handle_echo, '127.0.0.1', 1234)

        addr = self._server.sockets[0].getsockname()
        logging.info(f'Serving on {addr}')

        await self._server.serve_forever()
