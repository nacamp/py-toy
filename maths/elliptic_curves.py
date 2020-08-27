import math
import sys
from number_theory import mul_inverse_mod


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


def make_a_bi(mod):
    ef = []
    for a in range(mod):
        for b in range(mod):
            ef.append(complex(a, b))
    return ef

def make_f(mod):
    ef = []
    for a in range(mod):
        ef.append(a)
    return ef

# print(make_a_bi(9))
# print('y2=x3+4')
# find_point_in_curve2([4, 0, 0, 1], 11, make_a_bi(11))

def fdouble(pt, a, mod):
    x, y = pt
    y2 = 2 * y
    if isinstance(y2, complex):
        l = (3 * x ** 2 + a) * complex(y2.real, -y2.imag) * mul_inverse_mod((y2 * complex(y2.real, -y2.imag)).real, mod)
    else:
        l = (3 * x ** 2 + a) * mul_inverse_mod(y2, mod)
    newx = l ** 2 - 2 * x
    newy = -l * newx + l * x - y
    if isinstance(newx, complex):
        newx = complex(newx.real % mod, newx.imag % mod)
    else:
        newx = newx % mod
    if isinstance(newy, complex):
        newy = complex(newy.real % mod, newy.imag % mod)
    else:
        newy = newy % mod
    return newx, newy

def fadd(p1, p2, a, mod):
    if p1 is None or p2 is None:
        return p1 if p2 is None else p2
    x1, y1 = p1
    x2, y2 = p2
    if x2 == x1 and y2 == y1:
        return fdouble(p1, a, mod)
    elif x2 == x1:
        return None
    else:
        x21 = x2 - x1
        if isinstance(x21, complex):
            #l = ((y2 - y1)*(x21.real, -x21.imag)) / (x21*(x21.real, -x21.imag))
            l = ((y2 - y1) * complex(x21.real, -x21.imag)) *  mul_inverse_mod((x21 * complex(x21.real, -x21.imag)).real, mod)
        else:
            l = (y2 - y1) * mul_inverse_mod(x21, mod)
    newx = l ** 2 - x1 - x2
    newy = -l * newx + l * x1 - y1
    # assert newy == (-l * newx + l * x2 - y2)
    if isinstance(newx, complex):
        newx = complex(newx.real % mod, newx.imag%mod)
    else:
        newx = newx % mod
    if isinstance(newy, complex):
        newy = complex(newy.real % mod, newy.imag%mod)
    else:
        newy = newy % mod
    return newx, newy


def fmultiply(pt, n, a, mod):
    if n == 0:
        return None
    elif n == 1:
        return pt
    elif not n % 2:
        return fmultiply(fdouble(pt, a, mod), n // 2, a, mod)
    else:
        return fadd(fmultiply(fdouble(pt, a, mod), int(n // 2), a, mod), pt, a, mod)


class FEC():
    def __init__(self, coefficients, mod):
        self.coefficients = coefficients
        self.mod = mod

    def find_point(self, ef):
        points = []
        for x in ef:
            y = 0
            for order, c in enumerate(self.coefficients):
                y = y + c * x ** order
            points += self.find_sqrt_y(x, complex(y.real % self.mod, y.imag % self.mod), ef)
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
            #ex) 3x^3+x^2+x 라면
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
                    x_y2_points.append( (x_exp, y2_exp))
                    for y_exp in range(len(ef)):
                        if y2_exp == (y_exp * 2) % order:
                            x_y_points.append((x_exp, y_exp))
        # for x_y2_pt in x_y2_points:
        #     for y_exp in range(len(ef)):
        #         if x_y2_pt[1] == (y_exp * 2) % order:
        #             x_y_points.append((x_y2_pt[0], y_exp))
        return x_y_points

    def find_sqrt_y(self, x, y, ef):
        points = []
        for sqrt_y in ef:
            c = sqrt_y ** 2
            if c.real % self.mod == y.real and c.imag % self.mod == y.imag:
                points.append((x, sqrt_y))
            # if sqrt_y ** 2 % mod == y:
            #     print(x, sqrt_y)
        return points

    def fmultiply(self, pt, n):
        return fmultiply(pt, n, a=self.coefficients[1], mod=self.mod)

    def fadd(self, pt1, pt2):
        return fadd(pt1, pt2, a=self.coefficients[1], mod=self.mod)

# ec = FEC([4, 0, 0, 1], 11)
# ec.find_point(make_a_bi(11))
# #[(0j, (2+0j)), (0j, (9+0j)), (2j, (4+10j)), (2j, (7+1j)), (4j, (3+4j)), (4j, (8+7j)), (7j, (3+7j)), (7j, (8+4j)), (9j, (4+1j)), (9j, (7+10j)), ((1+0j), (4+0j)), ((1+0j), (7+0j)), ((1+2j), (3+7j)), ((1+2j), (8+4j)), ((1+3j), (3+8j)), ((1+3j), (8+3j)), ((1+5j), 2j), ((1+5j), 9j), ((1+6j), 2j), ((1+6j), 9j), ((1+8j), (3+3j)), ((1+8j), (8+8j)), ((1+9j), (3+4j)), ((1+9j), (8+7j)), ((2+0j), (1+0j)), ((2+0j), (10+0j)), ((2+1j), 4j), ((2+1j), 7j), ((2+2j), (2+4j)), ((2+2j), (9+7j)), ((2+5j), (3+2j)), ((2+5j), (8+9j)), ((2+6j), (3+9j)), ((2+6j), (8+2j)), ((2+9j), (2+7j)), ((2+9j), (9+4j)), ((2+10j), 4j), ((2+10j), 7j), ((3+0j), (3+0j)), ((3+0j), (8+0j)), ((3+1j), (3+8j)), ((3+1j), (8+3j)), ((3+3j), (3+9j)), ((3+3j), (8+2j)), ((3+4j), 5j), ((3+4j), 6j), ((3+7j), 5j), ((3+7j), 6j), ((3+8j), (3+2j)), ((3+8j), (8+9j)), ((3+10j), (3+3j)), ((3+10j), (8+8j)), ((4+0j), 3j), ((4+0j), 8j), ((4+2j), (3+0j)), ((4+2j), (8+0j)), ((4+4j), (1+9j)), ((4+4j), (10+2j)), ((4+5j), (2+4j)), ((4+5j), (9+7j)), ((4+6j), (2+7j)), ((4+6j), (9+4j)), ((4+7j), (1+2j)), ((4+7j), (10+9j)), ((4+9j), (3+0j)), ((4+9j), (8+0j)), ((5+0j), 5j), ((5+0j), 6j), ((5+1j), (4+1j)), ((5+1j), (7+10j)), ((5+3j), (4+0j)), ((5+3j), (7+0j)), ((5+4j), (2+4j)), ((5+4j), (9+7j)), ((5+5j), (1+4j)), ((5+5j), (10+7j)), ((5+6j), (1+7j)), ((5+6j), (10+4j)), ((5+7j), (2+7j)), ((5+7j), (9+4j)), ((5+8j), (4+0j)), ((5+8j), (7+0j)), ((5+10j), (4+10j)), ((5+10j), (7+1j)), ((6+0j), 0j), ((6+1j), (4+1j)), ((6+1j), (7+10j)), ((6+2j), (3+9j)), ((6+2j), (8+2j)), ((6+3j), (5+0j)), ((6+3j), (6+0j)), ((6+8j), (5+0j)), ((6+8j), (6+0j)), ((6+9j), (3+2j)), ((6+9j), (8+9j)), ((6+10j), (4+10j)), ((6+10j), (7+1j)), ((7+0j), 4j), ((7+0j), 7j), ((7+1j), (1+7j)), ((7+1j), (10+4j)), ((7+2j), 1j), ((7+2j), 10j), ((7+4j), (3+3j)), ((7+4j), (8+8j)), ((7+7j), (3+8j)), ((7+7j), (8+3j)), ((7+9j), 1j), ((7+9j), 10j), ((7+10j), (1+4j)), ((7+10j), (10+7j)), ((8+0j), 1j), ((8+0j), 10j), ((8+1j), (1+2j)), ((8+1j), (10+9j)), ((8+4j), 0j), ((8+7j), 0j), ((8+10j), (1+9j)), ((8+10j), (10+2j)), ((9+0j), 2j), ((9+0j), 9j), ((9+1j), 3j), ((9+1j), 8j), ((9+10j), 3j), ((9+10j), 8j), ((10+0j), (5+0j)), ((10+0j), (6+0j)), ((10+2j), (3+7j)), ((10+2j), (8+4j)), ((10+3j), (1+2j)), ((10+3j), (10+9j)), ((10+4j), (1+7j)), ((10+4j), (10+4j)), ((10+5j), (1+0j)), ((10+5j), (10+0j)), ((10+6j), (1+0j)), ((10+6j), (10+0j)), ((10+7j), (1+4j)), ((10+7j), (10+7j)), ((10+8j), (1+9j)), ((10+8j), (10+2j)), ((10+9j), (3+4j)), ((10+9j), (8+7j))]
# # order3인 cyclic (8,1j), (8,10j), none
# print(fmultiply((8,1j), 1, a=0, mod=11))
# print(fmultiply((8,1j), 2, a=0, mod=11))
# print(fmultiply((8,1j), 3, a=0, mod=11))
# print('----')
# print(fmultiply((8,10j), 1, a=0, mod=11))
# print(fmultiply((8,10j), 2, a=0, mod=11))
# print(fmultiply((8,10j), 3, a=0, mod=11))
# print('----')
# # order3인 cyclic (0,2), (0,9), none
# print(fmultiply((0, 2), 1, a=0, mod=11))
# print(fmultiply((0, 2), 2, a=0, mod=11))
# print(fmultiply((0, 2), 3, a=0, mod=11))
# print('----')
# print(fmultiply((0, 9), 1, a=0, mod=11))
# print(fmultiply((0, 9), 2, a=0, mod=11))
# print(fmultiply((0, 9), 3, a=0, mod=11))
# print('----')
#
#
# ec = FEC([13, 0, 0, 1], 31)
# points = ec.find_point(make_f(31))
# print('points len =', len(points) +1)
# print(points)
# print('----')
# print(ec.fmultiply((1,18), 1 ))
# print(ec.fmultiply((1,18), 2 ))
# print(ec.fmultiply((1,18), 3 ))
# print(ec.fmultiply((1,18), 4 ))
# print(ec.fmultiply((1,18), 5 ))
# print('----')
# #덧셈에 닫혀있는지 확인
# #(1, 18) (12, 25) (12, 6) (1, 13) None
# print(ec.fadd((1,18), (12,25) ))
# print(ec.fadd((1, 13), (12,25) ))
# print('----')

# ec = FEC([2, 7, 0, 1], 11**3)
# points = ec.find_point(make_f(11**3))
# print('points len =', len(points) +1)
# print(points)
# print('----')

#irreducible polynomial
def make_ex_field_by_irreducible_polynomial(irr_coef, mod):
    irr_len = len(irr_coef)
    fields = []
    fields.append([1]+[0] * (irr_len-1))
    for i in range(mod**irr_len -2):
        f = fields[i][:]
        f.insert(0,0)
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
# u^3+u+4=0 =>  u^3=0u^2-u-4=0u^2+10u+7
f_11 = make_ex_field_by_irreducible_polynomial([7,10,0], 11)
print(f_11)
print(f_11[384]) #[5, 9, 1]
print(f_11[778]) # [0, 3, 4]
#u^481*3 + 7u^481 + 2
print(f_11[113]) # [0, 8, 7]
print(f_11[481]) # [4, 7, 4]
for i, x in enumerate(f_11):
    if x == [8,2,2]:
        print(i) #768
print(f_11[768])
print(1049*2 % 1330, 384*2% 1330)

#y^2=x^3+0x^2+7x+2
ec = FEC([2, 7, 0, 1], 11)
x = ec.find_point2(f_11)
print(x)

#TODO: 덧셈, 뺄샘
# print(len(x))
# # x^2+2x+2=0 =>  x^2=x+1
# make_irr_points([1,1], 3)
# # u^3+u+4=0 =>  u^3=0u^2-u-4=0u^2+10u+7
# f_11 = make_irr_points([7,10,0], 11)
# print(len(f_11))
# print(f_11[0])
# print(f_11[481])
# print(f_11[113])
# for i, x in enumerate(f_11):
#     if x == [1,5,6]:
#         print(i)
# print(f_11[87])
# print(f_11[1049])
# for i, x in enumerate(f_11):
#     if x == [8,2,2]:
#         print(i)
    # for a in range(mod):
    #     for b in range(mod):
    #         ef.append(complex(a, b))
    # return ef
# def make_u3_u_4(mod):
#     ef = []
#     for a in range(mod):
#         for b in range(mod):
#             ef.append(complex(a, b))
#     return ef

# find_point_in_curve([2, 0, 0, 1], 7)
# #E(F7) = {∞, (0, 3), (0, 4), (3, 1), (3, 6), (5, 1), (5, 6), (6, 1), (6, 6)}.
# print(multiply((5, 6), 6, a=0, mod=7))
# print(add((5, 6),(5, 6), a=0, mod=7))

# # y2 = x3+20x+20
# find_point_in_curve([20, 20, 0, 1], 103)
# print(muli_add([(26, 20),(63, 78),(59, -95),(24, -25)], a=20, mod=103))
# print(muli_add([(26, 20),(63, 78),(59, -95),(77, -84)], a=20, mod=103))
#
# #x3+8x+1 F61
# print(muli_add([(57,24),(25,37),(17,32),(42,35)], a=8, mod=61))
#
# #y2=x3-x-2
# find_point_in_curve([-2, -1, 0, 1], 163)

# print('y2=x3+4')
# find_point_in_curve([4, 0, 0, 1], 11)

# print(multiply((0, 2), 3, a=0, mod=11))
# print(multiply((10, 5), 2, a=0, mod=11))


# R = (12,35) and S = (5,66)
# lP,Q(D1) = (yR + 93xR + 85)2(yS + 93xS + 85) = 122
# Consider E/F163 : y2 = x3 − x − 2, with P = (43,154), Q = (46,38), R = (12,35) and S = (5,66) all on E.
