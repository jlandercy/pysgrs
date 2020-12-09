import sys

from pysgrs.interfaces import GenericBreaker
from pysgrs.settings import settings


class HillClimbingBreaker(GenericBreaker):

    def attack(self, text, **kwargs):
        pass


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
