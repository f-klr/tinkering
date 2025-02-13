#!/usr/bin/env python3.13

from functools import partial, cache
from typing import Callable, List, Any
import string, random

class Converter:

    class Stats:       
        def __init__(self: object):
            self.class_instances = 0
            self.count = 0
            self.stats = {}
            
        def update_class_info(self: object):
            self.class_instances = self.class_instances + 1

        def update(self: object, n: string):
            self.count = self.count + 1
            for c in list(n):
                if c in self.stats.keys():
                    self.stats[c]['count'] = self.stats[c]['count'] + 1
                else:
                    self.stats[c] = { 'count' : 0 }
                    
        def show(self: object):
            print("Hoe many instances - %d" % (self.class_instances))
            for k in sorted(self.stats.keys()):
                print("\t\t%s - %d" % (k, self.stats[k]['count']))
            

    # Statistica about classes/objcts,
    # .. conversions and specific digits/letters being generated .
    stats = Stats()
    
    @staticmethod
    def show_stats():
        Converter.stats.show()

    @cache
    @staticmethod
    def get_partial_by_base(base: int) -> Callable:
        def convert_by_base(base: int, n: int) -> Callable:
            if n < 0: raise ValueError("We only convert positive numbers sorry :/")
            while True:
                x = n % base
                n = int(n / base)
                if x < 10:
                    yield str(x)
                else:
                    yield chr(ord('a') -10 + x)
                if n == 0:
                    return
        return partial(convert_by_base, base)

    @cache
    @staticmethod
    def lookup(base: int) -> Callable:
        ic = {
            0x02: [ bin, 8, 2 ],
            0x08: [ oct, 4, 2 ],
            0x0a: [ str, 0, 0 ],    # special case ... radix = 10 :)
            0x10: [ hex, 2, 2 ] 
        }
        l = lambda f, n, i, x: [ d for d in f(x)[i:].zfill(n).lower() ]
        match base:
            case x if x in ic.keys():
                p = partial(l, *ic[base])
            case _:
                p = Converter.get_partial_by_base(base)
        return p         # this is a "lambda fn" - not a data structure !!

    def as_list(self: object, n: int) -> List[Any]:
        if n < 0: raise ValueError("We only convert positive numbers sorry :/")
        p = Converter.lookup(self.base)
        x = p(n)
        Converter.stats.update(x)
        return [ int(d, self.base) if d in string.digits else d for d in p(n) ]

    def __init__(self: object, base: int) -> object:
        if not base in range(2, 36):
            raise ValueError("Err ! actually, a 'base' must be between 2 and 36")
        self.base = base
        Converter.stats.update_class_info()

    def __call__(self: object, n: int) -> List[Any]:
        return self.as_list(n)

C16 = Converter(16)
C12 = Converter(12)

as_binary = lambda n: Converter(2).as_list(n)
as_hex = lambda n: C16(n)
as_base12 = lambda n: C12.as_list(n)

how_many = random.randrange(0, 10_000)
for i in range(0, how_many):
    x = random.randrange(1, 1_000_000)
    for f in [as_binary, as_hex, as_base12]:
        f(x)

Converter.show_stats()

