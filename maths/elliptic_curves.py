import math
import sys
import itertools
from maths.number_theory import *


# 비탈릭 코드 참조
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


# Convert P => -P
def neg(pt):
    if pt is None:
        return None
    x, y = pt
    return (x, -y)


def multiply(pt, n, a, mod):
    if n == 0:
        return None
    elif n == 1:
        return pt
    elif not n % 2:
        return multiply(double(pt, a, mod), n // 2, a, mod)
    else:
        return add(multiply(double(pt, a, mod), int(n // 2), a, mod), pt, a, mod)


def muli_add(points, a, mod):
    result = points[0];
    for v in points[1:]:
        result = add(result, v, a=a, mod=mod)
    return result;


def find_sqrt_y(x, y, mod):
    for sqrt_y in range(mod):
        if sqrt_y ** 2 % mod == y:
            print(x, sqrt_y)


def find_point_in_curve(coefficients, mod):
    print('x y')
    for x in range(mod):
        y = 0
        for order, c in enumerate(coefficients):
            y = y + c * x ** order
        # if math.sqrt(y % p).is_integer():
        #     print(x, y % p, math.sqrt(y % p).is_integer())
        find_sqrt_y(x, y % mod, mod)


def find_sqrt_y2(x, y, mod, ef):
    for sqrt_y in ef:
        c = sqrt_y ** 2
        if c.real % mod == y.real and c.imag % mod == y.imag:
            print(x, sqrt_y)
        # if sqrt_y ** 2 % mod == y:
        #     print(x, sqrt_y)


def find_point_in_curve2(coefficients, mod, ef):
    print('x y')
    for x in ef:
        y = 0
        for order, c in enumerate(coefficients):
            y = y + c * x ** order
        # if math.sqrt(y % p).is_integer():
        #     print(x, y % p, math.sqrt(y % p).is_integer())
        find_sqrt_y2(x, complex(y.real % mod, y.imag % mod), mod, ef)


# print(make_a_bi(9))
# print('y2=x3+4')
# find_point_in_curve2([4, 0, 0, 1], 11, make_a_bi(11))

# def finite_double(pt, a, mod):
#     x, y = pt
#     y2 = 2 * y
#     if y2 == 0:
#         return None
#     if isinstance(y2, complex):
#         l = (3 * x ** 2 + a) * complex(y2.real, -y2.imag) * mul_inverse_mod((y2 * complex(y2.real, -y2.imag)).real, mod)
#         # 이곳에서 %를 안해주면 결과값이 다르게 나올수 있다?
#         l = complex(l.real % mod, l.imag % mod)
#     else:
#         l = (3 * x ** 2 + a) * mul_inverse_mod(y2, mod)
#     newx = l ** 2 - 2 * x
#     newy = -l * newx + l * x - y
#     if isinstance(newx, complex):
#         newx = complex(newx.real % mod, newx.imag % mod)
#     else:
#         newx = newx % mod
#     if isinstance(newy, complex):
#         newy = complex(newy.real % mod, newy.imag % mod)
#     else:
#         newy = newy % mod
#     return newx, newy

def finite_double(pt, a, mod):
    x, y = pt
    y2 = 2 * y
    if y2 == 0:
        return None
    if isinstance(y2, Cpx):
        l = (3 * x ** 2 + a) * y2.ineg() * mul_inverse_mod((y2*y2.ineg()).r, mod)
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

# def finite_add(p1, p2, a, mod):
#     if p1 is None or p2 is None:
#         return p1 if p2 is None else p2
#     x1, y1 = p1
#     x2, y2 = p2
#     if x2 == x1 and y2 == y1:
#         return finite_double(p1, a, mod)
#     elif x2 == x1:
#         return None
#     else:
#         x21 = x2 - x1
#         if isinstance(x21, complex):
#             # l = ((y2 - y1)*(x21.real, -x21.imag)) / (x21*(x21.real, -x21.imag))
#             l = ((y2 - y1) * complex(x21.real, -x21.imag)) * mul_inverse_mod((x21 * complex(x21.real, -x21.imag)).real,
#                                                                              mod)
#         else:
#             l = (y2 - y1) * mul_inverse_mod(x21, mod)
#     newx = l ** 2 - x1 - x2
#     newy = -l * newx + l * x1 - y1
#     # assert newy == (-l * newx + l * x2 - y2)
#     if isinstance(newx, complex):
#         newx = complex(newx.real % mod, newx.imag % mod)
#     else:
#         newx = newx % mod
#     if isinstance(newy, complex):
#         newy = complex(newy.real % mod, newy.imag % mod)
#     else:
#         newy = newy % mod
#     return newx, newy

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
                l = ((y2 - y1) * x21.ineg()) * mul_inverse_mod((x21 *  x21.ineg()).r, mod)
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
    s1 = field.add(field.mul(3,field.pow(x,2)),a)
    s2 = field.inv(y2)
    l = field.mul(s1, s2)
    #newx = l ** 2 - 2 * x
    newx = field.sub(field.pow(l,2), field.mul(2,x))
    #newy = -l * newx + l * x - y
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
        # 아직 미구현
        return poly_double(p1, a, field)
    elif list(x2) == list(x1):
        return None
    else:
        x21 = field.sub(x2, x1)
        l = field.mul(field.sub(y2,y1) , field.inv(x21) )
    newx = field.sub(field.mul(l,l) , field.add(x1, x2) )
    newy = field.sub (field.add(field.mul(field.neg(l) ,newx) , field.mul(l,x1 )) , y1)
    return newx, newy

def poly_neg(pt):
    if pt is None:
        return None
    return (pt[0], [x*(-1) for x in pt[1]])

def poly_multiply(pt, n, a, field):
    if n == 0:
        return None
    elif n == 1:
        return pt
    elif not n % 2:
        return poly_multiply(poly_double(pt, a, field), n // 2, a, field)
    else:
        return poly_add(poly_multiply(poly_double(pt, a, field), int(n // 2), a, field), pt, a, field)

#Finite Elliptic Curve
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
                y = self.poly_field.add( y, self.poly_field.mul(c,self.poly_field.pow(pt[0], order)) )
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
            for order, c in enumerate(self.coefficients):
                y = y + c * x ** order
            # if isinstance(y, Cpx):
            #     points += self.find_sqrt_y(x, y % self.mod, ef)
            # else:
            points += self.find_sqrt_y(x, y % self.mod, ef)
        points.insert(0, (0, 0))
        return points

    '''
    ef: extend field
    '''

    def find_point2(self, ef):
        x_y2_points = []
        x_y_points = []
        order = self.mod ** len(ef[0]) - 1
        for x_exp in range(len(ef)):
            ef_idx = []
            for deg in range(len(self.coefficients)):
                ef_idx.append(x_exp * deg % order)
            # ex) 3x^3+x^2+x 라면
            # 3ef[3], ef[2], ef[1] 3개의 식을 생성하고
            fns = []
            for deg, c in enumerate(self.coefficients):
                fns.append([x * c for x in ef[ef_idx[deg]]])
            fn = [0] * len(ef[0])
            # 각 deg 별로 더한다
            # ef[3][0] + ef[2][0] + ef[1][0]
            for f in fns:
                for k in range(len(ef[0])):
                    fn[k] += f[k]

            for y2_exp, coef in enumerate(ef):
                c = [x % self.mod for x in fn]
                if coef == c:
                    x_y2_points.append((x_exp, y2_exp))
                    for y_exp in range(len(ef)):
                        if y2_exp == (y_exp * 2) % order:
                            x_y_points.append((x_exp, y_exp))
        # for x_y2_pt in x_y2_points:
        #     for y_exp in range(len(ef)):
        #         if x_y2_pt[1] == (y_exp * 2) % order:
        #             x_y_points.append((x_y2_pt[0], y_exp))
        return x_y_points

    # def find_sqrt_y(self, x, y, ef):
    #     points = []
    #     for sqrt_y in ef:
    #         c = sqrt_y ** 2
    #         if c.real % self.mod == y.real and c.imag % self.mod == y.imag:
    #             points.append((x, sqrt_y))
    #         # if sqrt_y ** 2 % mod == y:
    #         #     print(x, sqrt_y)
    #     return points
    def find_sqrt_y(self, x, y, ef):
        points = []
        for sqrt_y in ef:
            c = sqrt_y ** 2
            # if isinstance(y, Cpx):
            #     c % self.mod
            #     if c.real % self.mod == y.real and c.imag % self.mod == y.imag:
            #         points.append((x, sqrt_y))
            # else:
            #     pass
            # c % mod
            if c % self.mod == y:
                points.append((x, sqrt_y))
            # if sqrt_y ** 2 % mod == y:
            #     print(x, sqrt_y)
        return points

    # def multiply(self, pt, n):
    #     if pt is None:
    #         return None;
    #     if isinstance(pt[0], list) or isinstance(pt[0], tuple):
    #         return poly_multiply(pt, n, a=self.coefficients[1], field=self.poly_field)
    #     else:
    #         return finite_multiply(pt, n, a=self.coefficients[1], mod=self.mod)

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

    #Frobenius endomorphism π
    def frobEndPi(self, pt, i=1):
        if isinstance(pt[0], list) or isinstance(pt[0], tuple):
            x = self.poly_field.pow(pt[0], self.mod ** i)
            y = self.poly_field.pow(pt[1], self.mod ** i)
            return (x,y)
        else:
            if isinstance(pt[0], complex):
                x = complex(1)
                for i in range(self.mod ** i):
                    x = x * pt[0]
                    x = complex(x.real % self.mod, x.imag % self.mod)
                # overflow ...
                # x = pow(pt[0], self.mod ** i)
                # x = complex(x.real % self.mod, x.imag % self.mod)
            else:
                x = pow(pt[0], self.mod ** i, self.mod)
            if isinstance(pt[1], complex):
                y = complex(1)
                for i in range(self.mod ** i):
                    y = y * pt[1]
                    y = complex(y.real % self.mod, y.imag % self.mod)
                # y = pow(pt[1], self.mod ** i)
                # y = complex(y.real % self.mod, y.imag % self.mod)
            else:
                y = pow(pt[1], self.mod ** i, self.mod)
            return (x,y)

    #  trace map
    def Tr(self, pt):
        new_points = list(pt[:])
        if isinstance(pt[0], list) or isinstance(pt[0], tuple):
            for i in range(1, len(pt[0]), 1):
                new_points = self.add(new_points, self.frobEndPi(pt,i))
            return new_points
        else:
            pass
'''
itertools.zip_longest(*iterables, fillvalue=None)
출처: https://excelsior-cjh.tistory.com/100 [EXCELSIOR]
'''


'''
def Tr2(pt,ec):
    new_points = list(pt[:])
    # new_points = [(0,0,0), (0,0,0)]
    for i in range(1, len(pt[0]), 1):
        x = ec.poly_field.pow(pt[0], ec.mod**i)
        y = ec.poly_field.pow(pt[1], ec.mod**i)
        # print(x,y)
        # print(new_points)
        new_points = ec.add(new_points, [x,y])
    return new_points
def Tr2(pt,ec):
    new_points = list(pt[:])
    # new_points = [(0,0,0), (0,0,0)]
    for i in range(1, len(pt[0]), 1):
        x = ec.poly_field.pow(pt[0], ec.mod**i)
        y = ec.poly_field.pow(pt[1], ec.mod**i)
        # print(x,y)
        # print(new_points)
        new_points = ec.add(new_points, [x,y])
    return new_points
If E is defined over Fq, then the Frobenius endomorphism π is defined as
π : E → E, (x,y) 􏰀→ (xq,yq).

'''