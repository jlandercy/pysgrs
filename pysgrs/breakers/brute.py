import sys

from pysgrs.interfaces import GenericBreaker
from pysgrs.settings import settings


class BruteForceBreaker(GenericBreaker):

    def attack(self, text, **kwargs):
        pass


def main():
    settings.logger.warning("Hello world!")
    sys.exit(0)


if __name__ == "__main__":
    main()
