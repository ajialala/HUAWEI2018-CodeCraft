# coding=utf-8
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

def place_vm (pre_flavor,input_inf):
	normaliz = pre_flavor.copy()                # 计算每个flavor的均一化
	if input_inf[3] == 'CPU\n':
		for key in pre_flavor.keys():
			normaliz[key] = flavor_mem_format[key] / flavor_cpu_format[key]
	elif input_inf[3] == 'MEM\n':
		for key in pre_flavor.keys():
			normaliz[key] = float(flavor_cpu_format[key]) / flavor_mem_format[key]
	else:
		print 'cpu or mem? wrong!' 
		print '!!!!!!!!!!!!!!!!!!!!!!!!!'
	
	total_cpu = 0                          #计算总的均一化，作为阈值
	total_mem = 0
	for key,value in pre_flavor.items():
		total_cpu += value * flavor_cpu_format[key]
		total_mem += value * flavor_mem_format[key]
	if input_inf[3] == 'CPU\n':
		total_normaliz = float(total_mem) / total_cpu
	elif input_inf[3] == 'MEM\n':
		total_normaliz = float(total_cpu) / total_mem
	else:
		print 'cpu or mem? wrong!' 
		print '!!!!!!!!!!!!!!!!!!!!!!!!!'
	
	sorted_normaliz = []
	sorted_normaliz_values = sorted({}.fromkeys(normaliz.values()).keys())
	for valuel in range(1,len(sorted_normaliz_values)+1):
		sorted_normaliz.append([])
	i = 0
	for value in sorted_normaliz_values:
		temps = []
		for key,value_2 in normaliz.items():
			if value == value_2:
				temps.append(key[6:]) 
		for temp in sorted(temps):
			sorted_normaliz[i].append(['flavor'+str(temp),pre_flavor['flavor'+str(temp)],value])
		i += 1
	
	active = 1
	server_num = 1
	server = []
	this_cpu = []
	this_mem = []
	while active:                             #服务器循环
		this_cpu.append(input_inf[0])         #服务器cpu初始化
		this_mem.append(input_inf[1])         #服务器mem初始化
		server.append([])
		
		if input_inf[3] == 'CPU\n':           #若是cpu最优
			active_1 = 1
			while active_1:
				if float(this_mem[server_num-1]) / this_cpu[server_num-1] >= total_normaliz:
					sorted_normaliz.reverse()
					for sa_value in sorted_normaliz:
						sa_value.reverse()
						flag = 0
						for value in sa_value:
							this_cpu[server_num-1] -= flavor_cpu_format[value[0]]
							this_mem[server_num-1] -= flavor_mem_format[value[0]]
							if this_cpu[server_num-1] > 0:
								if this_mem[server_num-1] > 0:
									server[server_num-1].append(value[0])
									#print value[0]
									if value[1] == 1:
										sa_value.remove(value)
									else:
										value[1] -= 1
									flag = 1
									break
								else:
									this_cpu[server_num-1] += flavor_cpu_format[value[0]]
									this_mem[server_num-1] += flavor_mem_format[value[0]]
							else:
								this_cpu[server_num-1] += flavor_cpu_format[value[0]]
								this_mem[server_num-1] += flavor_mem_format[value[0]]
						sa_value.reverse()
						if flag == 1:
							break
					sorted_normaliz.reverse()
				else:
					for sa_value in sorted_normaliz:
						sa_value.reverse()
						flag = 0
						for value in sa_value:
							this_cpu[server_num-1] -= flavor_cpu_format[value[0]]
							this_mem[server_num-1] -= flavor_mem_format[value[0]]
							if this_cpu[server_num-1] > 0:
								if this_mem[server_num-1] > 0:
									server[server_num-1].append(value[0])
									if value[1] == 1:
										sa_value.remove(value)
									else:
										value[1] -= 1
									flag = 1
									break
								else:
									this_cpu[server_num-1] += flavor_cpu_format[value[0]]
									this_mem[server_num-1] += flavor_mem_format[value[0]]
							else:
								this_cpu[server_num-1] += flavor_cpu_format[value[0]]
								this_mem[server_num-1] += flavor_mem_format[value[0]]
						sa_value.reverse()
						if flag == 1:
							break
				if flag == 0:
					active_1 = 0
			
		elif input_inf[3] == 'MEM\n':
			active_1 = 1
			while active_1:
				if float(this_cpu[server_num-1]) / this_mem[server_num-1] >= total_normaliz:
					sorted_normaliz.reverse()
					for sa_value in sorted_normaliz:
						sa_value.reverse()
						flag = 0
						for value in sa_value:
							this_cpu[server_num-1] -= flavor_cpu_format[value[0]]
							this_mem[server_num-1] -= flavor_mem_format[value[0]]
							if this_cpu[server_num-1] > 0:
								if this_mem[server_num-1] > 0:
									server[server_num-1].append(value[0])
									if value[1] == 1:
										sa_value.remove(value)
									else:
										value[1] -= 1
									flag = 1
									break
								else:
									this_cpu[server_num-1] += flavor_cpu_format[value[0]]
									this_mem[server_num-1] += flavor_mem_format[value[0]]
							else:
								this_cpu[server_num-1] += flavor_cpu_format[value[0]]
								this_mem[server_num-1] += flavor_mem_format[value[0]]
						sa_value.reverse()
						if flag == 1:
							break
					sorted_normaliz.reverse()
				else:
					for sa_value in sorted_normaliz:
						sa_value.reverse()
						flag = 0
						for value in sa_value:
							this_cpu[server_num-1] -= flavor_cpu_format[value[0]]
							this_mem[server_num-1] -= flavor_mem_format[value[0]]
							if this_cpu[server_num-1] > 0:
								if this_mem[server_num-1] > 0:
									server[server_num-1].append(value[0])
									if value[1] == 1:
										sa_value.remove(value)
									else:
										value[1] -= 1
									flag = 1
									break
								else:
									this_cpu[server_num-1] += flavor_cpu_format[value[0]]
									this_mem[server_num-1] += flavor_mem_format[value[0]]
							else:
								this_cpu[server_num-1] += flavor_cpu_format[value[0]]
								this_mem[server_num-1] += flavor_mem_format[value[0]]
						sa_value.reverse()
						if flag == 1:
							break
				if flag == 0:
					active_1 = 0
			
		else:
			print 'cpu or mem? wrong!' 
			print '!!!!!!!!!!!!!!!!!!!!!!!!!'
		
		while [] in sorted_normaliz:
			sorted_normaliz.remove([])
		if len(sorted_normaliz) == 0:
			break
		else:
			server_num += 1
	return server
