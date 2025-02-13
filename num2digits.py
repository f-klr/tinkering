#!/usr/bin/env python3.13

from functools import partial, cache
from typing import Callable, List, Any
import string

class Converter:

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
        return [ int(d, self.base) if d in string.digits else d \
            for d in Converter.lookup(self.base)(n) ]

    def __init__(self: object, base: int) -> object:
        if not base in range(2, 36):
            raise ValueError("Err ! actually, a 'base' must be between 2 and 36")
        self.base = base

    def __call__(self: object, n: int) -> List[Any]:
        return self.as_list(n)


C16 = Converter(16)
C12 = Converter(12)

as_binary = lambda n: Converter(2).as_list(n)
as_hex = lambda n: C16(n)
as_base12 = lambda n: C12.as_list(n)

print(as_binary(1984))              # an "Orwellian year" :)
print(as_hex(1_234_567))
print(as_base12(1000))              # an unusual base, to check things out, a bit ... :!
