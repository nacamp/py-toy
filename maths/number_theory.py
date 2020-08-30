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

##### polynomial operation #####
def _calc_high_deg(irr_coef, bb):
    aa = irr_coef[:]
    r = []
    for i, c in enumerate(bb):
        if i > 0:
            aa.insert(0, 0)
        r.append([x * c for x in aa])
    r = [sum(x) for x in itertools.zip_longest(*r, fillvalue=0)]
    return r

def poly_mul(a, b, irr_coef, mod=None):
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



def poly_mul2(a, b):
    aa = a[:]
    bb = b[:]
    r = []
    for i, c in enumerate(bb):
        if i > 0:  # for j in range(i):
            aa.insert(0, 0)
        r.append([x * c for x in aa])
    return [sum(x) for x in itertools.zip_longest(*r, fillvalue=0)]

def poly_add(a, b, mod=None):
    if mod:
        return [sum(x) % mod for x in zip(a,b)]
    else:
        return [sum(x) for x in zip(a,b)]

def poly_inv(a, irr_coef, mod):
    pass


def poly_round_div(numerator, denominator, mod):
    # a//b
    quotient = []
    n = numerator[:]
    while len(n) >= len(denominator):
        diff_deg = len(n) - len(denominator)
        d = [0] * diff_deg + denominator
        c = (n[-1] * mul_inverse_mod(d[-1], mod)) % mod
        quotient.insert(0, c)
        d = [x * (-c) for x in d]
        n = [sum(x) for x in itertools.zip_longest(n, d, fillvalue=0)]
        n.pop()
    return quotient

def poly_div(a, b, mod):
    """
    a * x + b * y = gcd
    """
    s, old_s = [0], [1]
    t, old_t = [1], [0]
    r, old_r = b, a

    while sum(r) != 0:
        quotient = poly_round_div(old_r, r, mod)
        old_r, r = r, [sum(x) % mod for x in itertools.zip_longest(old_r, [x * (-1) for x in poly_mul2(quotient,r)], fillvalue=0)]
        old_s, s = s, [sum(x) % mod for x in itertools.zip_longest(old_s, [x * (-1) for x in poly_mul2(quotient,s)], fillvalue=0)]
        old_t, t = t, [sum(x) % mod for x in itertools.zip_longest(old_t, [x * (-1) for x in poly_mul2(quotient,t)], fillvalue=0)]
        while len(r) and r[-1] == 0:
            r.pop()
    # old_r[0]이 1이 아닌경우는 old_r[0]으로 나눠야 한다.
    old_s_inv = mul_inverse_mod(old_r[0], mod)
    result = [ x % 3 for x in poly_mul2(old_s, [old_s_inv])]
    return result + ([0]* (mod - len(result)))

# extension field, irreducible polynomial
def make_extension_field(irr_coef, mod):
    irr_len = len(irr_coef)
    fields = []
    fields.append([1] + [0] * (irr_len - 1))
    for i in range(mod ** irr_len - 2):
        f = fields[i][:]
        f.insert(0, 0)
        ms = f.pop(irr_len)
        if ms != 0:
            # 최상위 deg의 값이 0이 아니면 하위 deg 식으로 변환 후 식을 더한다.
            # [ms * irr_coef[0], ms * irr_coef[1], ...] + f
            new_field = []
            zip_object = zip([x * ms for x in irr_coef], f)
            for a, b in zip_object:
                new_field.append(a + b)
            fields.append([x % mod for x in new_field])
        else:
            fields.append([x % mod for x in f])
    return fields

# class FQP():
#     def __init__(self, coeffs):
#         self.coeffs = coeffs
#
#     def print(self):
#         print('print{}'.format(self.coeffs))
#
#     @classmethod
#     def one(cls):
#         return cls(2)

# print(mul_inverse_mod(1, 21888242871839275222246405745257275088696311157297823662689037894645226208583))
# print(mul_inverse_mod(2, 21888242871839275222246405745257275088696311157297823662689037894645226208583))
#print(mul_inverse_mod(25,35))
# FQP.one().print()