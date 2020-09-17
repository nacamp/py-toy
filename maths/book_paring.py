import inspect
from maths.elliptic_curves import *
from maths.number_theory import *


# https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjhiuXAzbzrAhWzL6YKHQohB1oQFjAAegQIBBAB&url=http%3A%2F%2Fwww.craigcostello.com.au%2Fpairings%2FPairingsForBeginners.pdf&usg=AOvVaw1H5dLtelG00vWsvWRGxBNZ
# ParingsForBeginners.pdf

def find_cosets(rE,points,ec):
    r = []
    for pt in points[1:]:
        s = set()
        for i in rE:
            s.add(ec.add(i, pt))
        for ss in r:
            if not s.isdisjoint(ss):
                s = set()
                break;
        if len(s) > 0 :
            r.append(s)

    return r

def find_rE(r,points,ec):
    s=set()
    for pt in points[1:]:
       s.add(ec.multiply(pt, r))
    return s

def print_element_order(points,ec):
    for pt in points:
        pts = []
        for i in range(1, len(points)):
            new_pt = ec.multiply(pt, i)
            if new_pt is None:
                break
            pts.append(new_pt)
        print('{} order(r)={}, element={}'.format(pt,i, pts))

def subgroups(pt,ec, order_size):
    pts = []
    pts.append((0, 0))
    for i in range(1, order_size+1):
        new_pt = ec.multiply(pt, i)
        if new_pt is None:
            break
        pts.append(new_pt)
    return pts

def find_k(q, r):
    for k in range(1, q):
        if (q ** k - 1) % r == 0:
            return k
            # print('r=', r, ' k=', k)
            # break

def find_r_torsion(points, ec, candidate_r):
    results = []
    s = set()
    for r in candidate_r:
        for pt in points[1:]:
            sub_group = []
            for i in range(1,len(points)+1,1):
                try:
                    e = ec.multiply(pt, i)
                    if e == None and i == r:
                        # sub_group.append(pt)
                        break
                    else:
                        sub_group.append(e)
                except:
                    #print(pt, i, 'err')
                    break;
            if len(sub_group) + 1 == r:
                s.add(r)
                # print('r=', r, ':', sub_group)
                results.append({'r':r, 'e':sub_group})
    return s, results

def find_r(points, ec, candidate_r):
    results = []
    for r in candidate_r:
        sub_group = []
        for pt in points[1:]:
            for i in range(1,len(points)+1,1):
                try:
                    if ec.multiply(pt, i) == None and i == r:
                        sub_group.append(pt)
                        break
                except:
                    #print(pt, i, 'err')
                    break;
        print(sub_group)
        if len(sub_group) + 1 == r:
            print('r=', r, sub_group)
            results.append(r)
    return results

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
    P1 = (15,50)
    P2 = ((16, 2), (39, 30))
    P3 = ((8, 4, 15), (21, 30, 44))

    mod = 67
    ec = FEC([3, 4, 0, 1], mod)
    print(ec.frobEndPi(P1))

    field = PolyField([1, 0, 1], mod)
    ec = FEC([3, 4, 0, 1], mod, field)
    print(ec.frobEndPi(P2))
    print(ec.frobEndPi(P2,2)) #P2

    field = PolyField([2, 0, 0, 1], mod)
    ec = FEC([3, 4, 0, 1], mod, field)
    print(ec.frobEndPi(P3,2))
    # 시간이 오래걸림
    # print(ec.frobEndPi(P3,3)) #P3

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
    q = mod = 11
    ec = FEC([4, 0, 0, 1], q)
    points = ec.find_point(make_field(q))
    print('points : ', points)
    print('order : ', len(points))
    print('----')
    candidate_r = int_divisor(len(points))
    # 맞는것지 아직은 미지수
    rs = find_r(points,ec, candidate_r)
    r = rs[0]
    print('k=', find_k(q,r))
    print('----')
    print('orders')
    ec = FEC([4, 0, 0, 1], q)
    points = ec.find_point(make_a_bi(q))
    print('points : ', points)
    print('order : ', len(points))
    print('----')
    print('orders')
    for pt in points[1:]:
        for i in range(1,145,1):
            try:
                if ec.multiply(pt, i) == None and i == r:
                    print(pt, i)
                    break
            except:
                #print(pt, i, 'err')
                break;

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

    r = 3
    assert (pow(11,1) - 1) % r != 0
    assert (pow(11,2) - 1) % r == 0

def p52():
    print(inspect.stack()[0][3], '>>>>>')
    ec = FEC([13, 0, 0, 1], 31)
    points = ec.find_point(make_field(31))
    print('points : ', points)
    print('order : ', len(points))
    print('----')
    print('orders')
    for pt in points[1:]:
        for i in range(1,26,1):
            try:
                if ec.multiply(pt, i) == None and i == 5:
                    print(pt, i)
                    break
            except:
                #print(pt, i, 'err')
                break

    print('----')
    print('(1,18):')
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

def p53():
    print(inspect.stack()[0][3], '>>>>>')
    mod = 11
    ec = FEC([2, 7, 0, 1], mod)
    points = ec.find_point(make_field(mod))
    print('points : ', points)
    print('order : ', len(points))

    field = PolyField([4,1,0,1], mod)
    f_11_3 = field.elements()
    # print(f_11_3[481], f_11_3[1049]) # [4, 7, 4],[6, 2, 10]
    Q = ([4, 7, 4], [6, 2, 10])
    # print(f_11_3[423], f_11_3[840])  # [7, 8, 4], [4, 9, 7]
    R = ([7, 8, 4], [4, 9, 7])
    # print(f_11_3[1011], f_11_3[1244])  # [2, 8, 1], [0, 10, 10]
    S = ([2, 8, 1], [0, 10, 10])
    # print(f_11_3[1315], f_11_3[1150])  # [8, 10, 6], [7, 10, 6]
    T = ([8, 10, 6], [7, 10, 6])
    ec = FEC([2, 7, 0, 1], mod, field)
    print('Tr(Q) ', ec.Tr(Q))
    print('Tr(R) ',ec.Tr(R))
    print('Tr(S) ',ec.Tr(S))
    print('Tr(T) = O')
    print('Tr(T) ', ec.Tr(T))

    #aTr
    pp =ec.add(ec.multiply(Q,3), ec.neg(ec.Tr(Q)) )
    for i, c in enumerate(field.elements()):
        if c == pp[0]:
            print('x', i)
        if c == pp[1]:
            print('y', i)

    # print(f_11_3[831], f_11_3[949]) #[2, 5, 5], [6, 10, 9]
    P_831_949 = ([2, 5, 5], [6, 10, 9])
    pp =ec.add(ec.multiply(P_831_949,3), ec.neg(ec.Tr(P_831_949)) )
    for i, c in enumerate(field.elements()):
        if c == pp[0]:
            print('x', i)
        if c == pp[1]:
            print('y', i)

def p56():
    print(inspect.stack()[0][3], '>>>>>')
    q = mod = 59
    ec = FEC([1, 0, 0, 1], q)
    points = ec.find_point(make_field(mod))
    print('points : ', points)
    print('order : ', len(points))
    if len(points) == (q+1):
        print('supersingular')

    print('------')
    print('g1: ')
    assert ec.frobEndPi((18,46),1) == (18,46)
    print('g2: ')
    assert ec.frobEndPi((36,37j),1) != (36,37j)
    assert ec.frobEndPi((36,37j),2) == (36,37j)
    print('----')
    candidate_r = int_divisor(len(points))
    rs = find_r(points,ec, candidate_r)
    r = rs[1]
    print('k=', find_k(q,r))
    print('----')
    print(subgroups((36, 37j), ec, 3600 + 1))
    print(subgroups((1, 36j), ec, 3600 + 1))
    print(subgroups((36, 22j), ec, 3600 + 1))
    print(subgroups((1, 23j), ec, 3600 + 1))
    print('----')
    cube_root_unity = 24j+29
    cube_root_unity_3 = pow(cube_root_unity,3)
    print( complex((cube_root_unity*18).real %q, (cube_root_unity*18).imag%q)) # (50+19j)
    print(complex((cube_root_unity *36).real % q, (cube_root_unity*36).imag % q)) #(41+38j)
    assert complex((cube_root_unity_3 * 18).real % q, (cube_root_unity_3 * 18).imag % q) == 18
    assert complex((cube_root_unity_3 * 36).real % q, (cube_root_unity_3 * 36).imag % q) == 36

def p57():
    print(inspect.stack()[0][3], '>>>>>')
    q = mod = 59
    ec = FEC([0, 1, 0, 1], q)
    points = ec.find_point(make_field(mod))
    print('points : ', points)
    print('order : ', len(points))
    if len(points) == (q+1):
        print('supersingular')
    print('----')
    candidate_r = int_divisor(len(points))
    rs = find_r(points,ec, candidate_r)
    r = rs[1]
    print('k=', find_k(q,r))
    print('----')
    print(subgroups((34, 30j), ec, 3600 + 1))
    print('----')
    def distortion_map_phi(pt):
        x = -1*pt[0]
        y = 1j*pt[1]
        return ( complex(x.real % q, x.imag % q ) , complex(y.real % q, y.imag % q) )
    step1 = distortion_map_phi((34, 30j))
    step2 = distortion_map_phi(step1)
    print(step1, step2)
    step1 = distortion_map_phi((31j+51, 34j+49))
    step2 = distortion_map_phi(step1)
    step3 = distortion_map_phi(step2)
    step4 = distortion_map_phi(step3)
    print(step1, step2, step3, step4)

def p61():
    print(inspect.stack()[0][3], '>>>>>')
    q = mod = 11
    ec = FEC([4, 0, 0, 1], q)
    points = ec.find_point(make_field(q))
    print('points : ', points)
    print('order : ', len(points))
    print('----')
    candidate_r = int_divisor(len(points))
    # 맞는것지 아직은 미지수
    rs = find_r(points,ec, candidate_r)
    r = rs[0]
    print('k=', find_k(q,r))
    print('----')

    ec1 = FEC([-4, 0, 0, 1], q)
    points1 = ec1.find_point(make_field(q))
    print('points : ', points1)
    print('order : ', len(points1))
    print('----')

    def psi_inv(pt):
        x = pt[0]*(-1)
        y = pt[1]*1j
        return (complex(x.real % q, x.imag % q), complex(y.real % q, y.imag % q))

    print(psi_inv((8, 1j)))
    print(psi_inv((8, 10j)))

    def psi(pt):
        x = pt[0]*(-1)
        y = pt[1]*1j*(-1)
        return (complex(x.real % q, x.imag % q), complex(y.real % q, y.imag % q))

    print(psi((3, 10)))
    print(psi((3, 1)))

def p62():
    print(inspect.stack()[0][3], '>>>>>')
    q = mod = 103
    ec = FEC([72, 0, 0, 1], q)
    points = ec.find_point(make_field(q))
    print('points : ', points)
    print('order : ', len(points))
    print('----')
    candidate_r = int_divisor(len(points))
    # 맞는것지 아직은 미지수
    rs = find_r(points,ec, candidate_r)
    r = rs[0]
    print('k=', find_k(q,r))
    print('----')
    field = PolyField([2, 0, 0, 0, 0, 0, 1], q)
    ec = FEC([72, 0, 0, 1], q, field)
    print(subgroups(([0, 0, 0, 0, 35, 0], [0, 0, 0, 42, 0, 0]), ec, 7))
    print('----')
    print('y^2 = x^3 + 72u^6')
    # u^6+2=0, u^6 = -2
    ec = FEC([72*(-2), 0, 0, 1], q)
    points = ec.find_point(make_field(q))
    print('points : ', points)
    print('order : ', len(points))
    print(subgroups((33,19), ec, 7))
    print('----')
    candidate_r = int_divisor(len(points))
    # 맞는것지 아직은 미지수
    rs = find_r(points,ec, candidate_r)
    r = rs[0]
    print('k=', find_k(q,r))
    print('----')

    print('psi_inv')
    def psi_inv(pt):
        x = field.mul([0, 0, 1], pt[0])
        y = field.mul([0, 0, 0, 1], pt[1])
        return(x,y)

    print('(35u^4,42u^3):')
    print(psi_inv(([0, 0, 0, 0, 35, 0], [0, 0, 0, 42, 0, 0])))
    print('(65u^4,61u^3):')
    print(psi_inv(([0, 0, 0, 0, 65, 0], [0, 0, 0, 61, 0, 0])))
    #58u^5+81u^4....
    print(psi_inv(([8, 49, 66, 99, 81, 58], [71, 65, 66, 14, 23, 8])))

    print('psi')
    def psi(pt):
        x = field.mul( field.inv([0, 0, 1]), pt[0])
        y = field.mul(field.inv([0, 0, 0, 1]), pt[1])
        return(x,y)

    print('(33,19):')
    print(psi((33,19)))
    print('(76,84):')
    print(psi((76,84)))

def p68():
    print(inspect.stack()[0][3], '>>>>>')
    q = mod = 23
    ec = FEC([6, 17, 0, 1], q)
    points = ec.find_point(make_field(q))
    print('points : ', points)
    print('order : ', len(points))
    print('----')
    print(subgroups((10,7), ec, q))
    # candidate_r = int_divisor(len(points))
    # # 맞는것지 아직은 미지수
    # rs = find_r(points,ec, candidate_r)
    # r = rs[0]
    # print('k=', find_k(q,r))
    # print('----')
    # field = PolyField([2, 0, 0, 0, 0, 0, 1], q)
    # ec = FEC([72, 0, 0, 1], q, field)
    # print(subgroups(([0, 0, 0, 0, 35, 0], [0, 0, 0, 42, 0, 0]), ec, 7))
    # print('----')
    # print('y^2 = x^3 + 72u^6')
    # # u^6+2=0, u^6 = -2
    # ec = FEC([72*(-2), 0, 0, 1], q)
    # points = ec.find_point(make_field(q))
    # print('points : ', points)
    # print('order : ', len(points))
    # print(subgroups((33,19), ec, 7))
    # print('----')
    # candidate_r = int_divisor(len(points))
    # # 맞는것지 아직은 미지수
    # rs = find_r(points,ec, candidate_r)
    # r = rs[0]
    # print('k=', find_k(q,r))
    # print('----')
    #
    # print('psi_inv')
    # def psi_inv(pt):
    #     x = field.mul([0, 0, 1], pt[0])
    #     y = field.mul([0, 0, 0, 1], pt[1])
    #     return(x,y)
    #
    # print('(35u^4,42u^3):')
    # print(psi_inv(([0, 0, 0, 0, 35, 0], [0, 0, 0, 42, 0, 0])))
    # print('(65u^4,61u^3):')
    # print(psi_inv(([0, 0, 0, 0, 65, 0], [0, 0, 0, 61, 0, 0])))
    # #58u^5+81u^4....
    # print(psi_inv(([8, 49, 66, 99, 81, 58], [71, 65, 66, 14, 23, 8])))
    #
    # print('psi')
    # def psi(pt):
    #     x = field.mul( field.inv([0, 0, 1]), pt[0])
    #     y = field.mul(field.inv([0, 0, 0, 1]), pt[1])
    #     return(x,y)
    #
    # print('(33,19):')
    # print(psi((33,19)))
    # print('(76,84):')
    # print(psi((76,84)))

def p71():
    print(inspect.stack()[0][3], '>>>>>')
    q = mod = 5
    ec = FEC([-3, 0, 0, 1], q)
    points = ec.find_point(make_field(q))
    print('points : ', points)
    print('order : ', len(points))
    print('----')

    points = ec.find_point(make_a_bi(q,2))
    print('points : ', points)
    print('order : ', len(points))
    print('----')

    rs = find_r_torsion(points, ec, [3])
    print('r_torsion >>')
    print('r = ', rs[0])
    print('coset :')
    for r in rs[1]:
        print(r)
    print('----')

    print('rE>>>')
    rE = find_rE(3,points,ec)
    print(rE)
    print('----')

    print('cosets>>>')
    subs = find_cosets( list(rE), points, ec)
    print('cosets number : ', len(subs))
    print('cosets : ', points)
    for s in subs:
        print(s)
    print('----')

    P1 = (Cpx(i=2, r=0, m=2), Cpx(i=4, r=3, m=2))
    P2 = (Cpx(i=0, r=4, m=2), Cpx(i=0, r=1, m=2))
    P3 = (Cpx(i=0, r=3, m=2), Cpx(i=0, r=2, m=2))
    P4 = (Cpx(i=3, r=0, m=2), Cpx(i=1, r=3, m=2))
    print('P1-P2=P3-P4')
    print(ec.add(P1, (P2[0],-P2[1])))
    print(ec.add(P3, (P4[0],-P4[1])))
    print('P1-P3=P2-P4')
    print(ec.add(P1, (P3[0],-P3[1])))
    print(ec.add(P2, (P4[0],-P4[1])))
    print('P1-P4=P2-P3')
    print(ec.add(P1, (P4[0],-P4[1])))
    print(ec.add(P2, (P3[0],-P3[1])))
    # print(ec.contain((Cpx(0,2,2),Cpx(3,4,2))))


    # H2 = ( Cpx(4,3,2), 0)
    # H3 = ( Cpx(4,2,2), 0)
    # H4 = ( Cpx(2,0,2), 0)
    # P = (Cpx(3, 0, 2), Cpx(2, 0, 2))
    # print(ec.add(H3, P))
    # P = (Cpx(4, 0, 2), Cpx(1, 0, 2))
    # print(ec.add(H3, P))
    # P = (Cpx(0, 2, 2), Cpx(3, 4, 2))
    # print(ec.add(H3, P))
    # print('---------')
    # P = (Cpx(2, 1, 2), Cpx(0, 1, 2))
    # print(ec.add(H3, P))
    # P = (Cpx(1, 0, 2), Cpx(0, 1, 2))
    # print(ec.add(H3, P))
    # print('---------')
    #
    # P = (Cpx(3, 0, 2), Cpx(2, 0, 2))
    # print(ec.add(H2, P))
    # P = (Cpx(4, 0, 2), Cpx(1, 0, 2))
    # print(ec.add(H2, P))
    # P = (Cpx(0, 2, 2), Cpx(3, 4, 2))
    # print(ec.add(H2, P))
    # print('---------')
    # P = (Cpx(2, 1, 2), Cpx(0, 1, 2))
    # print(ec.add(H2, P))
    # P = (Cpx(1, 0, 2), Cpx(0, 1, 2))
    # print(ec.add(H2, P))
    # print('---------')
    # print(ec.multiply(H3, 2))

    # print("(3, 3)>>>>>>")
    # print(ec.multiply((3,2), 2))
    # print(ec.multiply((4,1), 2))
    # print(ec.multiply((Cpx(0,2,2),Cpx(3,4,2)),2))
    # print(ec.multiply((Cpx(0,3,2),Cpx(3,1,2)),2))
    #
    # print("('0+0i', '0+2i')>>>>>>")
    # print(ec.multiply((Cpx(2,1,2),Cpx(0,1,2)),2))
    # print(ec.multiply((Cpx(1,0,2),Cpx(0,1,2)),2))
    # print(ec.multiply((0,Cpx(0,3,2)),2))
    # print(ec.multiply((Cpx(2,4,2),Cpx(0,1,2)),2))
    # print('------')
    # print(subgroups((Cpx(2,1,2),Cpx(0,1,2)), ec, q))


    # print(ec.multiply((Cpx(0,2,2),Cpx(3,4,2)),4))
    # print(ec.multiply((Cpx(0,2,2),Cpx(3,4,2)),5))
    # print(ec.multiply((Cpx(0,2,2),Cpx(3,4,2)),6))
    # ec = FEC([-3, 0, 0, 1], q)
    # points = ec.find_point(make_a_bi(q))
    # print('points : ', points)
    # print('order : ', len(points))
    # print('----')
    # field = PolyField([2,4,1], mod)
    # print(field.elements())
    # ec = FEC([-3, 0, 0, 1], q, field)
    # points = ec.find_point2(field)
    # print('points : ', points)
    # print('order : ', len(points))
    # f_11_3 = field.elements()
    # candidate_r = int_divisor(len(points))
    # print(candidate_r)
    # rs = find_r(points, ec, candidate_r)
    # print(rs)
    # print(subgroups((3,2j), ec, q))

p71()