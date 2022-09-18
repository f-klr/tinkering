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

class Digits:
    __digits = "0123456789abcdefghijklmnopqrstuwxyz"
    __default_r = 2

    @staticmethod
    def __n_to_alpha_digits(r):
        _strip_leading_prefix = lambda s, n=2: s[n:]
        _n2a = lambda c, s, p, x: _strip_leading_prefix(c(x), s).zfill(p)
        match r:
            case 0x02: _f = partial(_n2a, bin, 8, 2)
            case 0x08: _f = partial(_n2a, oct, 4, 0)
            case 0x10: _f = partial(_n2a, hex, 2, 2)
            case _: raise ValueError("radix must be, either 2, 8 or 16.")
        return lambda x: [int(d) for d in _f(x)]

    __init_stats = lambda self, n: \
        dict(zip(map(int, self.__digits[:n]), [0] * n))

    def __init__(self, r):
        self.__f = self.__n_to_alpha_digits(r)     # we a get a "lambda" ref. as to convert a number to, eg. "bin" digits
        self.__s = self.__init_stats(r)

    def update(self, n):
        for i in self.__f(n):
            self.__s[i] = self.__s[i] + 1

    def get(self):
        return tuple([self.__s[k] for k in sorted(self.__s.keys())])

class App:
    __instances = []        # keep tracks of "class" instances

    def __init__(self):
        App.setUp(self)

    @classmethod
    def setUp(cls, obj):
        return cls.__instances.append(obj)

    @classmethod
    def howMany(cls):
        return len(cls.__instances)
        
    @classmethod
    def executeOverInstances(cls):
        refs = []               # we keep track of both "obj ref", and its "doSomething()" return value
        for obj in cls.__instances:
            refs.append((obj, obj.doSomething()))
        return refs
    
    def doSomething(self, n = 100):
        d = Digits(8)
        for x in os.urandom(n):
            d.update(x)
        return d.get()

    def doSomethingGreat(self, x = 100):
        s2 = lambda a, b: a+b
        nl = [np.random.rand(1, 4) for i in range(x)]
        return reduce(s2, flatten(nl))

if __name__ == '__main__':
    a1 = App()
    someInstances = [App() for i in range(0, 4)]
    
    for obj, r in App.executeOverInstances():
        print(obj.doSomethingGreat())
        print(r)
