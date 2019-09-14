import numpy as np

A = [
    [-5.0, 9.166, -5.0, 0.833],
    [8.0, -11.333, 5.0, -0.666],
    [0.0, 0.0, 0.0, 0.0],
    [-6.0, 9.5, -4.0, 0.5],
    [4.0, -7.0, 3.5, -0.5],
    [-1.0, 1.833, -1.0, 0.166]
]
B = [[3.0, -5.166, 2.5, -0.333],
     [-2.0, 5.166, -2.5, 0.333],
     [0.0, 0.0, 0.0, 0.0],
     [0.0, 0.0, 0.0, 0.0],
     [0.0, 0.0, 0.0, 0.0],
     [0.0, 0.0, 0.0, 0.0]
     ]
C = [[0.0, 0.0, 0.0, 0.0],
     [0.0, 0.0, 0.0, 0.0],
     [-1.0, 1.833, -1.0, 0.166],
     [4.0, -4.333, 1.5, -0.166],
     [-6.0, 9.5, -4.0, 0.5],
     [4.0, -7.0, 3.5, -0.5]
     ]


def p(x, l):
    r = l[0] + l[1] * pow(x, 1) + l[2] * pow(x, 2) + l[3] * pow(x, 3)
    print(round(r), ' ', end='')


print('A > ')
for i in range(0, 6):
    p(1, A[i])
    p(2, A[i])
    p(3, A[i])
    p(4, A[i])
    print('')

a = np.array(A).T
s = np.array([1, 3, 35, 9, 27, 30])
print('dot > ')
print('A.s', np.dot(np.array(A).T, s))
print('B.s', np.dot(np.array(B).T, s))
print('C.s', np.dot(np.array(C).T, s))

#https://medium.com/@VitalikButerin/quadratic-arithmetic-programs-from-zero-to-hero-f6d558cea649