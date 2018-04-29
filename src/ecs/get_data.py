# coding=utf-8
import sys
import os
import datetime

def get_everyday_flavor(train_array):
	everyday_flavor = {}
	for i in range(1,25):
		everyday_flavor['flavor'+str(i)] = []
	a = '0001-01-01'				#当前日期初始化
	flag = 0
	for value in train_array:
		values = value.split("\t")
		if values[2][:10] != a:
			d1 = datetime.date(int(a[:4]),int(a[5:7]),int(a[8:10]))
			d2 = datetime.date(int(values[2][:4]),int(values[2][5:7]),int(values[2][8:10]))
			day_delta = (d2-d1).days
			if flag == 0:
				flag =1
				day_delta = 1
			a = values[2][:10]
			for i in range(1,25):
				for j in range(1,day_delta+1):
					everyday_flavor['flavor'+str(i)].append(0)
		everyday_flavor[values[1]][-1] += 1
	
	return everyday_flavor	
