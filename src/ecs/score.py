# coding=utf-8
import sys
import os
import datetime

flavor_cpu_format={'flavor1':1,'flavor2':1,'flavor3':1,'flavor4':2,
	'flavor5':2,'flavor6':2,'flavor7':4,'flavor8':4,'flavor9':4,
	'flavor10':8,'flavor11':8,'flavor12':8,'flavor13':16,'flavor14':16,
	'flavor15':16,}

flavor_mem_format={'flavor1':1,'flavor2':2,'flavor3':4,'flavor4':2,
	'flavor5':4,'flavor6':8,'flavor7':4,'flavor8':8,'flavor9':16,
	'flavor10':8,'flavor11':16,'flavor12':32,'flavor13':16,
	'flavor14':32,'flavor15':64,}
	
flavor_inial={'flavor1':0,'flavor2':0,'flavor3':0,'flavor4':0,
	'flavor5':0,'flavor6':0,'flavor7':0,'flavor8':0,'flavor9':0,
	'flavor10':0,'flavor11':0,'flavor12':0,'flavor13':0,'flavor14':0,
	'flavor15':0,}

def main():
	print 'output your score'
	if len(sys.argv) != 4:
		print 'parameter is incorrect!'
		print 'Usage: python score.py resultFilePath testFilePath inputFilePath'
		exit(1)
	resultFilePath = sys.argv[1]
	testFilePath = sys.argv[2]
	inputFilePath = sys.argv[3]
	input_array = read_lines(inputFilePath)
	input_inf = read_input(input_array)
	result_array = read_lines(resultFilePath)
	pre_flavor, server_inf=exam_result(result_array,input_inf)
	test_file_array = read_lines(testFilePath)
	testflavors = test_flavors(input_inf[-2],input_inf[-1],test_file_array)
	cpu_score,mem_score = compute_score(testflavors,pre_flavor,server_inf,input_inf)
	print 'your cpu_score is:'
	print cpu_score
	print 'your mem_score is:'
	print mem_score
	print 'main function end.'

def read_input(input_array):           #读取输入信息
	enterindex = find_repeat(input_array,'\n')
	if len(enterindex) != 3:
		print "your input.txt is wrong!"
		print '!!!!!!!!!!!!!!!!!!!!!!!!!!!'
	server = input_array[0].split(" ")
	oneserver_cpus = int(server[0])
	oneserver_mems = int(server[1])
	cpu_or_mem = input_array[-4]
	start_time = input_array[-2]
	end_time = input_array[-1]
	value = [oneserver_cpus,oneserver_mems,cpu_or_mem,start_time,end_time]
	return value

def exam_result(result_array,input_inf):         #检查输出是否有问题，返回预测和安排情况 
	enterindex = find_repeat(result_array,'\n')    #找到空行的位置
	if len(enterindex) != 1:                       #判断有几个空行
		print "your result.txt is wrong!"
		print '!!!!!!!!!!!!!!!!!!!!!!!!!!!'   
		return        
	else:                                          #将输出结果分为两部分
		flavor = result_array[:enterindex[0]]
		server = result_array[enterindex[0]+1:]
	
	pre_flavor = flavor_inial.copy()               #初始化
	server_all_flavor = flavor_inial.copy()
	
	flavor_sum = 0								   #计算flavor的总数，看对不对
	for item in flavor[1:]:
		values = item.split(" ")
		flavor_sum = flavor_sum + int(values[1])
		pre_flavor[values[0]] = int(values[1])
	if flavor_sum != int(flavor[0]):
		print 'your number of flavor is wrong!'
		print '!!!!!!!!!!!!!!!!!!!!!!!!!!!'  
	
	server_sum = 0								   #看server对不对,溢了没
	server_cpus = 0
	server_mems = 0
	oneserver_cpus = input_inf[0]
	oneserver_mems = input_inf[1]
	for item in server[1:]:
		values = item.split(" ")
		server_sum += 1
		if int(values[0]) != server_sum :
			print 'your number of server is wrong!'
			print '!!!!!!!!!!!!!!!!!!!!!!!!!!!'
		i = 1
		this_server_cpus = 0
		this_server_mems = 0
		for value in values[1:]:
			if i % 2 != 0:
				temp = value
			else:
				server_all_flavor[temp] += int(value)
				this_server_cpus += flavor_cpu_format[temp] * int(value)
				this_server_mems += flavor_mem_format[temp] * int(value)
			i += 1
		server_cpus += this_server_cpus
		server_mems += this_server_mems
		if this_server_cpus > oneserver_cpus:
			print 'cpus of server is out of numbers!'
			print '!!!!!!!!!!!!!!!!!!!!!!!!!!!'
		if this_server_mems > oneserver_mems:
			print 'mems of server is out of numbers!'
			print '!!!!!!!!!!!!!!!!!!!!!!!!!!!'

	for key in pre_flavor.keys():       #检查server和预测的总数是否一致
		if server_all_flavor[key] != pre_flavor[key]:
			print 'your numbers of server and pre-flavor are not match!'
			print '!!!!!!!!!!!!!!!!!!!!!!!!!!!'
	
	server_inf = []
	server_inf.append(int(server[0]))
	server_inf.append(server_cpus)
	server_inf.append(server_mems)
	
	return pre_flavor, server_inf

def test_flavors(day1,day2,test_file_array):     #提取测试集中的flavor数
	d1 = datetime.date(int(day1[:4]),int(day1[5:7]),int(day1[8:10]))
	d2 = datetime.date(int(day2[:4]),int(day2[5:7]),int(day2[8:10]))
	flavors = flavor_inial.copy()
	for item in test_file_array:
		values = item.split("\t")
		t = values[2]
		d = datetime.date(int(t[:4]),int(t[5:7]),int(t[8:10]))
		if (d-d1).days >= 0:
			if (d-d2).days < 0:
				flavors[values[1]] += 1
	return flavors
  
def compute_score(testflavors,pre_flavor,server_inf,input_inf):   #计算分数
	oneserver_cpus = input_inf[0]
	oneserver_mems = input_inf[1]
	x_2 = 0
	y_2 = 0
	y_x_2 = 0
	for key,value in pre_flavor.items():
		if value != 0:
			x_2 += testflavors[key] ** 2
			y_2 += pre_flavor[key] ** 2
			y_x_2 += (pre_flavor[key] - testflavors[key]) ** 2
	a = y_x_2 ** 0.5
	b = x_2 ** 0.5
	c = y_2 ** 0.5
	cpu_score = (1 - a / (b + c))*(float(server_inf[1])/oneserver_cpus/server_inf[0])*100
	mem_score = (1 - a / (b + c))*(float(server_inf[2])/oneserver_mems/server_inf[0])*100
	print 'use of cpu:'
	print float(server_inf[1])/oneserver_cpus/server_inf[0]
	print 'use of mem:'
	print float(server_inf[2])/oneserver_mems/server_inf[0]
	return cpu_score,mem_score

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
        
def find_repeat(source,elmt): # The source may be a list or string.
        elmt_index=[]
        s_index = 0;e_index = len(source)
        while(s_index < e_index):
                try:
                    temp = source.index(elmt,s_index,e_index)
                    elmt_index.append(temp)
                    s_index = temp + 1
                except ValueError:
                    break
        return elmt_index


if __name__ == "__main__":
    main()

