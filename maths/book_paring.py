import inspect
from maths.elliptic_curves import *
from maths.number_theory import *


# https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjhiuXAzbzrAhWzL6YKHQohB1oQFjAAegQIBBAB&url=http%3A%2F%2Fwww.craigcostello.com.au%2Fpairings%2FPairingsForBeginners.pdf&usg=AOvVaw1H5dLtelG00vWsvWRGxBNZ
# ParingsForBeginners.pdf
def p22():
    print(inspect.stack()[0][3], '>>>>>')
    ec = FEC([1, 1, 0, 1], 101)
    points = ec.find_point(make_field(101))
    print('points : ', points)
    print('order : ', len(points))

    def _subgroups(pt):
        pts = []
        pts.append((0, 0))
        for i in range(1, 106):
            new_pt = ec.multiply(pt, i)
            if new_pt is None:
                break
            pts.append(new_pt)
        return pts

    print('order 1  [105](47,12)  >>')
    pts = _subgroups(ec.multiply((47, 12), 105))
    print('order: ', len(pts), 'sub: ', pts)
    print('------------')
    print('order 3  [35](47,12)  >>')
    pts = _subgroups(ec.multiply((47, 12), 35))
    print('order: ', len(pts), 'sub: ', pts)
    print('------------')
    print('order 5  [21](47,12)  >>')
    pts = _subgroups(ec.multiply((47, 12), 21))
    print('order: ', len(pts), 'sub: ', pts)
    print('------------')
    print('order 7  [15](47,12)  >>')
    pts = _subgroups(ec.multiply((47, 12), 15))
    print('order: ', len(pts), 'sub: ', pts)
    print('------------')
    print('order 15  [7](47,12)  >>')
    pts = _subgroups(ec.multiply((47, 12), 7))
    print('order: ', len(pts), 'sub: ', pts)
    print('------------')
    print('order 21  [5](47,12)  >>')
    pts = _subgroups(ec.multiply((47, 12), 5))
    print('order: ', len(pts), 'sub: ', pts)
    print('------------')
    print('order 35  [3](47,12)  >>')
    pts = _subgroups(ec.multiply((47, 12), 3))
    print('order: ', len(pts), 'sub: ', pts)
    print('------------')
    print('order 105  [1](47,12)  >>')
    pts = _subgroups(ec.multiply((47, 12), 1))
    print('order: ', len(pts), 'sub: ', pts)

def p26():
    print(inspect.stack()[0][3], '>>>>>')
    ec = FEC([3, 4, 0, 1], 67)
    points = ec.find_point(make_field(67))
    print('points : ', points)
    print('order : ', len(points))

    print('(15^67, )', pow(15,67, 67))
    # u^2+1=0
    field = PolyField([1, 0, 1], 67)
    #((16,2)^67,)
    #print(field.pow([16,2], 67))
    #((39, 30)^ 67,)
    print(field.pow([39, 30], 67))

    # u^3+2=0
    field = PolyField([2, 0, 0,1], 67)
    #(8, 4, 15)^67
    print(field.pow([8, 4, 15], 67))
    # (8, 4, 15)^67^2
    print(field.pow([8, 4, 15], 67*67))
    # (8, 4, 15)^67^2
    # 시간이 오래걸림
    # print(field.pow([8, 4, 15], 67*67*67))

def p29():
    print(inspect.stack()[0][3], '>>>>>')
    ec = FEC([1, 1, 0, 1], 101)
    points = ec.find_point(make_field(101))

    print('r=2, y = solve_poly([4, 4, 0, 4], x) % 101')
    roots_x = []
    for x in range(101):
        y = solve_poly([4, 4, 0, 4], x) % 101
        if y == 0:
            roots_x.append(x)
    print(roots_x)
    print('r=3, y = solve_poly([100, 12, 6, 0, 3], x) % 101')
    roots_x = []
    for x in range(101):
        y = solve_poly([100, 12, 6, 0, 3], x) % 101
        if y == 0:
            roots_x.append(x)
    print(roots_x) #17, 28
    print('qr(solve_poly([1, 1, 0, 1], 17), 101) = ')
    print(qr(solve_poly([1, 1, 0, 1], 17), 101))
    print('qr(solve_poly([1, 1, 0, 1], 28), 101) = ')
    print(qr(solve_poly([1, 1, 0, 1], 28), 101))
    print('EC에서 x=17인 점이 있는지')
    for pt in points:
        if pt[0] == 17:
            print(pt)
    print('EC에서 x=28인 점이 있는지')
    for pt in points:
        if pt[0] == 28:
            print(pt)

def p37():
    print(inspect.stack()[0][3], '>>>>>')
    ec = FEC([20, 20, 0, 1], 103)
    points = ec.find_point(make_field(103))
    print('points : ', points)
    print('order : ', len(points))

    P = (26, 20)
    Q = (63, 78)
    R = (59, 95)
    S = (24, 25)
    T = (77, 84)
    U = (30, 99)
    assert ec.fadd(R, T) == U
    print(ec.fadd(ec.fadd(P, Q), ec.fadd(neg(R), neg(S))))  # (18,49)
    print(ec.fadd(ec.fadd(P, Q), ec.fadd(neg(R), neg(T))))  # None

def p38():
    print(inspect.stack()[0][3], '>>>>>')
    ec = FEC([1, 8, 0, 1], 61)
    points = ec.find_point(make_field(61))
    print('points : ', points)
    print('order : ', len(points))

    P = (57, 24)
    Q = (25, 37)
    R = (17, 32)
    S = (42, 35)
    print(ec.fadd(ec.fadd(P, Q), R))  # (42,26)
    print(ec.fadd((42,26), S))  # None

    assert solve_poly([24, 10, 33], P[0]) % 61 == P[1]
    assert solve_poly([24, 10, 33], Q[0]) % 61 == Q[1]
    assert solve_poly([24, 10, 33], R[0]) % 61 == R[1]
    assert solve_poly([24, 10, 33], S[0]) % 61 == S[1]

def p43():
    print(inspect.stack()[0][3], '>>>>>')
    ec = FEC([-2, -1, 0, 1], 163)
    points = ec.find_point(make_field(163))
    print('points : ', points)
    print('order : ', len(points))

    P = (43, 154)
    Q = (46, 38)
    R = (12, 35)
    S = (5, 66)
    # print(ec.fadd(ec.fadd(P, Q), R))  # (42,26)
    # print(ec.fadd((42,26), S))  # None

    assert solve_poly([-85, -93], P[0]) % 163 == P[1]
    assert solve_poly([-90, -127], P[0]) % 163 == P[1]
    assert solve_poly([-16, -13], Q[0]) % 163 == Q[1]

    #l_p_q(D1)
    print((solve_poly([85, 93], R[0]) + R[1])**2 * (solve_poly([85, 93], S[0]) + S[1])**1 %163)
    #l_p_p(D2)  53
    print((solve_poly([90, 127], R[0]) + R[1])**3 * inv((solve_poly([90, 127], S[0]) + S[1])**3,163) %163)
    #2l_p_p(D2) 53
    print((solve_poly([2*90, 2*127], R[0]) + 2*R[1])**3 * inv((solve_poly([2*90, 2*127], S[0]) + 2*S[1])**3,163) %163)

def p44():
    print(inspect.stack()[0][3], '>>>>>')
    ec = FEC([1, 0, 0, 1], 503)
    points = ec.find_point(make_field(503))
    print('points : ', points)
    print('order : ', len(points))

    def inv(n, p):
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

    for pt in points:
        try:
            if (20*pt[1]+9*pt[0]+179) * inv(199*pt[1]+187*pt[0]+359, 503) % 503 == 0:
                print(pt)
        except:
            print('err', pt)
    print('g:')
    for pt in points:
        if solve_poly([201, 129, 251], pt[0])*(-1) % 503 == pt[1]:
            print(pt)

def p48():
    print(inspect.stack()[0][3], '>>>>>')
    mod = 7691
    field = PolyField([1, 0, 1], mod)
    ec = FEC([1, 0, 0, 1], mod, field)

    P = [2693, 4312]
    Q = ((6145, 633), (109, 7372))
    assert ec.multiply(P, 641) == None
    assert ec.multiply(Q, 641) == None
    a = 403
    b = 135
    print('[a]P')
    print(ec.multiply(P, a))
    print('[b]Q')
    print(ec.multiply(Q, b))
    print(field.pow((5677, 6744), a))  # [7025, 3821]
    print(field.pow((5677, 6744), b))  # [5, 248]
    print(field.pow((5677, 6744), 561))  # [2731, 2719]
    # a*b%mod = 568 ?
    print(field.pow((5677, 6744), a*b%mod))  # [6363, 4914]

def p51():
    print(inspect.stack()[0][3], '>>>>>')
    ec = FEC([4, 0, 0, 1], 11)
    points = ec.find_point(make_a_bi(11))
    print(points)

    print('order3인 cyclic (8,1j), (8,10j), none')
    print(ec.multiply((8,1j), 1))
    print(ec.multiply((8,1j), 2))
    print(ec.multiply((8,1j), 3))
    print('----')
    print(ec.multiply((8,10j), 1))
    print(ec.multiply((8,10j), 2))
    print(ec.multiply((8,10j), 3))
    print('----')
    print('order3인 cyclic (0,2), (0,9), none')
    print(ec.multiply((0,2), 1))
    print(ec.multiply((0,2), 2))
    print(ec.multiply((0,2), 3))
    print('----')
    print(ec.multiply((0,9), 1))
    print(ec.multiply((0,9), 2))
    print(ec.multiply((0,9), 3))
    print('----')

def p52():
    print(inspect.stack()[0][3], '>>>>>')
    ec = FEC([13, 0, 0, 1], 31)
    points = ec.find_point(make_field(31))
    print('points len =', len(points) +1)
    print(points)

    print(ec.multiply((1,18), 1 ))
    print(ec.multiply((1,18), 2 ))
    print(ec.multiply((1,18), 3 ))
    print(ec.multiply((1,18), 4 ))
    print(ec.multiply((1,18), 5 ))
    print('----')
    #덧셈에 닫혀있는지 확인
    #(1, 18) (12, 25) (12, 6) (1, 13) None
    print(ec.add((1,18), (12,25) ))
    print(ec.add((1, 13), (12,25) ))
    print('----')

# def p53():
#     print(inspect.stack()[0][3], '>>>>>')
#     mod = 11
#     field = PolyField([4,1,0,1], mod)
#     f_11 = field.elements()
#     print(f_11[384]) #[5, 9, 1]
#     print(f_11[778]) # [0, 3, 4]
#     for i, x in enumerate(f_11):
#         if x == [1,5,6]:
#             print(i)
#     print(len(f_11))
#     print(f_11[0])
#     print(f_11[481])
#     print(f_11[113])
#     for i, x in enumerate(f_11):
#         if x == [1,5,6]:
#             print(i)
#     print(f_11[87])
#     print(f_11[1049])
#     for i, x in enumerate(f_11):
#         if x == [8,2,2]:
#             print(i)
#     # ec = FEC([2, 7, 0, 1], 11, [4,1,0,1])
#     # points = ec.find_point(make_field(11**3))
#     # print('points len =', len(points) +1)
#     # print(points)
#     # print('----')
#     print(1049*2 % 1330, 384*2% 1330)
p52()



# fmul([7, 10, 0],[3, 9, 6],[7,10,0], 11 )
# print(fmul([7, 10, 0],[3, 9, 6],[7,10,0], 11 ))



# print(f_11[384]) #[5, 9, 1]
# print(f_11[778]) # [0, 3, 4]
# #u^481*3 + 7u^481 + 2
# print(f_11[113]) # [0, 8, 7]
# print(f_11[481]) # [4, 7, 4]
# for i, x in enumerate(f_11):
#     if x == [8,2,2]:
#         print(i) #768
# print(f_11[768])
# print(1049*2 % 1330, 384*2% 1330)
#
# #y^2=x^3+0x^2+7x+2
# ec = FEC([2, 7, 0, 1], 11)
# x = ec.find_point2(f_11)
# print(x)

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
