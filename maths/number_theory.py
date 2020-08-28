import itertools
def xgcd(a, b):
    """
    a * x + b * y = gcd
    """
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = b, a

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    return old_r, old_s, old_t


def mul_inverse_mod(n, p):
    if n == 0:
        raise ZeroDivisionError('division by zero')
    gcd, x, y = xgcd(n, p)
    assert (n * x + p * y) % p == gcd
    # (n * x) % p == 1.

    if gcd != 1:
        # Either n is 0, or p is not a prime number.
        raise ValueError(
            '{} has no multiplicative inverse '
            'modulo {}'.format(n, p))
    else:
        return x % p

def _calc_high_deg(irr_coef, bb):
    aa = irr_coef[:]
    r = []
    for i, c in enumerate(bb):
        if i > 0:
            aa.insert(0, 0)
        r.append([x * c for x in aa])
    r = [sum(x) for x in itertools.zip_longest(*r, fillvalue=0)]
    # print(r)
    return r

def poly_mul(a, b, irr_coef, mod):
    low_coefs = []
    irr_len = len(irr_coef)

    # 하위 deg실행
    aa = a[:]
    bb = b[:]
    r = []
    for i, c in enumerate(bb):
        if i > 0:  # for j in range(i):
            aa.insert(0, 0)
        r.append([x * c for x in aa])
    # print(r)
    r = [sum(x) for x in itertools.zip_longest(*r, fillvalue=0)]
    low_coefs.append(r[0:irr_len])

    # 초과 deg실행
    while len(r) > irr_len:
        # print('xxxx')
        r = _calc_high_deg(irr_coef, r[irr_len:])
        low_coefs.append(r[0:irr_len])
    if mod:
        return [sum(x) % mod for x in itertools.zip_longest(*low_coefs, fillvalue=0)]
    else:
        return [sum(x) for x in itertools.zip_longest(*low_coefs, fillvalue=0)]



# r = fmul([7, 10, 0],[3, 9, 6],[7,10,0], 11 )
#r = poly_mul([1, 1, 1], [2, 2, 2], [7, 10, 1], 5)


class FQP():
    def __init__(self, coeffs):
        self.coeffs = coeffs

    def print(self):
        print('print{}'.format(self.coeffs))

    @classmethod
    def one(cls):
        return cls(2)

# print(mul_inverse_mod(1, 21888242871839275222246405745257275088696311157297823662689037894645226208583))
# print(mul_inverse_mod(2, 21888242871839275222246405745257275088696311157297823662689037894645226208583))
#print(mul_inverse_mod(25,35))
# FQP.one().print()