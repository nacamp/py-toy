import inspect
from maths.elliptic_curves import *
from maths.number_theory import *


# https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjhiuXAzbzrAhWzL6YKHQohB1oQFjAAegQIBBAB&url=http%3A%2F%2Fwww.craigcostello.com.au%2Fpairings%2FPairingsForBeginners.pdf&usg=AOvVaw1H5dLtelG00vWsvWRGxBNZ
# ParingsForBeginners.pdf
def p22():
    print(inspect.stack()[0][3], '>>>>>')
    ec = FEC([1, 1, 0, 1], 101)
    points = ec.find_point(make_f(101))
    print('points : ', points)
    print('order : ', len(points))

    def _subgroups(pt):
        pts = []
        pts.append((0, 0))
        for i in range(1, 106):
            new_pt = ec.fmultiply(pt, i)
            if new_pt is None:
                break
            pts.append(new_pt)
        return pts

    print('order 1  [105](47,12)  >>')
    pts = _subgroups(ec.fmultiply((47, 12), 105))
    print('order: ', len(pts), 'sub: ', pts)

    print('order 3  [35](47,12)  >>')
    pts = _subgroups(ec.fmultiply((47, 12), 35))
    print('order: ', len(pts), 'sub: ', pts)

    print('order 5  [21](47,12)  >>')
    pts = _subgroups(ec.fmultiply((47, 12), 21))
    print('order: ', len(pts), 'sub: ', pts)

    print('order 7  [15](47,12)  >>')
    pts = _subgroups(ec.fmultiply((47, 12), 15))
    print('order: ', len(pts), 'sub: ', pts)

    print('order 15  [7](47,12)  >>')
    pts = _subgroups(ec.fmultiply((47, 12), 7))
    print('order: ', len(pts), 'sub: ', pts)

    print('order 21  [5](47,12)  >>')
    pts = _subgroups(ec.fmultiply((47, 12), 5))
    print('order: ', len(pts), 'sub: ', pts)

    print('order 35  [3](47,12)  >>')
    pts = _subgroups(ec.fmultiply((47, 12), 3))
    print('order: ', len(pts), 'sub: ', pts)

    print('order 105  [1](47,12)  >>')
    pts = _subgroups(ec.fmultiply((47, 12), 1))
    print('order: ', len(pts), 'sub: ', pts)

def p26():
    print(inspect.stack()[0][3], '>>>>>')
    ec = FEC([3, 4, 0, 1], 67)
    points = ec.find_point(make_f(67))
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
    points = ec.find_point(make_f(101))

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
p29()

# http://matrix.etseq.urv.es/manuals/matlab/toolbox/comm/tutor33.html



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


# fmul([7, 10, 0],[3, 9, 6],[7,10,0], 11 )
# print(fmul([7, 10, 0],[3, 9, 6],[7,10,0], 11 ))
'''
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

'''


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
