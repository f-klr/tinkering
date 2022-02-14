#!/usr/bin/env python3

#
# this script is a demo showing how to compute bit/stats over a "/random" source
# also, shows how to keep track of instantiated objects,
# and "iterate" over them, then executing a "default" method,
# that is "doSomething"
#

from functools import reduce
from more_itertools import flatten
import numpy as np
import os

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

    @staticmethod
    def bits(n, zfill = -1):
        c = 0
        while True:
            yield n % 2
            c = c + 1
            if (n == 0) and ((zfill > 0) or not(c % zfill)):
                break
            else:
                n = n >> 1

    def doSomething(self, n = 10):
        d0 = 0
        d1 = 0
        for x in os.urandom(n):
            for b in App.bits(x, 8):
                if b == 0:
                    d0 = d0 + 1
                elif b == 1:
                    d1 = d1 + 1
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
