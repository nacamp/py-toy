import inspect
from maths.elliptic_curves import *


# https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjhiuXAzbzrAhWzL6YKHQohB1oQFjAAegQIBBAB&url=http%3A%2F%2Fwww.craigcostello.com.au%2Fpairings%2FPairingsForBeginners.pdf&usg=AOvVaw1H5dLtelG00vWsvWRGxBNZ
# ParingsForBeginners.pdf
def p22():
    print(inspect.stack()[0][3])
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


def p23():
    print(inspect.stack()[0][3])
    ec = FEC([100, 905, 0, 1], 1021)
    points = ec.find_point(make_f(1021))
    print('points : ', points)
    print('order : ', len(points))
    print(ec.fmultiply((612, 827), 20))
    pt = (612, 827)
    for i in range(1, 106):
        pt = ec.fmultiply(pt, i)
        if pt is None:
            print(i, 'None')
            break
        if pt == (1006, 416):
            print(i)
    #
    # def _subgroups(pt):
    #     pts = []
    #     pts.append((0,0))
    #     for i in range(1, 106):
    #         pt = ec.fmultiply(pt, i)
    #         if pt is None:
    #             break
    #         pts.append(pt)
    #     return pts
    # print('order 1  [105](47,12)  >>')
    # pts = _subgroups(ec.fmultiply((47,12), 105))
    # print( 'order: ', len(pts), 'sub: ', pts)
    #
    # print('order 3  [35](47,12)  >>')
    # pts = _subgroups(ec.fmultiply((47,12), 35))
    # print( 'order: ', len(pts), 'sub: ', pts)
    #
    # print('order 5  [21](47,12)  >>')
    # pts = _subgroups(ec.fmultiply((47,12), 21))
    # print( 'order: ', len(pts), 'sub: ', pts)
    #
    # print('order 7  [15](47,12)  >>')
    # pts = _subgroups(ec.fmultiply((47,12), 15))
    # print( 'order: ', len(pts), 'sub: ', pts)
    #
    # print('order 15  [7](47,12)  >>')
    # pts = _subgroups(ec.fmultiply((47,12), 7))
    # print( 'order: ', len(pts), 'sub: ', pts)
    #
    # print('order 21  [5](47,12)  >>')
    # pts = _subgroups(ec.fmultiply((47,12), 5))
    # print( 'order: ', len(pts), 'sub: ', pts)
    #
    # print('order 35  [3](47,12)  >>')
    # pts = _subgroups(ec.fmultiply((47,12), 3))
    # print( 'order: ', len(pts), 'sub: ', pts)
    #
    # print('order 105  [1](47,12)  >>')
    # pts = _subgroups(ec.fmultiply((47,12), 1))
    # print( 'order: ', len(pts), 'sub: ', pts)
    # '''
    # order는 소수값으로 만들어지고 있음
    # '''


p22()
