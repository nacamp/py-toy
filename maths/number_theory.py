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