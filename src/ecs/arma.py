# coding=utf-8
import sys
import os
import datetime
import math

import arma_math
import diff

def decent(meandata,data):
	for i in range(0,len(data)):
		#data[i] = round(data[i]-meandata,5)
		data[i] -= meandata
	return data

def cent(meandata,data):
	for i in range(0,len(data)):
		#data[i] = round(data[i]-meandata,5)
		data[i] += meandata
	return data

def build_x(n,data):
	result = []
	for i in range(0,len(data)-n):
		b = data[i:i+n]
		b.reverse()
		result.append(b)
	return result

def least_squ(n,data):
	y = arma_math.vector(data[n:])
	x = build_x(n,data)
	x_T = arma_math.trans(x)
	try:
		first = arma_math.invert(arma_math.matrix_mul(x_T,x))
	except AssertionError:
		return [[0.3]]*n
	second = arma_math.matrix_mul(first,x_T)
	third = arma_math.matrix_mul(second,y)
	return third

def p_least_squ(n,data):
	k = n + 16
	p = []
	for i in range(k+1):
		try:
			p.append(arma_math.p_k(i,data))
		except ZeroDivisionError:
			return [[0.1]]*n
	t = []
	for i in range(k):
		t.append([])
		temp = p[1:i+1]
		temp.reverse()
		t[i] = temp + p[:n-i]
	p = arma_math.vector(p[1:])
	t_T = arma_math.trans(t)
	first = arma_math.invert(arma_math.matrix_mul(t_T,t))
	second = arma_math.matrix_mul(first,t_T)
	third = arma_math.matrix_mul(second,p)
	return third

def bic_crit(phi,data):
	a = 0
	for i in range(len(data)-len(phi)):
		j = -1
		tem_sum = 0
		for value in phi:
			tem_sum += value[0] * data[len(phi)+i+j]
			j -= 1
		a += (tem_sum - data[len(phi)+i]) ** 2
	N = len(data)
	p = len(phi)
	if a == 0:
		return 0
	result = N * math.log(a / (N-p)) + p * math.log(N)
	return result

def AR(data):
	phi = []
	bic = []
	n = 5
	for i in range(1,n):
		phi.append(least_squ(i,data))
		bic.append(bic_crit(phi[-1],data))
	min_bic = min(bic)
	for i in range(0,n-1):
		if bic[i] == min_bic:
			#print i + 1
			return phi[i]
			break

def ARMA(data):
	I = AR(data)
	p = len(I)
	theta = [[]]
	for m in range(1,p):
		pre_theta = theta
		n = p - m
		x = []
		for i in range(m):
			x.append([])
			for j in range(m):
				x[i].append(I[n+i-j-1][0])
		y = I[n:]
		try:
			theta = arma_math.matrix_mul(arma_math.invert(x),y)
		except AssertionError:
			theta = [[0]] * m
		if theta[-1][0] < 0.01:
			if m == 1:
				m = 2
				break
			else:
				theta = pre_theta
			break
	m = m -1
	n = p - m
	x = []
	for i in range(n):
		x.append([])
		for j in range(n):
			if j == i:
				x[i].append(1)
			elif j > i:
				x[i].append(0)
			else:
				if i-j-1 > m-1:
					x[i].append(0)
				else:
					x[i].append(-1 * theta[i-j-1][0])
	mul = arma_math.matrix_mul(x,I[:n])
	phi = []
	for i in range(n):
		if i > m-1:
			phi.append(mul[i][0])
		else:
			phi.append(theta[i][0] + mul[i][0])
	i = -1
	for j in range(len(phi)):
		if abs(phi[i]) < 0.01:
			i -= 1
		else:
			break
	return phi[:i+1],theta
