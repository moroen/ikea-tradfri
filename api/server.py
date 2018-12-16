from aiohttp import web
import json

if __name__ == "__main__":
    from devices import getDevices
    import config
else:
    from .devices import getDevices
    from.config import *

PORT = 8085

routes = web.RouteTableDef()

@routes.get("/")
async def index(request):
    return web.Response(text="Hello, world")

@routes.get("/devices/")
async def listdevices(request):
    lights, outlets, groups, others = await getDevices(api, gateway)
    return web.Response(text=json.dumps(lights))

async def server(api, config):
    global api
    global gateway


    print("Starting IKEA-Tradfri server on localhost:{0}".format(PORT))
    app = web.Application()
    app.add_routes(routes)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', PORT)
    await site.start()

if __name__ == "__main__":

    global api
    global gateway

    api, gateway = config.connectToGateway()

    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, port=8085)
