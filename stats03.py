#!/usr/bin/env python3

#
# this script is a demo showing how to compute bit/stats over a "/random"" source
# also, shows how to keep track of instantiated objects,
# and "iterate" over them, then executing a "default" method,
# that is "doSomething"
#

from functools import partial
from functools import reduce

import os
import numpy as np
from more_itertools import flatten

class Digits:
    __digits = "0123456789abcdefghijklmnopqrstuwxyz"
    __default_r = 2

    @staticmethod
    def __n_to_alpha_digits(radix):
        l = lambda asStr, p, i, x: (asStr(x)[i:]).zfill(p)
        match radix:
            case 2: fn = partial(l, bin, 8, 2)
            case 8: fn = partial(l, oct, 4, 2)
            case 0x10: fn = partial(l, hex, 2, 2)
            case _: raise ValueError("radix must be, either 2, 8 or 16.")
        return lambda x: [int(d, radix) for d in fn(x)]

    __init_stats = lambda self, n: \
        dict(zip(map(int, self.__digits[:n]), [0] * n))

    def __init__(self, radix = __default_r):
        self.__f = self.__n_to_alpha_digits(radix)  # we get a "lambda" ref. as to convert a number to, eg. "bin" digits
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
    def how_many(cls):
        return len(cls.__instances)
  
    @classmethod
    def execute_over_instances(cls):
        for obj in cls.__instances:
            yield obj, obj.do_something()

    def do_something(self, n = 100):
        d = Digits()
        for x in os.urandom(n):
            d.update(x)
        return tuple(d.get())

    def do_something_great(self, n = 100):
        a_few_numbers = [ \
            np.random.rand(1, 10) \
                for i in range(n) \
        ]
        return reduce(lambda a, b: a+b, flatten(a_few_numbers))

if __name__ == '__main__':
    a1 = App()
    someInstances = [App() for i in range(0, 4)]
    for obj, r in App.execute_over_instances():
        print(obj.do_something_great())
        print(r)
