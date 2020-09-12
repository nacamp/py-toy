import itertools

def int_divisor(a):
    results = []
    for i in range(2,a+1):
        if a % i == 0:
            results.append(i)
    return results

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

##### modular #######
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

inv = mul_inverse_mod

##### polynomial operation #####
class PolyField():
    def __init__(self, irr_coef, mod):
        self.coef = irr_coef
        self.mod = mod
        self.fields = []
        # x^3+2x+1=0  [1,2,0,1] => x^3=0x^2+1x+2, mod = 3 [2,1,0] 으로 변환
        self.irr_coef = irr_coef[:]
        self.irr_coef.pop()
        self.irr_coef = [x * (-1) % self.mod for x in self.irr_coef]

    def _calc_high_deg(self, bb):
        aa = self.irr_coef[:]
        r = []
        for i, c in enumerate(bb):
            if i > 0:
                aa.insert(0, 0)
            r.append([x * c for x in aa])
        r = [sum(x) for x in itertools.zip_longest(*r, fillvalue=0)]
        return r

    def mul(self, a, b):
        if isinstance(a, int):
            return [x * a % self.mod for x in b]
        if isinstance(b, int):
            return [x * b % self.mod for x in a]

        low_coefs = []
        irr_len = len(self.irr_coef)

        # 하위 deg실행
        aa = list(a[:])
        bb = list(b[:])
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
            r = self._calc_high_deg(r[irr_len:])
            low_coefs.append(r[0:irr_len])
        return [sum(x) % self.mod for x in itertools.zip_longest(*low_coefs, fillvalue=0)]


    def poly_mul2(self, a, b):
        aa = a[:]
        bb = b[:]
        r = []
        for i, c in enumerate(bb):
            if i > 0:  # for j in range(i):
                aa.insert(0, 0)
            r.append([x * c for x in aa])
        return [sum(x) for x in itertools.zip_longest(*r, fillvalue=0)]

    def add(self, a, b):
        if isinstance(a, int):
            a = [a]
        if isinstance(b, int):
            b = [b]
        return [sum(x) % self.mod for x in itertools.zip_longest(a,b, fillvalue=0)]

    def sub(self, a, b):
        aa = list(a[:])
        bb = list(b[:])
        for i, c in enumerate(aa):
            aa[i] = (aa[i] - bb[i]) % self.mod
        return aa

    @staticmethod
    def neg(a):
        return [x * (-1) for x in a]

    # @staticmethod
    # def neg(c, a):
    #     return [x * c for x in a]

    def poly_round_div(self, numerator, denominator):
        # a//b
        quotient = []
        n = numerator[:]
        while len(n) >= len(denominator):
            diff_deg = len(n) - len(denominator)
            d = [0] * diff_deg + denominator
            c = (n[-1] * mul_inverse_mod(d[-1], self.mod)) % self.mod
            quotient.insert(0, c)
            d = [x * (-c) for x in d]
            n = [sum(x) for x in itertools.zip_longest(n, d, fillvalue=0)]
            n.pop()
        return quotient

    '''
    #TODO: 코드 정리
    https://math.stackexchange.com/questions/124300/finding-inverse-of-polynomial-in-a-field
    '''
    def inv(self, a):
        """
        a * x + b * y = gcd
        """
        s, old_s = [0], [1]
        t, old_t = [1], [0]
        r, old_r = self.coef, a

        while sum(r) != 0:
            quotient = self.poly_round_div(old_r, r)
            old_r, r = r, [sum(x) % self.mod for x in itertools.zip_longest(old_r, [x * (-1) for x in self.poly_mul2(quotient,r)], fillvalue=0)]
            old_s, s = s, [sum(x) % self.mod for x in itertools.zip_longest(old_s, [x * (-1) for x in self.poly_mul2(quotient,s)], fillvalue=0)]
            old_t, t = t, [sum(x) % self.mod for x in itertools.zip_longest(old_t, [x * (-1) for x in self.poly_mul2(quotient,t)], fillvalue=0)]
            while len(r) and r[-1] == 0:
                r.pop()
        # old_r[0]이 1이 아닌경우는 old_r[0]으로 나눠야 한다.
        old_s_inv = mul_inverse_mod(old_r[0], self.mod)
        #result = [ x % 3 for x in self.poly_mul2(old_s, [old_s_inv])]
        result = [x % self.mod for x in self.poly_mul2(old_s, [old_s_inv])]
        return result + ([0]* (len(self.irr_coef) - len(result)))

    def elements(self):
        irr_len = len(self.irr_coef)
        if len(self.fields) == 0:
            fields = []
            fields.append([1] + [0] * (irr_len - 1))
            for i in range(self.mod ** irr_len - 2):
                f = fields[i][:]
                f.insert(0, 0)
                ms = f.pop(irr_len)
                if ms != 0:
                    # 최상위 deg의 값이 0이 아니면 하위 deg 식으로 변환 후 식을 더한다.
                    # [ms * irr_coef[0], ms * irr_coef[1], ...] + f
                    new_field = []
                    zip_object = zip([x * ms for x in self.irr_coef], f)
                    for a, b in zip_object:
                        new_field.append(a + b)
                    fields.append([x % self.mod for x in new_field])
                else:
                    fields.append([x % self.mod for x in f])
            self.fields = fields
        return self.fields
    def pow(self, a, n):
        if n == 0:
            return [1] + [0]*(len(a)-1)
        x = a[:]
        for i in range(n-1):
            x = self.mul(x, a)
        return(x)


def find_sqrt_y(x, y, mod):
    for sqrt_y in range(mod):
        if sqrt_y ** 2 % mod == y:
            print(x, sqrt_y)

def find_sqrt_y(y, mod):
    results = []
    for sqrt_y in range(mod):
        if sqrt_y ** 2 % mod == y:
            results.append(sqrt_y)
    return results

# https://en.wikipedia.org/wiki/Quadratic_residue
# x^2  ~ q (mod n)
def qr(x_2, mod):
    if x_2 >= mod:
        x_2 = x_2 % mod
    results = []
    for x in range(mod):
        if x ** 2 % mod == x_2:
            results.append(x)
    return results

def solve_poly(coef, x):
    return sum(c * x ** i for i, c in enumerate(coef))

##### make field #####
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

def make_field(mod):
    return [i for i in range(mod)]

def make_a_bi(mod):
    ef = []
    for a in range(mod):
        for b in range(mod):
            ef.append(complex(a, b))
    return ef