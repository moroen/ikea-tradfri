from aiohttp import web
import asyncio
import signal
import logging

from . import config, exceptions, signal_handler
from .routes import routes

PORT = 8085
HOST = "127.0.0.1"
APP_FACTORY = None


async def start():
    global APP_FACTORY
    loop = asyncio.get_event_loop()

    app = web.Application()
    try:
        app["api"], app["gateway"], APP_FACTORY = await config.connectToGateway()
    
        app.add_routes(routes)

        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, HOST, PORT)

        logging.info("Starting IKEA-Tradfri HTTP server on {0}:{1}".format(HOST, PORT))
        await site.start()

    except exceptions.ConfigNotFound:
        await signal_handler.shutdown("ERROR")
        

    

