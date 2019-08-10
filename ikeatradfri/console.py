from .devices import get_devices


async def list_devices(api, gateway, expand_groups=False):
    lights, outlets, groups, others = await get_devices(api, gateway)
    print("Lights:")
    for aDevice in lights:
        print(
            "{0}: {1} ({2}) - {3}:{5} - {4}".format(
                aDevice.id,
                aDevice.name,
                aDevice.model,
                aDevice.state,
                aDevice.hex,
                aDevice.level,
            )
        )

    print("\nSockets:")
    for aDevice in outlets:
        print(
            "{0}: {1} ({2}) - {3}".format(
                aDevice.id, aDevice.name, aDevice.model, aDevice.state
            )
        )

    print("\nDevices:")
    for aDevice in others:
        print(
            "{0}: {1} ({2}) - {3}".format(
                aDevice.id, aDevice.name, aDevice.model, aDevice.battery_level
            )
        )

    print("\nGroups:")
    for aGroup in groups:
        descript = aGroup.description
        print(
            "{0}: {1} - {2}:{3} - {4}".format(
                descript["DeviceID"],
                descript["Name"],
                descript["State"],
                descript["Level"],
                descript["Hex"],
            )
        )
        if expand_groups:
            for aMember in aGroup.members:
                print(" - {0}: {1}".format(aMember.id, aMember.name))

    return
