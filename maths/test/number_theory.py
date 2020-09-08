import unittest
from maths.number_theory import *
class TestPolyField(unittest.TestCase):
    # u^3 + u + 4 [4,1,0,1], 손으로 계산 필요
    def test_mul(self):
        field = PolyField([4, 1, 0, 1], 11)
        self.assertEqual(field.mul([1, 1, 1], [2, 2, 2]), [8,3,4])
        self.assertEqual(field.mul([1], [2, 2, 2]), [2, 2, 2])

    def test_add(self):
        # x^3+2x+1 역순
        field = PolyField([1,2,0,1], 3)
        self.assertEqual(field.add([1], [1,1,1]), [2, 1, 1])

    # https://math.stackexchange.com/questions/124300/finding-inverse-of-polynomial-in-a-field
    def test_inv(self):
        # x^3+2x+1 역순
        field = PolyField([1,2,0,1], 3)
        self.assertEqual(field.inv([1,0,1]), [2,1,2])

    def test_elements(self):
        # x^3+2x+1 역순
        field = PolyField([1,2,0,1], 3)
        f_3_3 = field.elements()

        #order: 27 : f_3_3, [0,0,0]
        #cycyle: 27-1 = 26
        self.assertEqual(len(f_3_3), 3**3-1)

        #[0] x^0, [1] x^1, [25]=>[26]~[0] cycle
        self.assertEqual(field.mul(f_3_3[25], f_3_3[1]), f_3_3[0])

        #inverse x+y=26이면 [x]*[y]=[1,0,0]
        self.assertEqual(field.mul(f_3_3[2], f_3_3[26-2]), f_3_3[0])
        # print(f_3_3[2], f_3_3[26 - 2])
        self.assertEqual(field.mul(f_3_3[5], f_3_3[26 - 5]), f_3_3[0])
        # print(f_3_3[5], f_3_3[26 - 5])

    def test_div(self):
        # x^3+2x+1=0
        field = PolyField([1,2,0,1], 3)
        f_3_3 = field.elements()
        for i, c in enumerate(f_3_3):
            if i == 0:
                continue
            self.assertEqual(field.inv(f_3_3[i]), f_3_3[26 - i] )

#https://docs.python.org/ko/3/library/unittest.html