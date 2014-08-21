#!/usr/bin/python
#-*- coding:utf8 -*-


import os


## 递归遍历 获取文件夹大小
def dir_size(dir):  
	size = 0L
	for root, dirs, files in os.walk(dir):  
		size += sum([os.path.getsize(os.path.join(root, name)) for name in files])  
	return size  




