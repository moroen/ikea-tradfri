import os
import uuid
import json
import asyncio

import logging
import appdirs

from pytradfri import Gateway
from pytradfri.api.aiocoap_api import APIFactory
from pytradfri import error as pyerror

from .exceptions import ConfigNotFound, NoGatewaySpecified

CONFIGFILE = "{0}/gateway.json".format(appdirs.user_config_dir(appname="tradfri"))


class host_config(object):
    _confObj = {}

    def __init__(self):
        self._confObj.update(
            Server_type="Both",
            Gateway=None,
            Server_ip="0.0.0.0",
            Tcp_port=1234,
            Http_port=8085,
            Identity=None,
            Passkey=None,
            Transition_time=10,
            Verbosity=0,
        )
        self.load()

    def load(self):
        if os.path.isfile(CONFIGFILE):
            with open(CONFIGFILE) as json_data_file:
                loaded_conf = json.load(json_data_file)
                for key, value in loaded_conf.items():
                    self._confObj[key] = value
        else:
            self.save()

    def save(self):
        CONFDIR = appdirs.user_config_dir(appname="tradfri")
        if not os.path.exists(CONFDIR):
            os.makedirs(CONFDIR)

        with open(CONFIGFILE, "w") as outfile:
            json.dump(self._confObj, outfile)

        logging.info("Config created")

    def set_config_items(self, **kwargs):
        for key, value in kwargs.items():
            self._confObj[key] = value

    def set_config_item(self, key, value):
        try:
            self._confObj[key.capitalize().replace("-", "_")] = value.capitalize()
        except AttributeError:
            self._confObj[key.capitalize().replace("-", "_")] = value

    @property
    def configuation(self):
        return self._confObj

    @property
    def gateway(self):
        return self._confObj["Gateway"]


async def create_psk(args):
    hostConfig = host_config()

    identity = uuid.uuid4().hex
    api_factory = APIFactory(host=args.IP, psk_id=identity)

    psk = await api_factory.generate_psk(args.KEY)
    hostConfig.set_config_items(Gateway=args.IP, Identity=identity, Passkey=psk)

    hostConfig.save()

    print("Config created!")
    return


def handle_config_command(args):
    conf = host_config()
    conf.load()

    if args.config == None:
        try:
            print(json.dumps(conf.configuation, indent=4, sort_keys=True))
            exit()
        except ConfigNotFound:
            logging.critical("Config file not found!")

    if args.config == "gateway":
        loop = asyncio.get_event_loop()
        loop.run_until_complete(create_psk(args))
    else:
        conf.set_config_item(args.config, args.value)

    conf.save()


def get_config(args):
    confObj = host_config()

    if confObj.gateway is None:
        raise NoGatewaySpecified

    if args.command == "server":
        if args.verbose is not None:
            confObj.set_config_item("Verbosity", args.verbose)

        if args.server_host is not None:
            confObj.set_config_item("Server_ip", args.server_host)

        if args.tcp_port is not None:
            confObj.set_config_item("Tcp_port", args.tcp_port)

        if args.http_port is not None:
            confObj.set_config_item("Http_port", args.http_port)

        if args.server_type is not None:
            confObj.set_config_item("Server_type", args.server_type)

    return confObj.configuation


async def old_getConfig(args=None):
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
