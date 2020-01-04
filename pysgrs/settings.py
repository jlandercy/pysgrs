import os
import sys
import uuid
import pathlib
import logging.config
import json

from types import SimpleNamespace

# Settings Namespace:
settings = SimpleNamespace()

# Directories:
settings.home = pathlib.Path.home()
settings.package = pathlib.Path(__file__).parent
settings.resources = settings.package/'resources'
settings.name = settings.package.parts[-1]

# Logger:
settings.logger = logging.getLogger(settings.name)
with (settings.resources/'logging.json').open('r') as fh:
    logging.config.dictConfig(json.load(fh))

# Application Settings:
settings.database = os.environ.get('DATABASE', 'sqlite://')
settings.secretkey = os.environ.get('SECRETKEY', os.urandom(64))
settings.uuid4 = uuid.uuid4()


def main():
    import pprint
    settings.logger.info(settings.__dict__)
    sys.exit(0)


if __name__ == "__main__":
    main()
