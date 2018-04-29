# coding=utf-8
import sys
import os

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
	'flavor15':0,'flavor16':0,'flavor17':0,'flavor18':0,'flavor19':0,
	'flavor20':0,'flavor21':0,'flavor22':0,'flavor23':0,}

def main():
	print 'output your score'
	if len(sys.argv) != 3:
		print 'parameter is incorrect!'
		print 'Usage: python get_csv_score.py resultFilePath.csv testFilePath.csv'
		exit(1)
	resultFilePath = sys.argv[1]
	testFilePath = sys.argv[2]
	result_array = read_lines(resultFilePath)
	test_array = read_lines(testFilePath)
	pre_flavors = flavor_inial.copy()
	rel_flavors = flavor_inial.copy()
	a = 1
	for value in test_array[1:]:
		values = value.split(",")
		rel_flavors['flavor'+values[1]] = int(values[8])
		pre_flavors['flavor'+values[1]] = int(round(float(result_array[a])))
		a += 1
	compute_score(rel_flavors,pre_flavors)


def compute_score(rel_flavors,pre_flavors):   #计算分数
	x_2 = 0
	y_2 = 0
	y_x_2 = 0
	print 'Please input the format of flavors you need to predict:'
	print 'eg: 1 3 7 12 15'
	message = raw_input()
	message = message.split(' ')
	for value in message:
		x_2 += rel_flavors['flavor'+value] ** 2
		y_2 += pre_flavors['flavor'+value] ** 2
		y_x_2 += (pre_flavors['flavor'+value] - rel_flavors['flavor'+value]) ** 2
	a = y_x_2 ** 0.5
	b = x_2 ** 0.5
	c = y_2 ** 0.5
	score = (1 - a / (b + c))*100
	print 'the accuracy of prediction is:'
	print score

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
        
if __name__ == "__main__":
    main()
