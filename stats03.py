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
        strip_leading_prefix = lambda s, n=2: s[n:]
        n2a = lambda c, s, p, x: strip_leading_prefix(c(x), s).zfill(p)
        match r:
            case 0x02:
                fn = partial(n2a, bin, 8, 2)
            case 0x08:
                fn = partial(n2a, oct, 4, 0)
            case 0x10:
                fn = partial(n2a, hex, 2, 2)
            case _: raise ValueError("radix must be, either 2, 8 or 16.")
        return lambda x: [int(d) for d in fn(x)]

    __init_stats = lambda self, n: \
        dict(zip(map(int, self.__digits[:n]), [0] * n))

    def __init__(self, radix):
        self.__f = self.__n_to_alpha_digits(radix)  # we a get a "lambda" ref. as to convert a number to, eg. "bin" digits
        self.__s = self.__init_stats(radix)

    def update(self, n):
        for i in self.__f(n):
            self.__s[i] = self.__s[i] + 1

    def get(self):
        for k in sorted(self.__s.keys()):
            yield self.__s[k]

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
        d = Digits(2)
        for x in os.urandom(n):
            d.update(x)
        return tuple(d.get())

    def doSomethingGreat(self, n = 100):
        a_few_numbers = [ \
            np.random.rand(1, 10) \
                for i in range(n) \
        ]
        return reduce(lambda a, b: a+b, flatten(a_few_numbers))

if __name__ == '__main__':
    a1 = App()
    someInstances = [App() for i in range(0, 4)]
    for obj, r in App.executeOverInstances():
        print(obj.doSomethingGreat())
        print(r)
