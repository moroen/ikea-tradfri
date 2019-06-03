import os
import uuid
import json

from pytradfri import Gateway
from pytradfri.api.aiocoap_api import APIFactory
import logging
import appdirs

from .exceptions import ConfigNotFound

_API = None
_GATEWAY = None
_API_FACTORY = None


async def getConfig(args=None):
    hostConfig = {}
    showConfig = False

    CONFIGFILE = "{0}/gateway.json".format(appdirs.user_config_dir(appname="tradfri"))
    logging.debug("Looking for config: {}".format(CONFIGFILE))

    # print(CONFIGFILE)
    if args is not None:
        if args.command == "showconfig":
            showConfig = True

        if args.command == "config":
            identity = uuid.uuid4().hex
            api_factory = APIFactory(host=args.IP, psk_id=identity)

            psk = await api_factory.generate_psk(args.KEY)
            hostConfig["Gateway"] = args.IP
            hostConfig["Identity"] = identity
            hostConfig["Passkey"] = psk

            CONFDIR = appdirs.user_config_dir(appname="tradfri")
            if not os.path.exists(CONFDIR):
                os.makedirs(CONFDIR)

            with open(CONFIGFILE, "w") as outfile:
                json.dump(hostConfig, outfile)

            print("Config created!")
            return hostConfig

    if os.path.isfile(CONFIGFILE):
        with open(CONFIGFILE) as json_data_file:
            hostConfig = json.load(json_data_file)
        if showConfig:
            print(hostConfig)
        return hostConfig
    else:
        logging.error("Config-file not found")
        raise ConfigNotFound


async def connectToGateway(storeConfig=False):
    global _API, _API_FACTORY, _GATEWAY

    hostConfig = await getConfig()

    api_factory = APIFactory(
        hostConfig["Gateway"], hostConfig["Identity"], hostConfig["Passkey"]
    )
    api = api_factory.request
    gateway = Gateway()

    if storeConfig:
        _API = api
        _API_FACTORY = api_factory
        _GATEWAY = gateway

    return api, gateway, api_factory
