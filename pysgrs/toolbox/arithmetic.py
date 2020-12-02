import sys
import math

from pysgrs import errors
from pysgrs.settings import settings


class Arithmetic:
    pass


class ModularArithmetic(Arithmetic):

    @staticmethod
    def gcd(a, b):
        # https://en.wikipedia.org/wiki/Greatest_common_divisor
        return math.gcd(a, b)

    @staticmethod
    def lcm(a, b):
        # https://en.wikipedia.org/wiki/Least_common_multiple
        return abs(a * b) // math.gcd(a, b)

    @staticmethod
    def egcd(a, b):
        # https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
        if a == 0:
            return b, 0, 1
        else:
            g, y, x = ModularArithmetic.egcd(b % a, a)
            return g, x - (b // a) * y, y

    @staticmethod
    def modinv(a, m):
        # https://en.wikipedia.org/wiki/Modular_multiplicative_inverse
        try:
            # Only Python 3.8+
            return pow(a, -1, m)
        except ValueError:
            g, x, y = ModularArithmetic.egcd(a, m)
            if g != 1:
                raise errors.IllegalParameter('Modular inverse does not exist for {} mod {}'.format(a, m))
            else:
                return x % m

    @staticmethod
    def factor(a):
        import sympy
        return sympy.factorint(a)

    @staticmethod
    def is_prime(a):
        import sympy
        return sympy.isprime(a)


def main():
    sys.exit(0)


if __name__ == "__main__":
    main()
