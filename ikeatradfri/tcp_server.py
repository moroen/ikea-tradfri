import asyncio
import json
import logging
import signal


from . import config, devices
from .server_commands import return_object

class tcp_server():
    _api = None
    _gateway = None
    _api_factory = None

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
        return return_object("initGateway", status="Ok")

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
        loop.stop()

    def start_tcp_server(self):
        loop = asyncio.get_event_loop()
        coro = asyncio.start_server(self.handle_echo, '127.0.0.1', 1234, loop=loop)
        loop.create_task(self.handle_signals(loop))
        server = loop.run_until_complete(coro)

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

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    server = tcp_server()
    # server.start_tcp_server()
