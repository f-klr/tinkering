#!/usr/bin/python

DEFAULT_DEC_DIGITS = '0123456789'
DEFAULT_BIN_DIGITS = '01'

def stats(n, digits=DEFAULT_DEC_DIGITS):
    s = dict(zip(map(int,digits), [0] * len(digits)))
    for d in str(n):
        if not(d in digits):
            raise ValueError('"{:s}" is not a valid digit!'.format(d))
        s[int(d)] = s[int(d)] + 1
    return s

if __name__ == '__main__':
    b = lambda n: bin(n)[2:]                # "binary" number -
    s = stats(b(0xdeadbeef), DEFAULT_BIN_DIGITS)
    print(s)
