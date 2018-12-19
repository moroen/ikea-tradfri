from aiohttp import web
import asyncio
import json, os, signal, functools

if __name__ == "__main__":
    import devices as Devices
    import config
else:
    from . import devices as Devices
    from . import config

PORT = 8085

class Routes():
    api = None
    gateway = None
    api_factory = None


    # @routes.get("/")
    async def index(self,request):
        return web.Response(text="Hello, world")

    
    #@routes.get("/devices/")
    async def listdevices(self, request):
        devices =[] 
        lights, outlets, groups, others = await Devices.getDevices(self.api, self.gateway)
        
        for aDevice in lights:
            devices.append({"DeviceID": aDevice.id, "Name": aDevice.name, "Type": "Light", "Dimmable": aDevice.light_control.can_set_dimmer, "HasWB": aDevice.light_control.can_set_temp, "HasRGB": aDevice.light_control.can_set_xy})

        return web.Response(text=json.dumps(devices))

class TradfriServer():
    routes = web.RouteTableDef()
    api = None
    gateway = None

    async def start(self):
        self.api, self.gateway, self.api_factory = await config.connectToGateway()
        loop = asyncio.get_event_loop()

        # for signame in {'SIGINT', 'SIGTERM'}:
        #     loop.add_signal_handler(
        #         getattr(signal, signame),
        #         functools.partial(self.ask_exit, signame))

        for signame in {'SIGINT', 'SIGTERM'}:
            loop.add_signal_handler(
                getattr(signal, signame),
                    lambda: asyncio.ensure_future(self.ask_exit(signame)))

        app = web.Application()
        
        # app.add_routes(self.routes)
        
        app.add_routes([web.get('/', self.index), web.get('/devices', self.listdevices)])

        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, 'localhost', PORT)
        
        print("Starting IKEA-Tradfri server on localhost:{0}".format(PORT))

        await site.start()

    async def ask_exit(self, signame):
        print("Received signal %s: exiting" % signame)
        await self.api_factory.shutdown()
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
