import itertools
import math

def lcm(a, b):
    return a * b / math.gcd(a, b)

def int_divisor(a):
    results = []
    for i in range(2, a + 1):
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
    # assert (n * x + p * y) % p == gcd
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
    @staticmethod
    def neg(a):
        return [x * (-1) for x in a]

    @staticmethod
    def printPoint(a):
        for i, c in enumerate( reversed(a[0])):
            if i == len(a[0])-1 :
                print('{}'.format(c, len(a[0])-i-1), end='')
            else:
                print('{}u^{} + '.format(c, len(a[0]) - i - 1), end='')
        print(' , ', end='')
        for i, c in enumerate( reversed(a[1])):
            if i == len(a[1])-1 :
                print('{}'.format(c, len(a[1])-i-1), end='')
            else:
                print('{}u^{} + '.format(c, len(a[1]) - i - 1), end='')
        print('')

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

    def _mul_coef(self, a, b):
        aa = list(a[:])
        bb = list(b[:])
        while len(aa) > 0 and aa[-1] == 0:
            aa.pop()
        while len(bb) > 0 and bb[-1] == 0:
            bb.pop()
        r = [0] * (len(aa) + len(bb) - 1)
        for i, c in enumerate(bb):
            for j in range(len(aa)):
                r[i + j] += c * aa[j]
        return r

    def _mul_v2(self, a, b):
        irr_len = len(self.irr_coef)
        over_coef = self._mul_coef(a, b)
        coef = over_coef[0:irr_len]
        l = len(over_coef)
        while l > irr_len:
            over_coef = self._mul_coef(self.irr_coef, over_coef[irr_len:])
            l = len(over_coef)
            coef = [sum(x) for x in itertools.zip_longest(over_coef[0:irr_len],coef, fillvalue=0) ]
        return ([x % self.mod for x in coef])

    def mul(self, a, b):
        if isinstance(a, int):
            return [x * a % self.mod for x in b]
        if isinstance(b, int):
            return [x * b % self.mod for x in a]
        return self._mul_v2(a,b)

    def _mul_v1(self, a, b):
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
        # print(r)
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
        return [sum(x) % self.mod for x in itertools.zip_longest(a, b, fillvalue=0)]

    def sub(self, a, b):
        if isinstance(a, int):
            a = [a]
        if isinstance(b, int):
            b = [b]
        aa = list(a[:])
        bb = list(b[:])
        for i in range(max(len(aa), len(bb))):
            if len(aa) == i:
                aa.append(0)
            if len(bb) == i:
                bb.append(0)
            aa[i] = (aa[i] - bb[i]) % self.mod
        return aa

        # for i, c in enumerate(aa):
        #     aa[i] = (aa[i] - bb[i]) % self.mod
        # return aa

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
            old_r, r = r, [sum(x) % self.mod for x in
                           itertools.zip_longest(old_r, [x * (-1) for x in self._mul_coef(quotient, r)], fillvalue=0)]
            old_s, s = s, [sum(x) % self.mod for x in
                           itertools.zip_longest(old_s, [x * (-1) for x in self._mul_coef(quotient, s)], fillvalue=0)]
            old_t, t = t, [sum(x) % self.mod for x in
                           itertools.zip_longest(old_t, [x * (-1) for x in self._mul_coef(quotient, t)], fillvalue=0)]
            while len(r) and r[-1] == 0:
                r.pop()
        # old_r[0]이 1이 아닌경우는 old_r[0]으로 나눠야 한다.
        old_s_inv = mul_inverse_mod(old_r[0], self.mod)
        # result = [ x % 3 for x in self.poly_mul2(old_s, [old_s_inv])]
        result = [x % self.mod for x in self._mul_coef(old_s, [old_s_inv])]
        return result + ([0] * (len(self.irr_coef) - len(result)))

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
            return [1] + [0] * (len(a) - 1)
        x = a[:]
        for i in range(n - 1):
            x = self.mul(x, a)
        return (x)

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

def make_a_bi(mod, multiple=1):
    ef = []
    for a in range(mod):
        for b in range(mod):
            ef.append(Cpx(a, b, multiple))
    return ef


# Complex
class Cpx:
    def __init__(self, r=0, i=0, m=1):
        self.r = r
        self.i = i
        self.m = m

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Cpx(self.r + other.r, self.i + other.i, self.m)
        else:
            return Cpx(self.r + other, self.i, self.m)

    # def __radd__(self, other):
    #     return self + other
    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return Cpx(self.r - other.r, self.i - other.i, self.m)
        else:
            return Cpx(self.r - other, self.i, self.m)

    def __rsub__(self, other):
        if isinstance(other, self.__class__):
            return Cpx(other.r - self.r, other.i - self.i, self.m)
        else:
            return Cpx(other - self.r, (-1) * self.i, self.m)

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return Cpx(self.r * other.r - self.i * other.i * self.m,
                       self.r * other.i + self.i * other.r, self.m)
        else:
            return Cpx(self.r * other, self.i * other, self.m)

    __rmul__ = __mul__

    def __pow__(self, exp):
        if exp == 0:
            return Cpx(1, 0, self.m)
        if exp == 1:
            return Cpx(self.r, self.i, self.m)
        cur = Cpx(self.r, self.i, self.m)
        for i in range(1, exp):
            cur = cur * Cpx(self.r, self.i, self.m)
        return cur

    def __mod__(self, mod):
        return Cpx(self.r % mod, self.i % mod, self.m)

    def __neg__(self):
        return Cpx((-1) * self.r, (-1) * self.i, self.m)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.r == other.r and self.i == other.i
        else:
            return self.i == 0 and self.r == other

    def __hash__(self):
        return hash(self.__repr__())

    def __repr__(self):
        if self.i == 0:
            return repr(self.r)
        if self.r == 0:
            return repr('{}i'.format(self.i))
        m = '{}i+{}'.format(self.i, self.r)
        return repr(m)

    def ineg(self):
        return Cpx(self.r, (-1) * self.i, self.m)


# https://gist.github.com/dzhou/2632362
# https://ratsgo.github.io/data%20structure&algorithm/2017/10/07/prime/
def prime_sieve(sieveSize):
    # creating Sieve (0~n까지의 slot)
    sieve = [True] * (sieveSize + 1)
    # 0과 1은 소수가 아니므로 제외
    sieve[0] = False
    sieve[1] = False
    # 2부터 (루트 n) + 1까지의 숫자를 탐색
    for i in range(2, int(math.sqrt(sieveSize)) + 1):
        # i가 소수가 아니면 pass
        if sieve[i] == False:
            continue
        # i가 소수라면 i*i~n까지 숫자 가운데 i의 배수를
        # 소수에서 제외
        for pointer in range(i ** 2, sieveSize + 1, i):
            sieve[pointer] = False
    primes = []
    # sieve 리스트에서 True인 것이 소수이므로
    # True인 값의 인덱스를 결과로 저장
    for i in range(sieveSize + 1):
        if sieve[i] == True:
            primes.append(i)
    return primes


# 소인수분해, prime factorization
def get_prime_factors(n):
    # n 범위 내의 소수를 구한다
    primelist = prime_sieve(n)
    # 이 소수들 중 n으로 나누어 떨어지는
    # 소수를 구하고, 몇 번 나눌 수 있는지 계산
    # 예 : n = 8, factors = [(2, 3)]
    # 예 : n = 100, fcount = [(2: 2), (5: 2)]
    factors = []
    for p in primelist:
        count = 0
        while n % p == 0:
            n /= p
            count += 1
        if count > 0:
            factors.append((p, count))
    return factors


# https://en.wikipedia.org/wiki/Quadratic_residue
# https://rkm0959.tistory.com/20
# https://eli.thegreenplace.net/2009/03/07/computing-modular-square-roots-in-python
# https://gist.github.com/nakov/60d62bdf4067ea72b7832ce9f71ae079
# x^2  ~ q (mod n)
def qr(x_2, mod):
    if x_2 >= mod:
        x_2 = x_2 % mod
    results = []
    for x in range(mod):
        if x ** 2 % mod == x_2:
            results.append(x)
    return results

def modular_sqrt(a, p):

    def legendre_symbol(a, p):
        """ Compute the Legendre symbol a|p using
            Euler's criterion. p is a prime, a is
            relatively prime to p (if p divides
            a, then a|p = 0)

            Returns 1 if a has a square root modulo
            p, -1 otherwise.
        """
        ls = pow(a, (p - 1) // 2, p)
        return -1 if ls == p - 1 else ls

    """ Find a quadratic residue (mod p) of 'a'. p
        must be an odd prime.

        Solve the congruence of the form:
            x^2 = a (mod p)
        And returns x. Note that p - x is also a root.

        0 is returned is no square root exists for
        these a and p.

        The Tonelli-Shanks algorithm is used (except
        for some simple cases in which the solution
        is known from an identity). This algorithm
        runs in polynomial time (unless the
        generalized Riemann hypothesis is false).
    """
    # Simple cases
    #
    if legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return p
    elif p % 4 == 3:
        return pow(a, (p + 1) // 4, p)

    # Partition p-1 to s * 2^e for an odd s (i.e.
    # reduce all the powers of 2 from p-1)
    #
    s = p - 1
    e = 0
    while s % 2 == 0:
        s //= 2
        e += 1

    # Find some 'n' with a legendre symbol n|p = -1.
    # Shouldn't take long.
    #
    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1

    # Here be dragons!
    # Read the paper "Square roots from 1; 24, 51,
    # 10 to Dan Shanks" by Ezra Brown for more
    # information
    #

    # x is a guess of the square root that gets better
    # with each iteration.
    # b is the "fudge factor" - by how much we're off
    # with the guess. The invariant x^2 = ab (mod p)
    # is maintained throughout the loop.
    # g is used for successive powers of n to update
    # both a and b
    # r is the exponent - decreases with each update
    #
    x = pow(a, (s + 1) // 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e

    while True:
        t = b
        m = 0
        for m in range(r):
            if t == 1:
                break
            t = pow(t, 2, p)

        if m == 0:
            return x

        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m