#!/usr/bin/python
#-*- coding:utf8 -*-


import os


## 递归遍历 获取文件夹大小
def dir_size(path):
	exi = os.path.exists(path)
	if not exi:
		#print('不存在的目录！')
		return None
	size = 0
	for root, dirs, files in os.walk(path):
		size += sum([os.path.getsize(os.path.join(root, name)) for name in files])  
	return size  




