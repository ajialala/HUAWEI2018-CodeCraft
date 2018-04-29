# coding=utf-8
import sys
import os
import datetime
import copy
import diff

def mean_value(data):
	sum = 0
	for value in data:
		sum += value
	return float(sum) / len(data)

def var(data):
	sum = 0
	mean = mean_value(data)
	for value in data:
		sum += (value-mean)*(value-mean)
	return float(sum) / len(data)

def r_k(k,data):
	sum = 0
	mean = mean_value(data)
	length = len(data) - k
	if k == 0:
		for value in data:
			sum += (value-mean)*(value-mean)
	else:
		for value in data[:-k]:
			sum += value * data[k]
			k += 1
	#return float(sum) / len(data)
	return float(sum) / length

def p_k(k,data):
	return r_k(k,data) / var(data)

def h2(k,data):
	p = []
	for i in range(0,k+1):
		p.append(p_k(i,data))
	y = vector(p[1:])
	x = []
	for i in range(0,k):
		x.append([])
		for j in range(0,i):
			x[i].append(p[i-j])
		for value in p[:k-i]:
			x[i].append(value)
	h = matrix_mul(invert(x),y)
	return h[-1][0]

def matrix_mul(A, B):
	if len(A[0]) != len(B):
		return 'false'
	return [[sum(a * b for a, b in zip(a, b)) for b in zip(*B)] for a in A]

def det(mat):
	#为了节省空间，直接在输入的行列式上进行了化简，而没有使用copy
	n = len(mat)
	res = 1
	#遍历列
	for col in range(n):
		row = col
		res *= mat[row][col]
		#寻找不是0的位置row
		while mat[row][col] == 0 and row < n - 1:
			row += 1
		#化简mat[row,col]下面的每一元素为0
		for i in range(row + 1, n):
			if mat[i][col] == 0:
				pass
			else:
				k = - mat[i][col] / mat[row][col]
				for j in range(col ,n):
					mat[i][j] += mat[row][j] * k
	return res

def trans(m):
	return zip(*m)

def adj(m):
	result = copy.deepcopy(m)
	for i in range(0,len(m)):
		for j in range(0,len(m)):
			a = copy.deepcopy(m)
			del a[i]
			for p in range(0,len(m)-1):
				del a[p][j]
			result[i][j] = (-1)**(i+j) * det(a)
	result = trans(result)
	return result

def dot(a,m):
	result = []
	for value in m:
		result.append([])
	b = 0
	for value in m:
		for value1 in value:
			result[b].append(a*value1)
		b += 1
	return result

def identity(n):
	'''单位矩阵'''
	m = []
	for i in range(n):
		m.append([])
		for j in range(n):
			m[i].append(0)
	for r in range(n):
		for c in range(n):
			m[r][c] = 1.0 if r == c else 0.0
	return m

def invert(ma):
	'''逆矩阵'''
	m = copy.deepcopy(ma)
	row = len(m)
	column = len(m[0])
	if len(m) != len(m[0]):
		print '不是方阵'
	I = identity(len(m)) # 单位矩阵

	# 拼接
	for r in range(0,row):
		temp = m[r]
		temp.extend(I[r])
		m[r] = copy.deepcopy(temp)

	# 初等行变换
	for r in range(0,row):
		# 本行首元素(M[r, r])若为 0，则向下交换最近的当前列元素非零的行
		if m[r][r] == 0:
			for rr in range(r, 2*row):
				if m[rr][r] != 0:
					m[r],m[rr] = m[rr],m[r] # 交换两行
				break

		assert m[r][r] != 0, '矩阵不可逆'
            
		# 本行首元素(M[r, r])化为 1
		temp = m[r][r] # 缓存
		for c in range(r-1,2*column):
			m[r][c] = m[r][c] / float(temp)
			#print("M[{0}, {1}] /=  {2}".format(r,c,temp))

		# 本列上、下方的所有元素化为 0
		for rr in range(0, row):
			temp = m[rr][r] # 缓存
			for c in range(r-1, 2*column):
				if rr == r:
					continue
				m[rr][c] -= float(temp) * m[r][c]
				#print("M[{0}, {1}] -= {2} * M[{3}, {1}]".format(rr, c, temp,r))  

	# 截取逆矩阵
	N = []
	for i in range(row):
		N.append([])
		for j in range(row):
			N[i].append(0)
	for r in range(0,row):
		N[r] = m[r][row:]
	return N

def vector(arr):
	result = []
	for value in arr:
		result.append([value])
	return result

def medi_fil(data):
	n = 7
	half = (n - 1) / 2
	meandata = mean_value(data)
	for i in range(half,len(data)-half):
		if data[i] > 10 * meandata:
			temp = data[i-half:i+half+1]
			temp.sort()
			data[i] = temp[half]
	return data

def mean_fil(data):
	n = 3
	half = (n - 1) / 2
	meandata = mean_value(data)
	for i in range(half,len(data)-half):
		if data[i] > 10 * meandata:
			temp = data[i-half:i+half+1]
			mean = mean_value(temp)
			data[i] = mean
	return data
	
def mean7_fil(data):
	meandata = mean_value(data)
	for i in range(len(data)):
		if data[i] > 12 * meandata:
			newdata = data[i:] + data[:i]
			find = []
			for j in range(len(newdata)):
				m = j % 7
				if m == 0:
					find.append(newdata[j])
			data[i] = mean_value(newdata)
	return data
 
def fil(data):
	mean = mean_value(data)
	for i in range(len(data)):
		if data[i] > 10 * mean:
			data[i] = 6 * mean
			#if data[i] > 1:
			#	data[i] = data[i] * 0.5
	return data
