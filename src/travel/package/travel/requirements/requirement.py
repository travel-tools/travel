from travel.config.sanitizers import pip_sanitizer
from travel.requirements.constraints import Constraints


class Requirement:

    # Shape: 'grpcio (<2.0dev,>=1.47.0)' or 'google-api-core[grpc,grpcio-gcp] (!=2.0.*)'
    def __init__(self, requirement: str):

        requirement_parts = requirement.split(" ")

        # Get the name of the library
        name = requirement_parts[0]
        if " " in requirement:
            constraints = requirement_parts[1]
            self.constraints = Constraints(constraints)  # TODO check: requests ['urllib3 (<1.27,>=1.21.1)', 'certifi (>=2017.4.17)', 'chardet (<5,>=3.0.2) ; python_version < "3"', 'idna (<3,>=2.5) ; python_version < "3"', 'charset-normalizer (~=2.0.0) ; python_version >= "3"', 'idna (<4,>=2.5) ; python_version >= "3"', "PySocks (!=1.5.7,>=1.5.6) ; extra == 'socks'", 'win-inet-pton ; (sys_platform == "win32" and python_version == "2.7") and extra == \'socks\'', "chardet (<5,>=3.0.2) ; extra == 'use_chardet_on_py3'"]
        else:
            self.constraints = []

        # If extras, get them
        self.extras = []
        if "[" in name:
            parts = name.split("[")
            name = parts[0]
            # Get the second part after "[" but before the last (-1) "]", split by comma
            self.extras = parts[1][-1].split(",")

        self.name = pip_sanitizer.get_package_name(name)
