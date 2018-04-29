# coding=utf-8
import sys
import os
import datetime
import math
import numpy as np
import matplotlib.pyplot as plt

import predictor
import place
import get_data
import diff
import arma_math
import arma
import ecs

print 'main function begin.'
if len(sys.argv) != 4:
	print 'parameter is incorrect!'
	print 'Usage: python esc.py ecsDataPath inputFilePath resultFilePath'
	exit(1)
# Read the input files
ecsDataPath = sys.argv[1]
inputFilePath = sys.argv[2]
resultFilePath = sys.argv[3]

ecs_infor_array = ecs.read_lines(ecsDataPath)
everyday_flavor = get_data.get_everyday_flavor(ecs_infor_array)
input_file_array = ecs.read_lines(inputFilePath)
input_inf = ecs.read_input(input_file_array)
data = everyday_flavor['flavor5']
data = [608,617,625,636,657,691,728,784,816,876,949,997,1027,1047,
		1049,1018,1021,1012,1018,991,962,921,871,829,822,820,802,821,
		819,791,746,726,661,620,588,568,542,551,541,557,556,534,528,
		529,523,531]
data = [41.5,59.5,64.6,80.9,84.7,109.8,108.7,104.5,128.7,149.3,128.4,
		90.7,80.9,85.7,97.5,118.4,127.1,112.2,108.5,107.7,112.9,120.9,
		146.9,220.5,292.2,290.4,264.1,272.5,355,454.6,570,735.3,771.3,
		860.1,1201,2066.7,2580.4,3084.2,3821.8,4155.9,5560.1,7225.8,
		9119.6,11271,20381.9,23499.9,24133.8,26967.2,26854.1,26896.3,
		39273.2,42183.6,51378.2,70483.5,95539.1,116921.8]
data = [603.2225,636.8149,707.1452,638.0379,620.6295,707.2703,539.0789,
		252.8602,591.7836,626.9935,582.6923,611.3965,612.8499,645.9645,
		715.9899,646.1702,628.2095,717.1703,549.4425,
		259.8826,601.1425,637.4908,592.8298,620.8653,620.2722,655.7020,
		723.8026,654.8081,636.0499,725.7692,557.4150,270.9799,611.3857,
		646.0962,602.6265,630.0778,629.6026,663.0500,733.8522,664.6104,
		645.5190,735.4458,566.1298,279.3648,620.6696,654.9507,611.4662,
		637.0239,640.5817,672.2036,743.0334,675.1520,655.5609,741.9791,
		573.6024,288.2158,627.7034,663.0892,620.7718,647.4319]
def predict_ar(day,data):
	firsr_order = 12
	second_order = 1
	temp1 = data[0:firsr_order]
	data = diff.diff(firsr_order,data)
	data = diff.diff(second_order,data[firsr_order:])
	meandata = arma_math.mean_value(data)
	data = arma.decent(meandata,data)
	phi = arma.AR(data[second_order:])

	for i in range(0,day):
		j = -1
		tem_sum = 0
		for value in phi:
			tem_sum += value[0] * data[j]
			j -= 1
		data.append(tem_sum)
		
	data = arma.cent(meandata,data)
	data = diff.rediff(second_order,data)
	data = diff.rediff(firsr_order,temp1+data)
	return round(data[-1],4)
#data = map(math.log,data)
#data = arma.decent(meandata,data)

data = everyday_flavor['flavor8']
plt.plot(data)
a=[[1,2,3],[2,2,1],[3,4,3]]
temp1 = data[0:12]
data = diff.diff(7,data)
temp2 = data[0:1]
data = diff.diff(1,data[7:])
#plt.plot(data[1:])
p = []
k = 24
for i in range(0,k+1):
	p.append(arma_math.p_k(i,data[1:]))
h = []
k = 24
for i in range(1,k+1):
	h.append(arma_math.h2(i,data[1:]))
#print data
#print arma.least_squ(2,data[1:])
#print h
#data = diff.rediff(1,data)
#data = diff.rediff(12,temp1+data)
#plt.plot(data[1:])
plt.show()
