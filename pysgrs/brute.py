import sys
import time
import itertools
import logging

import numpy as np

#from pysgrs import base
#from pysgrs.settings import settings


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s\t%(process)d\t%(levelname)s\t%(message)s')

A = 'EASINTRLUODCPMVGFBQHXJYZKW'

M = np.array([
#   v1 v2 v3 v4 v5 v6 v7 v8
    [1, 1, 1, 1, 0, 0, 0, 0], # S1 FRONT
    [1, 1, 0, 0, 1, 1, 0, 0], # S2 UP
    [1, 0, 0, 1, 1, 0, 0, 1], # S3 RIGHT
    [0, 0, 0, 0, 1, 1, 1, 1], # S4 BACK
    [0, 0, 1, 1, 0, 0, 1, 1], # S5 DOWN
    [0, 1, 1, 0, 0, 1, 1, 0], # S6 LEFT
])

b0 = np.array([64, 46, 62, 48, 57, 53])


def generate(alphabet=A, n=8):
    for x in itertools.product(alphabet, repeat=n):
        yield "".join(x)


def vect(s):
    return np.array([ord(c) - 64 for c in s])


def check(s, b, M=M):
    v = vect(s)
    x = M.dot(v)
    d = x-b
    c = np.allclose(d, 0)
    if c:
        logging.debug("[CHECK] '{}': v={}, x={}, d={}".format(s, v, x, d))
    return c


def bruteforce(b, seq, ic=1000000, file='brute.log'):
    i = 0
    t0 = time.process_time()
    n = 26**8
    for w in seq:
        c = check(w, b)
        if c:
            logging.info("[MATCH] '{}': i={}".format(w, i))
            with open(file, 'a') as fh:
                fh.write(w+'\n')
        i += 1
        if (i % ic) == 0:
            t = time.process_time()
            logging.info("[{:.3f}s] {:.3f}% i={}: {}".format(t-t0, i/n, i, w))
            t0 = t


def main():
    logging.info("Started to bruteforce")

    bruteforce(np.array([64, 53, 62, 46, 57, 48]), seq=["UNEXEMPL"])


    sys.exit(0)


if __name__ == "__main__":
    main()
