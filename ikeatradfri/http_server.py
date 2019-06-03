from aiohttp import web
import asyncio
import signal
import logging

from . import config, exceptions, signal_handler
from .routes import routes

PORT = 8085
HOST = "127.0.0.1"
APP_FACTORY = None


async def start(host=None, port=None):
    global APP_FACTORY
    loop = asyncio.get_event_loop()

    app = web.Application()
    try:
        app["api"], app["gateway"], APP_FACTORY = await config.connectToGateway()

        app.add_routes(routes)

        runner = web.AppRunner(app)
        await runner.setup()

        if host is None:
            host = HOST
        if port is None:
            port = PORT

        site = web.TCPSite(runner, host, port)

        logging.info("Starting IKEA-Tradfri HTTP server on {0}:{1}".format(host, port))
        await site.start()

    except exceptions.ConfigNotFound:
        await signal_handler.shutdown("ERROR")
