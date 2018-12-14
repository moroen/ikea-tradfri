import os
import uuid,json

from pytradfri import Gateway
from pytradfri.api.aiocoap_api import APIFactory

api = None
gateway = None

def getConfig(args=None):
    hostConfig = {}

    CONFIGFILE = "{0}/../config.json".format(os.path.dirname(os.path.realpath(__file__)))
 
    if args.command=="config":
        identity = uuid.uuid4().hex
        api_factory = APIFactory(host=args.IP, psk_id=identity)

        psk = api_factory.generate_psk(args.KEY)
        hostConfig["Gateway"] = args.IP
        hostConfig["Identity"] = identity
        hostConfig["Passkey"] = psk

        with open('config.json', 'w') as outfile:
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