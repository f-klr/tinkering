#!/usr/bin/env python3

#
# this script is a demo showing how to compute bit/stats over a "/random"" source
# also, shows how to keep track of instantiated objects,
# and "iterate" over them, then executing a "default" method,
# that is "doSomething"
#

from functools import reduce
from more_itertools import flatten
import numpy as np
import os
import textwrap

class App:
    __instances = []

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
        for obj in cls.__instances:
            yield (obj, obj.doSomething())
        # stateless

    def doSomething(self, n = 10):
        d0 = 0
        d1 = 0
        rj = lambda s: ''.join(reversed(s))
        octs = lambda n: [rj(o).zfill(8) for o in reversed(textwrap.wrap(rj(bin(n)[2:]), 8))]
        bits = lambda n: [int(b) for b in flatten(octs(n))]
        for x in os.urandom(10):
            for b in bits(x):
                match b:
                    case 0: d0 = d0 + 1
                    case 1: d1 = d1 + 1
        return (d0, d1)

    def doSomethingGreat(self, x = 100):
        return reduce(lambda a, b: a+b, flatten([np.random.rand(1, 4) for i in range(x)]))

if __name__ == '__main__':
    a1 = App()
    a2 = App()
    a3 = App()
    a4 = App()
    for obj, r in App.executeOverInstances():
        print(obj.doSomethingGreat())
        print(r)
