import getpass, os, shutil
from string import Template


def show_service_file():
    try:
        service_file = "{0}/ikea-tradfri.service".format(os.getcwd())
        with open(service_file, "r") as fin:
            print(fin.read(), end="")
    except FileNotFoundError:
        print(
            "Error: No ikea-tradfri.service-file found!\nGenerate file with 'tradfri service create'"
        )


def create_service_file(user=None, group=None):
    tradfri_binary = shutil.which("tradfri")

    service = {
        "user": getpass.getuser(),
        "group": getpass.getuser(),
        "path": os.getcwd(),
        "tradfri": tradfri_binary,
    }
    if user is not None:
        service["user"] = user
        if group is None:
            service["group"] = user

    if group is not None:
        service["group"] = group

    tpl_path = os.path.abspath(os.path.dirname(__file__))

    tpl = open("{}/ikea-tradfri.service.tpl".format(tpl_path)).read()
    src = Template(tpl)
    result = src.substitute(service)
    try:
        with open("ikea-tradfri.service", "w+") as f:
            f.write(result)

        print("ikea-tradfri.service created:")
        show_service_file()
    except PermissionError:
        if args.debug:
            raise
        else:
            print("Error: Could not write ikea-tradfri.service")
