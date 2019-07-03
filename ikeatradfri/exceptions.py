class UnsupportedDeviceCommand(Exception):
    pass


class ConfigNotFound(Exception):
    # logging.error("Config not found")
    pass


class NoGatewaySpecified(Exception):
    pass
