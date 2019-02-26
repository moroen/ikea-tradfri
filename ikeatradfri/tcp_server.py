import asyncio
import json
import logging
import signal


from . import config, devices, exceptions
from .server_commands import return_object

from pytradfri import error as Error

class tcp_server():
    _api = None
    _gateway = None
    _api_factory = None

    _server = None

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

                else:
                    returnData = return_object(action=command['action'], status="Error", result="Unknown command")
                
                logging.info("Sending: {0}".format(returnData.json))
                writer.write(returnData.json)
                await writer.drain()

            else:
                logging.info("Closing connection")
                writer.close()
                return

    async def init_gateway(self, command):
        self._api, self._gateway, self._api_factory = await config.connectToGateway()
        return return_object("initGateway", status="Ok")

    async def send_devices_list(self, command):
        try:
            lights, sockets, groups, others = await devices.getDevices(self._api, self._gateway)
        except Error.ServerError:
            return return_object("getDevices", status="Error", result="Server error")

    async def handle_signals(self, loop):
        for signame in {'SIGINT', 'SIGTERM'}:
            logging.debug("Registering {}".format(signame))
            loop.add_signal_handler(
                getattr(signal, signame),
                    lambda: asyncio.ensure_future(self.ask_exit(signame)))

    async def ask_exit(self,signame):
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
        coro = asyncio.start_server(self.handle_echo, '127.0.0.1', 1234, loop=loop)
       
        try:
            server = loop.run_until_complete(coro)
        except exceptions.ConfigNotFound:
            logging.error("SgiteConfig-file not found")

        # Serve requests until Ctrl+C is pressed
        logging.info('Serving on {}'.format(server.sockets[0].getsockname()))
        # try:
        loop.run_forever()
        #except KeyboardInterrupt:
        #    pass

        # Close the server
        #server.close()
        #loop.run_until_complete(server.wait_closed())
        #loop.close()

    async def main(self):
        loop = asyncio.get_event_loop()
        await self.handle_signals(loop)
        
        await config.getConfig()

        
        self._server = await asyncio.start_server(self.handle_echo, '127.0.0.1', 1234)
        
        addr = self._server.sockets[0].getsockname()
        logging.info(f'Serving on {addr}')

        await self._server.serve_forever()
        
if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    server = tcp_server()
    # server.start_tcp_server()