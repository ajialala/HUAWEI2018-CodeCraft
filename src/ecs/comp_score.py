# coding=utf-8
import datetime

flavor_inial={'flavor1':0,'flavor2':0,'flavor3':0,'flavor4':0,
	'flavor5':0,'flavor6':0,'flavor7':0,'flavor8':0,'flavor9':0,
	'flavor10':0,'flavor11':0,'flavor12':0,'flavor13':0,'flavor14':0,
	'flavor15':0,'flavor22':0,}

def compute_score(testflavors,pre_flavor):   #计算分数
	x_2 = 0
	y_2 = 0
	y_x_2 = 0
	delta = {}
	for key,value in pre_flavor.items():
		x_2 += testflavors[key] ** 2
		y_2 += pre_flavor[key] ** 2
		delta[key] = pre_flavor[key] - testflavors[key]
		y_x_2 += (pre_flavor[key] - testflavors[key]) ** 2
	print '预测误差为：'
	print delta
	print 'Your score is:'
	a = y_x_2 ** 0.5
	b = x_2 ** 0.5
	c = y_2 ** 0.5
	score = (1 - a / (b + c))*100
	return score

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
