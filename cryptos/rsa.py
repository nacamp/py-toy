'''
https://en.wikipedia.org/wiki/RSA_(cryptosystem)
https://en.wikipedia.org/wiki/Carmichael_function
'''
from maths.number_theory import *
import random


def carmichael_function_for_prime(p, q):
    return lcm((p - 1), (q - 1))


def make_seed(p, q):
    n = p * q
    lcm_mod = carmichael_function_for_prime(p, q)
    while True:
        e = random.randrange(lcm_mod)
        try:
            d = inv(e, lcm_mod)
            break;
        except:
            continue
    return (n, e, int(d))


def encrypt(m, e, n):
    return pow(m, e, n)


def decrypt(c, d, n):
    return pow(c, d, n)


'''
n, e, d = make_seed(61, 53)

c = encrypt(65,e,n)
print('c : ', c)

m = decrypt(c,d,n)
print('m : ', m)
'''
