# coding=utf-8
import datetime
import arma
import arma_math
import diff
import math

def predict_ar(last_day,day1,day2,data):
	#data = update(data)
	data = arma_math.fil(data)
	data = [a ** (1./2) for a in data]
	firsr_order = 1
	second_order = 7
	temp1 = data[0:firsr_order]
	data = diff.diff(firsr_order,data)
	data = diff.diff(second_order,data[firsr_order:])
	meandata = arma_math.mean_value(data)
	data = arma.decent(meandata,data)
	var = arma_math.var(data)
	try:
		data = [a / var for a in data]
	except ZeroDivisionError:
		var = 1
	phi = arma.AR(data[second_order:])
	#phi,theta = arma.ARMA(data[second_order:])
	last_day = datetime.date(int(last_day[-20:-16]),int(last_day[-15:-13]),int(last_day[-12:-10]),)
	d1 = datetime.date(int(day1[:4]),int(day1[5:7]),int(day1[8:10]))
	d2 = datetime.date(int(day2[:4]),int(day2[5:7]),int(day2[8:10]))

	data = ar_predict(data,phi,(d2-d1).days)
	#data = arma_predict(data,phi,theta,(d2-d1).days)
	data = [a * var for a in data]
	data = arma.cent(meandata,data)
	data = diff.rediff(second_order,data)
	data = diff.rediff(firsr_order,temp1+data)
	for i in range(len(data)):
		if data[i] < 0:
			data[i] = 0
	data = [a ** 2 for a in data]
	absList = map(round, data[-(d2-d1).days:])
	return round(sum(data[-(d2-d1).days:]))
	#return round(sum(absList))

def ar_predict(data,phi,days):
	for i in range(0,days-1):
		j = -1
		tem_sum = 0
		for value in phi:
			tem_sum += value[0] * data[j]
			j -= 1
		data.append(tem_sum)
	return data

def arma_predict(data,phi,theta,days):
	n = len(phi)
	m = len(theta)
	maxnum = max([n,m])
	a = [data[0]]
	for i in range(1,maxnum):
		j = -1
		ar_sum = 0
		ma_sum = 0
		for k in range(i):
			if k < n:
				ar_sum += phi[k] * data[i+j]
			if k < m:
				ma_sum += theta[k][0] * a[i+j]
			j -= 1
		a.append(data[i] - ar_sum + ma_sum)
	
	for i in range(len(data)-maxnum):
		j = -1
		k = -1
		ar_sum = 0
		ma_sum = 0
		for value in phi:
			ar_sum += value * data[maxnum+i+j]
			j -= 1
		for value in theta:
			ma_sum += value[0] * a[maxnum+i+k]
			k -= 1
		a.append(data[i] - ar_sum + ma_sum)
	
	for i in range(0,days-1):
		j = -1
		k = -1
		ar_sum = 0
		ma_sum = 0
		for value in phi:
			ar_sum += value * data[j]
			j -= 1
		if i < m - 1:
			for value in theta[i:]:
				ma_sum += value[0] * a[k]
				k -= 1
		data.append(ar_sum - ma_sum)
	return data


