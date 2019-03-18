from aiohttp import web
import asyncio
import signal

if __name__ == "__main__":
    import config
    from routes import routes
else:
    from . import config
    from .routes import routes

PORT = 8085
APP_FACTORY = None


async def start():
    global APP_FACTORY
    loop = asyncio.get_event_loop()

    # Signal handlers
    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(
            getattr(signal, signame),
            lambda: asyncio.ensure_future(ask_exit(signame)))

    app = web.Application()
    app["api"], app["gateway"], APP_FACTORY = await config.connectToGateway()
    app.add_routes(routes)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', PORT)

    print("Starting IKEA-Tradfri server on localhost:{0}".format(PORT))

    await site.start()


async def ask_exit(signame):
    global APP_FACTORY
    print("Received signal %s: exiting" % signame)
    await APP_FACTORY.shutdown()
    loop = asyncio.get_event_loop()
    loop.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Received exit, exiting")
