import os
import uuid,json

from pytradfri import Gateway
from pytradfri.api.aiocoap_api import APIFactory

import appdirs

api = None
gateway = None

async def getConfig(args=None):
    hostConfig = {}

    CONFIGFILE = "{0}/gateway.json".format(appdirs.user_config_dir(appname="tradfri"))
 
    if args.command=="config":
        identity = uuid.uuid4().hex
        api_factory = APIFactory(host=args.IP, psk_id=identity)

        psk = await api_factory.generate_psk(args.KEY)
        hostConfig["Gateway"] = args.IP
        hostConfig["Identity"] = identity
        hostConfig["Passkey"] = psk

        CONFDIR = appdirs.user_config_dir(appname="tradfri")
        if not os.path.exists(CONFDIR):
            os.makedirs(CONFDIR)

        with open(CONFIGFILE, 'w') as outfile:
            json.dump(hostConfig, outfile)

        print("Config created!")

        return hostConfig
    elif os.path.isfile(CONFIGFILE):
        with open(CONFIGFILE) as json_data_file:
            hostConfig = json.load(json_data_file)
        return hostConfig
    else:
        print ("Fatal: No config.json found")
        exit()

async def connectToGateway():
    hostConfig=await getConfig()

    api_factory = APIFactory(hostConfig["Gateway"], hostConfig["Identity"],hostConfig["Passkey"])
    api = api_factory.request
    gateway = Gateway()

    return api, gateway