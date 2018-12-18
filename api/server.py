from aiohttp import web
import asyncio
import json, os, signal, functools

if __name__ == "__main__":
    from devices import getDevices
    import config
else:
    from . import devices
    from . import config

PORT = 8085

class Routes():
    api = None
    gateway = None

    routes = web.RouteTableDef()

    @routes.get("/")
    async def index(self, request):
        return web.Response(text="Hello, world")

    @routes.get("/devices/")
    async def listdevices(self, request):
        lights, outlets, groups, others = await devices.getDevices(self.api, self.gateway)
        return web.Response(text=json.dumps(lights))

class TradfriServer():
    routes = web.RouteTableDef()
    api = None
    gateway = None

    async def start(self):
        self.adi, self.gateway = await config.connectToGateway()
        loop = asyncio.get_event_loop()

        for signame in {'SIGINT', 'SIGTERM'}:
            loop.add_signal_handler(
                getattr(signal, signame),
                functools.partial(self.ask_exit, signame))

        app = web.Application()
        routes = Routes()

        app.add_routes(routes.routes)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, 'localhost', PORT)
        
        print("Starting IKEA-Tradfri server on localhost:{0}".format(PORT))
        await site.start()

    def ask_exit(self, signame):
        print("Received signal %s: exiting" % signame)
        loop = asyncio.get_event_loop()
        loop.stop()

if __name__ == "__main__":

    server = TradfriServer()

    future = asyncio.Future()
    loop = asyncio.get_event_loop()
    loop.create_task(server.start())



    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Received exit, exiting")
