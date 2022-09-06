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
        r = []              # here we keep track of both "obj ref", and its doSomething return value
        for obj in cls.__instances:
            r.append((obj, obj.doSomething()))
        return r

    @staticmethod
    def _bits():
        return lambda x: [int(b) for b in bin(x)[2:].zfill(8)]

    def doSomething(self, n = 10):
        bits = self._bits()
        d0, d1 = 0, 0 
        for x in os.urandom(n):
            for b in bits(x):
                match b:
                    case 0: d0 = d0 + 1
                    case 1: d1 = d1 + 1
        return (d0, d1)

    def doSomethingGreat(self, x = 100):
        return reduce(lambda a, b: a+b, flatten([np.random.rand(1, 4) for i in range(x)]))

if __name__ == '__main__':
    a1 = App()
    someInstances = [App() for i in range(0, 4)]
    
    for obj, r in App.executeOverInstances():
        print(obj.doSomethingGreat())
        print(r)
