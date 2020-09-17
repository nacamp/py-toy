import unittest
from maths.number_theory import *
from maths.elliptic_curves import *

class TestEllipticCurves(unittest.TestCase):
    sub_group = (None, ([4, 7, 4], [6, 2, 10]), ([5, 7, 2], [2, 2, 2]), ([4, 2, 1], [3, 10, 0]), ([4, 7, 4], [5, 9, 1]),
                 ([5, 7, 2], [9, 9, 9]), ([4, 2, 1], [8, 1, 0]))
    def test_poly_double(self):
        mod = 11
        field = PolyField([4,1,0,1], mod)
        f_11_3 = field.elements()
        print(len(f_11_3))
        print(f_11_3[481], f_11_3[1049])
        print(f_11_3[1052], f_11_3[924])
        print(f_11_3[1264], f_11_3[740])
        print(f_11_3[481], f_11_3[384])
        print(f_11_3[1052], f_11_3[259])
        print(f_11_3[1264], f_11_3[75])
        print('---------------------')
        print(poly_double(((4, 7, 4), (6,2,10)), 7, field))
        print(poly_double(((5, 7, 2), (2, 2, 2)), 7, field))
        print(poly_double(((4, 2, 1), (3, 10, 0)), 7, field))
        print(poly_double(((4, 7, 4), (5,9,1)), 7, field))
        print(poly_double(((5, 7, 2), (9, 9, 9)), 7, field))
        print(poly_double(((4, 2, 1), (8, 1, 0)), 7, field))
        self.assertIn(poly_double(((4, 2, 1), (8, 1, 0)), 7, field), TestEllipticCurves.sub_group)
        # [4, 7, 4][6, 2, 10]
        # [5, 7, 2][2, 2, 2]
        # [4, 2, 1][3, 10, 0]
        # [4, 7, 4][5, 9, 1]
        # [5, 7, 2][9, 9, 9]
        # [4, 2, 1][8, 1, 0]
        # ---------------------
        # ([4, 2, 1], [8, 1, 0])
        # ([4, 7, 4], [6, 2, 10])
        # ([5, 7, 2], [9, 9, 9])
        # ([4, 2, 1], [3, 10, 0])
        # ([4, 7, 4], [5, 9, 1])
        # ([5, 7, 2], [2, 2, 2])

    def test_poly_add(self):
        mod = 11
        field = PolyField([4,1,0,1], mod)
        f_11_3 = field.elements()
        print(len(f_11_3))
        print(f_11_3[481], f_11_3[1049])
        print(f_11_3[1052], f_11_3[924])
        print(f_11_3[1264], f_11_3[740])
        print(f_11_3[481], f_11_3[384])
        print(f_11_3[1052], f_11_3[259])
        print(f_11_3[1264], f_11_3[75])
        print('---------------------')
        print(poly_add(((4, 7, 4), (6,2,10)), ((5, 7, 2), (2,2,2)), 7, field))
        print(poly_add(((4, 7, 4), (6,2,10)), ((4, 2, 1), (3,10,0)), 7, field))
        print(poly_add(((4, 7, 4), (6, 2, 10)), ((4, 7, 4), (5, 9, 1)), 7, field))
        print(poly_add(((4, 7, 4), (6, 2, 10)), ((5, 7, 2), (9, 9, 9)), 7, field))
        print(poly_add(((4, 7, 4), (6, 2, 10)), ((4, 2, 1), (8, 1, 0)), 7, field))

        print('---------------------')
        ec = FEC([2, 7, 0, 1], 11, field)
        print(ec.add(((4, 7, 4), (6, 2, 10)), ((5, 7, 2), (2, 2, 2)) ))
        print(ec.add(((4, 7, 4), (6, 2, 10)), ((4, 2, 1), (3, 10, 0)) ))
        print(ec.add(((4, 7, 4), (6, 2, 10)), ((4, 7, 4), (5, 9, 1)) ))
        print(ec.add(((4, 7, 4), (6, 2, 10)), ((5, 7, 2), (9, 9, 9)) ))
        print(ec.add(((4, 7, 4), (6, 2, 10)), ((4, 2, 1), (8, 1, 0)) ))
        self.assertIn(ec.add(((4, 7, 4), (6, 2, 10)), ((4, 2, 1), (8, 1, 0)) ), TestEllipticCurves.sub_group)

    def test_poly_multiply(self):
        mod = 11
        field = PolyField([4,1,0,1], mod)
        f_11_3 = field.elements()
        print(len(f_11_3))
        print(f_11_3[481], f_11_3[1049])
        print(f_11_3[1052], f_11_3[924])
        print(f_11_3[1264], f_11_3[740])
        print(f_11_3[481], f_11_3[384])
        print(f_11_3[1052], f_11_3[259])
        print(f_11_3[1264], f_11_3[75])
        print('---------------------')
        print(poly_multiply(((4, 7, 4), (6, 2, 10)), 1, 7, field))
        print(poly_multiply(((4, 7, 4), (6, 2, 10)), 2, 7, field))
        print(poly_multiply(((4, 7, 4), (6, 2, 10)), 3, 7, field))
        print(poly_multiply(((4, 7, 4), (6, 2, 10)), 4, 7, field))
        print(poly_multiply(((4, 7, 4), (6, 2, 10)), 5, 7, field))
        print(poly_multiply(((4, 7, 4), (6, 2, 10)), 6, 7, field))
        print(poly_multiply(((4, 7, 4), (6, 2, 10)), 7, 7, field))
        print(poly_multiply(((4, 7, 4), (6, 2, 10)), 8, 7, field))
        self.assertEqual(poly_multiply(((4, 7, 4), (6, 2, 10)), 7, 7, field), None)

        print('---------------------')
        ec = FEC([2, 7, 0, 1], 11, field)
        print(ec.multiply(((4, 7, 4), (6, 2, 10)), 1 ))
        print(ec.multiply(((4, 7, 4), (6, 2, 10)), 2 ))
        print(ec.multiply(((4, 7, 4), (6, 2, 10)), 3 ))
        print(ec.multiply(((4, 7, 4), (6, 2, 10)), 4 ))
        print(ec.multiply(((4, 7, 4), (6, 2, 10)), 5 ))
        print(ec.multiply(((4, 7, 4), (6, 2, 10)), 6))
        print(ec.multiply(((4, 7, 4), (6, 2, 10)), 7 ))
        print(ec.multiply(((4, 7, 4), (6, 2, 10)), 8))
        self.assertEqual(ec.multiply(((4, 7, 4), (6, 2, 10)), 7 ), None)

    def test_finite_Cpx(self):
        pt = finite_double((Cpx(8, 0), Cpx(0, 1)), 0, 11)
        self.assertEqual(pt, (Cpx(8, 0), Cpx(0, 10)))
        pt = finite_double((Cpx(8, 0), Cpx(0, 10)), 0, 11)
        self.assertEqual(pt, (Cpx(8, 0), Cpx(0, 1)))

        pt = finite_add((Cpx(8, 0), Cpx(0, 1)), (Cpx(8, 0), Cpx(0, 10)), 0, 11)
        self.assertEqual(pt, None)

        # self.assertEqual(pt, Cpx(0, 10))
        # print(ec.multiply((8, 1j), 1))
        # print(ec.multiply((8, 1j), 2))
        # print(ec.multiply((8, 1j), 3))
        #    print(ec.multiply((8,10j), 3))
#https://docs.python.org/ko/3/library/unittest.html