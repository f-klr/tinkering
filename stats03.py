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

    class Stats:
        __DEFATULT_DIGITS = "01"
        def __init__(self, digits = __DEFATULT_DIGITS):
            self.__digits = digits
            self.__stats = dict(zip(map(int, digits), [0] * len(digits)))

        def _check_digits(self, d):
            if not(d in map(int, self.__digits)):
                raise ValueError("Digits must be: '%s'" % (self.__digits))

        def updateWithOneDigit(self, d):
            self._check_digits(d)
            self.__stats[d] = self.__stats[d] + 1

        def __getitem__(self, d):               # this is a "subscript" replcement
            self._check_digits(d)
            return self.__stats[d]

    @staticmethod
    def _n_to_alpha_digits(r = 2):
        _strip_leading_prefix = lambda s, n=2: s[n:]  
        match r:
            case 2:
                return lambda x: [int(b) for b in _strip_leading_prefix(bin(x)).zfill(8)]
            case 8:
                return lambda x: [int(d) for d in oct(x).zfill(4)]
            case 16:
                return lambda x: [int(h) for h in _strip_leading_prefix(hex(x)).zfill(2)]
        raise ValueError("RADIX must be, either 2, 8 or 16 - check it out!")

    def doSomething(self, n = 10):
        _bits = self._n_to_alpha_digits(2)      # we a get a "lambda" ref. as to convert a numberto "bin" digits
        s = self.Stats("01")                    # here we keep some bin stats

        def _collect_stats(x):
            for b in _bits(x):
                s.updateWithOneDigit(b)

        for x in os.urandom(n): _collect_stats(x)

        return (s[0], s[1])

    def doSomethingGreat(self, x = 100):
        return reduce(lambda a, b: a+b, flatten([np.random.rand(1, 4) for i in range(x)]))

if __name__ == '__main__':
    a1 = App()
    someInstances = [App() for i in range(0, 4)]
    
    for obj, r in App.executeOverInstances():
        print(obj.doSomethingGreat())
        print(r)
