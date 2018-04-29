# coding=utf-8
import sys
import os
import predictor
import place
import get_data
import comp_score
import knapsack

def main():
	print 'main function begin.'
	if len(sys.argv) != 5:
		print 'parameter is incorrect!'
		print 'Usage: python esc.py ecsDataPath inputFilePath resultFilePath'
		exit(1)
	# Read the input files
	ecsDataPath = sys.argv[1]
	inputFilePath = sys.argv[2]
	resultFilePath = sys.argv[3]
	testFilePath = sys.argv[4]

	ecs_infor_array = read_lines(ecsDataPath)
	everyday_flavor = get_data.get_everyday_flavor(ecs_infor_array)
	input_file_array = read_lines(inputFilePath)
	input_inf = read_input(input_file_array)
	print input_inf[3]
	test_file_array = read_lines(testFilePath)
	testflavors = comp_score.test_flavors(input_inf[-2],input_inf[-1],test_file_array)
	pre_flavor = {}
	for value in input_inf[2]:
		flavor_list = everyday_flavor[value]
		predic_result = predictor.predict_ar(ecs_infor_array[-1],input_inf[-2],input_inf[-1],flavor_list)
		pre_flavor[value] = predic_result
	print pre_flavor
	print comp_score.compute_score(testflavors,pre_flavor)
	place = knapsack.package_dyn(input_inf[3],pre_flavor,input_inf[4],input_inf[5],input_inf[0],input_inf[1])
	predic_result = []
	predic_result.append(0)
	sum_flavor = 0
	for key,value in pre_flavor.items():
		sum_flavor += value
		predic_result.append(key + ' ' + str(int(value)))
	predic_result[0] = int(sum_flavor)
	predic_result.append('')
	predic_result.append(place[0])
	for server in sorted(place[1].keys()):
		this_server = str(server)
		for key,value in place[1][server].items():
			this_server += ' '
			this_server += key
			this_server += ' '
			this_server += str(value)
		predic_result.append(this_server)
	# write the result to output file
	if len(predic_result) != 0:
		write_result(predic_result, resultFilePath)
	else:
		predic_result.append("NA")
		write_result(predic_result, resultFilePath)
	print 'main function end.'

def write_result(array, outpuFilePath):
	with open(outpuFilePath, 'w') as output_file:
		for item in array:
			output_file.write("%s\n" % item)

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

def read_input(input_array):           #读取输入信息
	server = input_array[0].split(" ")
	oneserver_cpus = int(server[0])
	oneserver_mems = int(server[1])
	flavor_num = int(input_array[2])
	cpu_or_mem = input_array[4+flavor_num][:3]
	start_time = input_array[6+flavor_num]
	end_time = input_array[7+flavor_num]
	need_flavor = []
	flavor_cpu_format = {}
	flavor_mem_format = {}
	for item in input_array[3:3+flavor_num]:
		need_flavor_format = item.split(' ')
		need_flavor.append(need_flavor_format[0])
		flavor_cpu_format[need_flavor_format[0]] = int(need_flavor_format[1])
		flavor_mem_format[need_flavor_format[0]] = int(int(need_flavor_format[2]) / 1024)
	value = [oneserver_cpus,oneserver_mems,need_flavor,cpu_or_mem,
			flavor_cpu_format,flavor_mem_format,start_time,end_time]
	return value

if __name__ == "__main__":
	main()
