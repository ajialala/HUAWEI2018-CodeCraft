# coding=utf-8
from numpy.random import rand, seed
from numpy.linalg import det
#生成随机行列式
seed(100)
n = 5
A = rand(n ** 2)
mat = A.reshape(n, n)
print mat
mat = mat.astype('float')
n = mat.shape[0]
print mat
print n
