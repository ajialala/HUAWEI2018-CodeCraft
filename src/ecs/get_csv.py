# coding=utf-8
from datetime import *
import sys
import os
import collections

def getcsv(ecs_infor_array,need_flavor,day1,day2):
	d1 = date(int(day1[:4]),int(day1[5:7]),int(day1[8:10]))
	d2 = date(int(day2[:4]),int(day2[5:7]),int(day2[8:10]))
	print d1
	print d2
	print need_flavor
	arr = []
	for i in range((d2-d1).days):
		for j in need_flavor:
			today = d1 + timedelta(days=i)
			string = ''
			string += j[6:]
			string += ','
			string += str(int(str(today)[5:7]))
			string += ','
			string += str(int(str(today)[8:10]))
			string += ','
			string += str(today.weekday())
			arr.append(string)
	write_result(arr, 'zhangjialiu.csv')
	write_result(every_day_flavor(ecs_infor_array), 'traindata1.csv')
	


def write_result(array, outpuFilePath):
	with open(outpuFilePath, 'w') as output_file:
		for item in array:
			output_file.write("%s\n" % item)

def every_day_flavor(train_array):
	a = '0'
	b = 0
	dayturn_posions = []
	for value in train_array:
		values = value.split("\t")
		if values[2][:10] != a:
			dayturn_posions.append(b)
			a = values[2][:10]
		b += 1
	dayturn_posions.append(b)
	arr = []
	for dayturn_posion in range(0,len(dayturn_posions)-1):
		flavor = []
		for value in train_array[dayturn_posions[dayturn_posion]:dayturn_posions[dayturn_posion+1]]:
			values = value.split("\t")
			flavor.append(values[1])
		flavors = collections.Counter(flavor)
		all_flavor = {}
		for key,value in flavors.items():
			all_flavor[key] = value
		for key,value in all_flavor.items():
			string = ''
			string += key[6:]
			string += ','
			temp = train_array[dayturn_posions[dayturn_posion]].split("\t")
			string += temp[2][5:7]
			string += ','
			string += temp[2][8:10]
			string += ','
			date_week = date(int(temp[2][:4]),int(temp[2][5:7]),int(temp[2][8:10])).weekday()
			string += str(date_week)
			string += ','
			string += str(value)
			arr.append(string)
	return arr

