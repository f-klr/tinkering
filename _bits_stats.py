#!/usr/bin/env python3

#
# this script is a demo showing how to compute bit/stats over a "/random" source
# also, shows how to keep track of instantiated objects,
# and "iterate" over them, then executing a "default" method,
# that is "doSomething"
#

from functools import reduce
from more_itertools import flatten
import textwrap
import os

class Bytes:
    def __init__(self, l):
        self.__list = l

    def asBitStream(self, zfill = -1):
        c = 0
        for n in self.__list:
            while True:
                yield n % 2
                c = c + 1
                if (n == 0):
                    if (zfill <= 0) or not(c % zfill):
                        break
                n = n >> 1

    def asOctects(self):
        b = lambda n: bin(n)[2:]
        r = lambda l: ''.join(reversed(l))
        l = lambda n: textwrap.wrap(r(b(n)), 8)
        for n in self.__list:
            for chunk in reversed(l(n)):
                if not(chunk):
                    break        
                yield r(chunk).zfill(8)

class App:
    __instances = []

    def __init__(self):
        self.__list = Bytes(os.urandom(10))
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

    def doSomething(self):
        s = { 0: 0, 1: 0 }
        for b in self.__list.asBitStream(zfill = 8):
            s[b] = s[b] + 1
        return (s[0], s[1])

    def doSomethingElse(self):
        return list(self.__list.asOctects())

if __name__ == '__main__':

    a1 = App()
    a2 = App()
    a3 = App()

    for (o, x) in App.executeOverInstances():
        print(x)
        print(o.doSomethingElse())
