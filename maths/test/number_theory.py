import unittest
from maths.number_theory import *
class TestNumberTheory(unittest.TestCase):

    def test_poly_mul(self):
        self.assertEqual(poly_mul([1, 1, 1], [2, 2, 2], irr_coef=[7, 10, 1], mod=5), [4,3,2])

    def test_make_extension_field(self):
        # x^3+2x+1=0 => x^3=0x^2+1x+2, mod = 3
        irr_coef = [2, 1, 0]
        f_3_3 = make_extension_field(irr_coef, 3)

        #order: 27 : f_3_3, [0,0,0]
        #cycyle: 27-1 = 26
        self.assertEqual(len(f_3_3), 3**3-1)

        #[0] x^0, [1] x^1, [25]=>[26]~[0] cycle
        self.assertEqual(poly_mul(f_3_3[25], f_3_3[1], irr_coef=irr_coef, mod=3), f_3_3[0])

        #inverse x+y=26이면 [x]*[y]=[1,0,0]
        self.assertEqual(poly_mul(f_3_3[2], f_3_3[26-2], irr_coef=irr_coef, mod=3), f_3_3[0])
        # print(f_3_3[2], f_3_3[26 - 2])
        self.assertEqual(poly_mul(f_3_3[5], f_3_3[26 - 5], irr_coef=irr_coef, mod=3), f_3_3[0])
        # print(f_3_3[5], f_3_3[26 - 5])

    def test_poly_div(self):
        # x^3+2x+1=0 => x^3=0x^2+1x+2, mod = 3
        irr_coef = [2, 1, 0]
        f_3_3 = make_extension_field(irr_coef, 3)
        for i, c in enumerate(f_3_3):
            if i == 0:
                continue
            self.assertEqual(poly_div(f_3_3[i], [1,2,0,1],3), f_3_3[26 - i] )

#https://docs.python.org/ko/3/library/unittest.html