import asyncio, signal, logging

async def handle_signals(loop):
    for signame in {'SIGINT', 'SIGTERM'}:
        logging.debug("Registering {}".format(signame))
        loop.add_signal_handler(
            getattr(signal, signame),
            lambda: asyncio.ensure_future(shutdown(signame)))

async def shutdown(signame):
    logging.info("Received signal %s: exiting" % signame)
    loop = asyncio.get_event_loop()

    #logging.info("Stopping TCP-server")
    #self._server.close()
    #loop.run_until_complete(self._server.wait_closed())
    # await self._server.wait_closed()
    #await asyncio.sleep(1)
    #loop.close()

    tasks = [task for task in asyncio.Task.all_tasks() if task is not
            asyncio.tasks.Task.current_task()]
    
    list(map(lambda task: task.cancel(), tasks))
    results = await asyncio.gather(*tasks, return_exceptions=True)
    logging.info('Finished awaiting cancelled tasks!')
    loop.stop()