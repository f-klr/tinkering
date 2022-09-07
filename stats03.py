#!/usr/bin/env python3

#
# this script is a demo showing how to compute bit/stats over a "/random"" source
# also, shows how to keep track of instantiated objects,
# and "iterate" over them, then executing a "default" method,
# that is "doSomething"
#

from functools import partial
from functools import reduce
from more_itertools import flatten
import numpy as np
import os

class App:
    __instances = []        # keep tracks of "class" instances

    def __init__(self):
        App.setUp(self)

    @classmethod
    def setUp(cls, obj):
        cls.__instances.append(obj)

    @classmethod
    def howMany(cls):
        return len(cls.__instances)
        
    @classmethod
    def executeOverInstances(cls):
        r = []              # we keep track of both "obj ref", and its "doSomething()" return value
        for obj in cls.__instances:
            r.append((obj, obj.doSomething()))
        return r

    __default_digits = "01"
    __default_r = 2

    @staticmethod
    def _n_to_alpha_digits(r = __default_r):
        _strip_leading_prefix = lambda s, n=2: s[n:]
        _n2a = lambda c, s, p, x: _strip_leading_prefix(c(x), s).zfill(p)
        match r:
            case  2:
                _f = partial(_n2a, bin, 8, 2)
            case  8:
                _f = partial(_n2a, oct, 4, 0)
            case 16:
                _f = partial(_n2a, hex, 2, 2)
        if '_f' in locals():
            return lambda x: [int(d) for d in _f(x)]
        raise ValueError("RADIX must be, either 2, 8 or 16.")

    def doSomething(self, n = 20):
        _bits = self._n_to_alpha_digits()      # we a get a "lambda" ref. as to convert a numberto "bin" digits
        s = dict(zip(map(int, self.__default_digits), [0] * len(self.__default_digits)))
        for x in os.urandom(n):
            for b in _bits(x):
                s[b] = s[b] + 1
        return (s[0], s[1])

    def doSomethingGreat(self, x = 100):
        return reduce(lambda a, b: a+b, flatten([np.random.rand(1, 4) for i in range(x)]))

if __name__ == '__main__':
    a1 = App()
    someInstances = [App() for i in range(0, 4)]
    
    for obj, r in App.executeOverInstances():
        print(obj.doSomethingGreat())
        print(r)
