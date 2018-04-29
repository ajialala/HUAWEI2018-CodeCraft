# coding=utf-8
import sys
import os
import datetime

def diff(b,data):
	result = []
	for i in range(0,b):
		result.append(data[i])
	for value in data[:-b]:
		result.append(data[b] - value)
		b += 1
	return result

def rediff(b,data):
	result = []
	for i in range(0,b):
		result.append(data[i])
	c = 0
	for value in data[b:]:
		result.append(result[c] + value)
		c += 1
	return result
