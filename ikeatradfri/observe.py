import asyncio
import signal

if __name__ == "__main__":
    import devices as Devices
    import config
else:
    from . import devices as Devices
    from . import config

PORT = 8085
APP_FACTORY = None


async def observe():
    global APP_FACTORY
    loop = asyncio.get_event_loop()

    # Signal handlers
    for signame in {"SIGINT", "SIGTERM"}:
        loop.add_signal_handler(
            getattr(signal, signame), lambda: asyncio.ensure_future(ask_exit(signame))
        )

    api, gateway, APP_FACTORY = await config.connectToGateway()

    # Callback
    def observe_callback(updated_device):
        light = updated_device.light_control.lights[0]
        print("Received message for: %s" % light)

    def observe_err_callback(err):
        print("observe error:", err)

    lights, _, _, _ = await Devices.getDevices(api, gateway)

    for light in lights:
        observe_command = light.observe(
            observe_callback, observe_err_callback, duration=0
        )
        # Start observation as a second task on the loop.
        asyncio.ensure_future(api(observe_command))

        await asyncio.sleep(0)


async def ask_exit(signame):
    global APP_FACTORY
    print("Received signal %s: exiting" % signame)
    await APP_FACTORY.shutdown()
    loop = asyncio.get_event_loop()
    loop.stop()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(observe())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Received exit, exiting")
