# coding=utf-8
from datetime import *
import sys
import os
import collections

flavor_cpu_format={'flavor1':1,'flavor2':1,'flavor3':1,'flavor4':2,
	'flavor5':2,'flavor6':2,'flavor7':4,'flavor8':4,'flavor9':4,
	'flavor10':8,'flavor11':8,'flavor12':8,'flavor13':16,'flavor14':16,
	'flavor15':16,'flavor16':32,'flavor17':32,'flavor18':32,'flavor19':64,
	'flavor20':64,'flavor21':64,'flavor22':128,'flavor23':128}

flavor_mem_format={'flavor1':1,'flavor2':2,'flavor3':4,'flavor4':2,
	'flavor5':4,'flavor6':8,'flavor7':4,'flavor8':8,'flavor9':16,
	'flavor10':8,'flavor11':16,'flavor12':32,'flavor13':16,
	'flavor14':32,'flavor15':64,'flavor16':32,'flavor17':64,'flavor18':128,
	'flavor19':64,'flavor20':128,'flavor21':256,'flavor22':128,'flavor23':256}

flavor_inial={'flavor1':0,'flavor2':0,'flavor3':0,'flavor4':0,
	'flavor5':0,'flavor6':0,'flavor7':0,'flavor8':0,'flavor9':0,
	'flavor10':0,'flavor11':0,'flavor12':0,'flavor13':0,'flavor14':0,
	'flavor15':0,}

def read_lines(file_path):
	if os.path.exists(file_path):
		array = []
		with open(file_path, 'rU') as lines:
			for line in lines:
				array.append(line)
		return array
	else:
		print 'file not exist: ' + file_path
		return None

def write_result(array, outpuFilePath):
	with open(outpuFilePath, 'w') as output_file:
		for item in array:
			output_file.write("%s\n" % item)

	# Read the input files
ecsDataPath = sys.argv[1]
resultFilePath = sys.argv[2]

ecs_infor_array = read_lines(ecsDataPath)
arr = []
for item in ecs_infor_array:
	values = item.split("\t")
	string = ''
	string += values[1][6:]
	string += ','
	string += str(flavor_cpu_format[values[1]])
	string += ','
	string += str(flavor_mem_format[values[1]])
	string += ','
	string += values[2][:4]
	string += ','
	string += values[2][5:7]
	string += ','
	string += values[2][8:10]
	string += ','
	date_week = date(int(values[2][:4]),int(values[2][5:7]),int(values[2][8:10])).weekday()
	string += str(date_week)
	#valuesss=date(int(valuess[:4]),int(valuess[5:7]),int(valuess[8:10])).weekday()
	arr.append(string)



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
		all_flavor = flavor_inial.copy()
		for key,value in flavors.items():
			all_flavor[key] = value
		for key,value in all_flavor.items():
			string = ''
			string += key[6:]
			string += ','
			string += str(flavor_cpu_format[key])
			string += ','
			string += str(flavor_mem_format[key])
			string += ','
			temp = train_array[dayturn_posions[dayturn_posion]].split("\t")
			string += temp[2][:4]
			string += ','
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

write_result(every_day_flavor(ecs_infor_array), resultFilePath)


