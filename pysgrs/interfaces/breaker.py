import sys

from pysgrs.settings import settings


def main():
    settings.logger.warning("Hello world!")
    sys.exit(0)


if __name__ == "__main__":
    main()
