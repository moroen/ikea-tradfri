from aiohttp import web

PORT = 8085

routes = web.RouteTableDef()

@routes.get("/")
async def index(request):
    return web.Response(text="Hello, world")

async def server():
    print("Starting IKEA-Tradfri server on localhost:{0}".format(PORT))
    app = web.Application()
    app.add_routes(routes)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', PORT)
    await site.start()
