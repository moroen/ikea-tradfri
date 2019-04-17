from .devices import get_devices


async def list_devices(api, gateway):
    lights, outlets, groups, others = await get_devices(api, gateway)
    print("Lights:")
    for aDevice in lights:
        print("{0}: {1} ({2}) - {3} - {4}".
              format(aDevice.id, aDevice.name,
                     aDevice.model,
                     aDevice.state,
                     aDevice.hex))

    print("\nSockets:")
    for aDevice in outlets:
        print("{0}: {1} ({2}) - {3}".
              format(aDevice.id, aDevice.name,
                     aDevice.model,
                     aDevice.state))

    print("\nDevices:")
    for aDevice in others:
        print("{0}: {1} ({2}) - {3}".
              format(aDevice.id, aDevice.name,
                     aDevice.model,
                     aDevice.battery_level))

    print("\nGroups:")
    for aGroup in groups:
        print("{0}: {1}".format(
            aGroup.description["DeviceID"], aGroup.description["Name"]))
    return
