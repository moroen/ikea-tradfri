from aiohttp import web
import asyncio
import signal
import logging

if __name__ == "__main__":
    import config
    from routes import routes
else:
    from . import config
    from .routes import routes

PORT = 8085
HOST = "127.0.0.1"
APP_FACTORY = None


async def start():
    global APP_FACTORY
    loop = asyncio.get_event_loop()

    app = web.Application()
    app["api"], app["gateway"], APP_FACTORY = await config.connectToGateway()
    app.add_routes(routes)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, HOST, PORT)

    logging.info("Starting IKEA-Tradfri HTTP server on {0}:{1}".format(HOST, PORT))

    await site.start()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.info("Received exit, exiting")
