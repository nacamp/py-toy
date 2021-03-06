from maths.number_theory import *


### when point is integer >>>>>
def double(pt, a, mod):
    x, y = pt
    if mod:
        l = (3 * x ** 2 + a) * mul_inverse_mod((2 * y), mod)
    else:
        l = (3 * x ** 2 + a) / (2 * y)
    newx = l ** 2 - 2 * x
    newy = -l * newx + l * x - y
    if newx >= mod or newy >= mod:
        return newx % mod, newy % mod
    else:
        return newx, newy


def add(p1, p2, a, mod):
    if p1 is None or p2 is None:
        return p1 if p2 is None else p2
    x1, y1 = p1
    x2, y2 = p2
    if x2 == x1 and y2 == y1:
        return double(p1, a, mod)
    elif x2 == x1:
        return None
    else:
        if mod:
            l = (y2 - y1) * mul_inverse_mod((x2 - x1), mod)
        else:
            l = (y2 - y1) / (x2 - x1)

    newx = l ** 2 - x1 - x2
    newy = -l * newx + l * x1 - y1
    # assert newy == (-l * newx + l * x2 - y2)
    if newx >= mod or newy >= mod:
        return (newx % mod, newy % mod)
    else:
        return (newx, newy)


def multiply(pt, n, a, mod):
    if n == 0:
        return None
    elif n == 1:
        return pt
    elif not n % 2:
        return multiply(double(pt, a, mod), n // 2, a, mod)
    else:
        return add(multiply(double(pt, a, mod), int(n // 2), a, mod), pt, a, mod)


# Convert P => -P
def neg(pt):
    if pt is None:
        return None
    x, y = pt
    return (x, -y)


### when point is integer <<<<<

def finite_slope(p1, p2, a, mod):
    if p1 is None or p2 is None:
        return p1 if p2 is None else p2
    x1, y1 = p1
    x2, y2 = p2
    if x2 == x1 and y2 == y1:
        y_2 = 2 * y1
        if y_2 == 0:
            return None
        if isinstance(y_2, Cpx):
            l = (3 * x1 ** 2 + a) * y_2.ineg() * mul_inverse_mod((y_2 * y_2.ineg()).r, mod)
            # 이곳에서 %를 안해주면 결과값이 다르게 나올수 있다?
            l = l % mod
            # l = (3 * x ** 2 + a) * complex(y2.real, -y2.imag) * mul_inverse_mod((y2 * complex(y2.real, -y2.imag)).real, mod)
            # 이곳에서 %를 안해주면 결과값이 다르게 나올수 있다?
            # l = complex(l.real % mod, l.imag % mod)
        else:
            l = (3 * x1 ** 2 + a) * mul_inverse_mod(y_2, mod)
        return l % mod
    elif x2 == x1:
        return None
    else:
        x_21 = x2 - x1
        try:
            if isinstance(x_21, Cpx):
                # l = ((y2 - y1)*(x21.real, -x21.imag)) / (x21*(x21.real, -x21.imag))
                l = ((y2 - y1) * x_21.ineg()) * mul_inverse_mod((x_21 * x_21.ineg()).r, mod)
            else:
                l = (y2 - y1) * mul_inverse_mod(x_21, mod)
            return l % mod
        except (ValueError, ZeroDivisionError):
            return None


def finite_double(pt, a, mod):
    x, y = pt
    y2 = 2 * y
    if y2 == 0:
        return None
    if isinstance(y2, Cpx):
        l = (3 * x ** 2 + a) * y2.ineg() * mul_inverse_mod((y2 * y2.ineg()).r, mod)
        # 이곳에서 %를 안해주면 결과값이 다르게 나올수 있다?
        l = l % mod
        # l = (3 * x ** 2 + a) * complex(y2.real, -y2.imag) * mul_inverse_mod((y2 * complex(y2.real, -y2.imag)).real, mod)
        # 이곳에서 %를 안해주면 결과값이 다르게 나올수 있다?
        # l = complex(l.real % mod, l.imag % mod)
    else:
        l = (3 * x ** 2 + a) * mul_inverse_mod(y2, mod)
    newx = l ** 2 - 2 * x
    newy = -l * newx + l * x - y
    return newx % mod, newy % mod

def finite_add(p1, p2, a, mod):
    if p1 is None or p2 is None:
        return p1 if p2 is None else p2
    x1, y1 = p1
    x2, y2 = p2
    if x2 == x1 and y2 == y1:
        return finite_double(p1, a, mod)
    elif x2 == x1:
        return None
    else:
        x21 = x2 - x1
        try:
            if isinstance(x21, Cpx):
                # l = ((y2 - y1)*(x21.real, -x21.imag)) / (x21*(x21.real, -x21.imag))
                l = ((y2 - y1) * x21.ineg()) * mul_inverse_mod((x21 * x21.ineg()).r, mod)
            else:
                l = (y2 - y1) * mul_inverse_mod(x21, mod)
        except (ValueError, ZeroDivisionError):
            return None
    newx = l ** 2 - x1 - x2
    newy = -l * newx + l * x1 - y1
    return newx % mod, newy % mod


def finite_neg(pt):
    if pt is None:
        return None
    x, y = pt
    return (x, -y)


def finite_multiply(pt, n, a, mod):
    if n == 0:
        return None
    elif n == 1:
        return pt
    elif not n % 2:
        return finite_multiply(finite_double(pt, a, mod), n // 2, a, mod)
    else:
        return finite_add(finite_multiply(finite_double(pt, a, mod), int(n // 2), a, mod), pt, a, mod)


def poly_double(pt, a, field):
    x, y = pt
    # y2 = 2 * y
    y2 = [x * 2 for x in y]
    # l = (3 * x ** 2 + a) * field.inv(y2)
    # l = (3 * x ** 2 + a) * mul_inverse_mod(y2, mod)
    #      s1                s2
    s1 = field.add(field.mul(3, field.pow(x, 2)), a)
    s2 = field.inv(y2)
    l = field.mul(s1, s2)
    # newx = l ** 2 - 2 * x
    newx = field.sub(field.pow(l, 2), field.mul(2, x))
    # newy = -l * newx + l * x - y
    #        s1             s2
    s1 = field.mul(field.neg(l), newx)
    s2 = field.sub(field.mul(l, x), y)
    newy = field.add(s1, s2)
    return newx, newy


def poly_add(p1, p2, a, field):
    if p1 is None or p2 is None:
        return p1 if p2 is None else p2
    x1, y1 = p1
    x2, y2 = p2
    if list(x2) == list(x1) and list(y2) == list(y1):
        return poly_double(p1, a, field)
    elif list(x2) == list(x1):
        return None
    else:
        x21 = field.sub(x2, x1)
        l = field.mul(field.sub(y2, y1), field.inv(x21))
    newx = field.sub(field.mul(l, l), field.add(x1, x2))
    newy = field.sub(field.add(field.mul(field.neg(l), newx), field.mul(l, x1)), y1)
    return newx, newy


def poly_neg(pt):
    if pt is None:
        return None
    return (pt[0], [x * (-1) for x in pt[1]])


def poly_multiply(pt, n, a, field):
    if n == 0:
        return None
    elif n == 1:
        return pt
    elif not n % 2:
        return poly_multiply(poly_double(pt, a, field), n // 2, a, field)
    else:
        return poly_add(poly_multiply(poly_double(pt, a, field), int(n // 2), a, field), pt, a, field)


# Finite Elliptic Curve
class FEC():
    def __init__(self, coefficients, mod, poly_field=None):
        self.coefficients = coefficients
        self.mod = mod
        if poly_field:
            self.poly_field = poly_field

    def contain(self, pt):
        if isinstance(pt[0], int):
            y = 0
            for order, c in enumerate(self.coefficients):
                y = y + c * pt[0] ** order
            return y % self.mod == pt[1] ** 2 % self.mod
        elif isinstance(pt[0], Cpx):
            y = 0
            for order, c in enumerate(self.coefficients):
                y = y + c * pt[0] ** order
            return y % self.mod == pt[1] ** 2 % self.mod
        else:
            y = 0
            for order, c in enumerate(self.coefficients):
                y = self.poly_field.add(y, self.poly_field.mul(c, self.poly_field.pow(pt[0], order)))
        return y == self.poly_field.pow(pt[1], 2)

    # def find_point(self, ef):
    #     points = []
    #     for x in ef:
    #         y = 0
    #         for order, c in enumerate(self.coefficients):
    #             y = y + c * x ** order
    #         points += self.find_sqrt_y(x, complex(y.real % self.mod, y.imag % self.mod), ef)
    #     points.insert(0, (0, 0))
    #     return points
    def find_point(self, ef):
        points = []
        for x in ef:
            y = 0
            for deg, c in enumerate(self.coefficients):
                y = y + c * x ** deg
            # if isinstance(y, Cpx):
            #     points += self.find_sqrt_y(x, y % self.mod, ef)
            # else:
            points += self.find_sqrt_y(x, y % self.mod, ef)
        points.insert(0, (0, 0))
        return points

    def find_sqrt_y(self, x, y, ef):
        points = []
        for sqrt_y in ef:
            c = sqrt_y ** 2
            if c % self.mod == y:
                points.append((x, sqrt_y))
        return points

    def multiply(self, pt, n):
        if pt is None:
            return None;
        if isinstance(pt[0], int) or isinstance(pt[0], Cpx):
            return finite_multiply(pt, n, a=self.coefficients[1], mod=self.mod)
        else:
            return poly_multiply(pt, n, a=self.coefficients[1], field=self.poly_field)

    def add(self, pt1, pt2):
        if pt1 is None or pt2 is None:
            return pt1 if pt2 is None else pt2
        if isinstance(pt1[0], list) or isinstance(pt1[0], tuple):
            return poly_add(pt1, pt2, a=self.coefficients[1], field=self.poly_field)
        else:
            return finite_add(pt1, pt2, a=self.coefficients[1], mod=self.mod)

    def neg(self, pt1):
        if isinstance(pt1[0], list) or isinstance(pt1[0], tuple):
            return poly_neg(pt1)
        else:
            return finite_neg(pt1)

    # Frobenius endomorphism π
    def frob_end_pi(self, pt, i=1):
        if isinstance(pt[0], list) or isinstance(pt[0], tuple):
            x = self.poly_field.pow(pt[0], self.mod ** i)
            y = self.poly_field.pow(pt[1], self.mod ** i)
            return (x, y)
        else:
            if isinstance(pt[0], Cpx):
                x = Cpx(r=1)
                for _ in range(self.mod ** i):
                    x = x * pt[0]
                    x = x % self.mod
                # overflow ...
                # x = pow(pt[0], self.mod ** i)
                # x = complex(x.real % self.mod, x.imag % self.mod)
            else:
                x = pow(pt[0], self.mod ** i, self.mod)
            if isinstance(pt[1], Cpx):
                y = Cpx(r=1)
                for _ in range(self.mod ** i):
                    y = y * pt[1]
                    y = y % self.mod
                # y = pow(pt[1], self.mod ** i)
                # y = complex(y.real % self.mod, y.imag % self.mod)
            else:
                y = pow(pt[1], self.mod ** i, self.mod)
            return (x, y)

    #  trace map
    def Tr(self, pt):
        new_points = list(pt[:])
        if isinstance(pt[0], list) or isinstance(pt[0], tuple):
            for i in range(1, len(pt[0]), 1):
                new_points = self.add(new_points, self.frob_end_pi(pt, i))
            return new_points
        else:
            return self.frob_end_pi(pt, 1)


def miller(P, Q, r, ec):
    if isinstance(Q[0], tuple) or isinstance(Q[0], list):
        return _poly_miller(P, Q, r, ec)
    return _finite_miller(P, Q, r, ec)


def _poly_miller(P, Q, r, ec):
    T = P
    f = 1
    for i in range(len(r) - 2, -1, -1):
        a = finite_slope(T, T, ec.coefficients[1], ec.mod)
        # y = ax+b, y-ax-b=0  y-ax = b
        b = T[1] - a * T[0]
        field = ec.poly_field
        l_rr = field.sub(field.sub(Q[1], field.mul(a, Q[0])), b)
        v_2r = field.sub(Q[0], T[0])
        print('y+{}x+{}'.format((-a) % ec.mod, (-b) % ec.mod))
        print('x+{}'.format((-T[0]) % ec.mod))

        if isinstance(f, int):
            f = [f]
        f = field.mul(field.mul(field.mul(f, f), l_rr), field.inv(v_2r))
        T = ec.add(T, T)
        print('T:', T)

        if r[i] == 1:
            a = finite_slope(T, P, ec.coefficients[1], ec.mod)
            if a == None:
                pass
                # print( field.mul(f, field.sub(Q[0], T[0])) )
                # v_2r = Q[0] - T[0]
                # f = f * v_2r
            else:
                # y = ax+b, y-ax-b=0  y-ax = b
                b = T[1] - a * T[0]
                l_tp = field.sub(field.sub(Q[1], field.mul(a, Q[0])), b)
                v_tp = field.sub(Q[0], T[0])
                f = field.mul(field.mul(f, l_tp), field.inv(v_tp))
                T = ec.add(T, P)
    return f


def _finite_miller(P, Q, r, ec):
    T = P
    f = 1
    for i in range(len(r) - 2, -1, -1):
        a = finite_slope(T, T, ec.coefficients[1], ec.mod)
        # y = ax+b, y-ax-b=0  y-ax = b
        b = T[1] - a * T[0]
        l_tt = Q[1] - a * Q[0] - b
        v_2t = Q[0] - T[0]
        f = f * f * l_tt * v_2t.ineg() * inv((v_2t * v_2t.ineg()).r, ec.mod)
        T = ec.add(T, T)

        if r[i] == 1:
            a = finite_slope(T, P, ec.coefficients[1], ec.mod)
            if a == None:
                pass
                # v_2r = Q[0] - T[0]
                # f = f * v_2r
            else:
                # y = ax+b, y-ax-b=0  y-ax = b
                b = T[1] - a * T[0]
                l_tp = Q[1] - a * Q[0] - b
                v_tp = Q[0] - T[0]
                f = f * l_tp * v_tp.ineg() * inv((v_tp * v_tp.ineg()).r, ec.mod)
                T = ec.add(T, P)

    return f % ec.mod

'''
itertools.zip_longest(*iterables, fillvalue=None)
출처: https://excelsior-cjh.tistory.com/100 [EXCELSIOR]
'''
