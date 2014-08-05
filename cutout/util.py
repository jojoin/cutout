#!/usr/bin/python
#-*- coding:utf8 -*-



import sys,re
import urllib.parse as urlparse



## 补全不足
# @side 填充位置 left 
def fillside(stuff,width=None,fill=' ',side='left'):
	if not width or not isinstance(width,int):
		return stuff
	stuff = str(stuff)
	w = len(stuff)
	if w > width:
		return num
	fillstr = fill * (width-w)
	if side = 'left':
		return fillstr+stuff
	elif side = 'right':
		return stuff+fillstr
	else:
		return stuff






## 限定数值范围
def rangable(num,low=None,top=None):
	if low and num<low:
		return low
	elif top and num>top:
		return top
	else:
		return num



## 解析命令行参数 
# @kr 去掉key里的 “-” 符号
def parse_argv(argv, kr='-'):
	#argv = argv[1:] # 去除文件名
	leg = len(argv)
	num = -1
	redict = {}
	#redict = dict( (k,v) for k in arg )
	while True: # 循环获取参数
		num += 1
		if num>=leg: break
		if num%2: continue
		k = argv[num].replace(kr,'')
		v = argv[num+1] if num+1<leg else ''
		redict[k] = v
	return redict



## 将计时器"时:分:秒"字符串转换为秒数间隔
def time2sec(sTime):
	leg = len(sTime)
	if leg<=5: #小时位补齐
		sTime = '0:'+sTime
	p="^([0-9]+):([0-5][0-9]):([0-5][0-9])$"
	cp=re.compile(p)
	try:
		mTime=cp.match(sTime)
	except TypeError:
		return "[InModuleError]:time2sec(sTime) invalid argument type"
	if mTime:
		t = list(map(int,mTime.group(1,2,3)))
		return 3600*t[0]+60*t[1]+t[2]
	else:
		return "[InModuleError]:time2sec(sTime) invalid argument value"


## 将秒数间隔转换为计时器"时:分:秒"字符串
# @fillzero 是否补全0位
# @fillhour 是否补全小时位
def sec2time(iItv,fillzero=True,fillhour=False):
	if type(iItv)==type(1):
		h=int(iItv/3600)
		sUp_h=iItv-3600*h
		m=int(sUp_h/60)
		sUp_m=sUp_h-60*m
		s=int(sUp_m)
		time = (m,s)
		if h>0 or fillhour: time = (h,m,s)
		def fill_zero(num):
			if num<10:
				return '0'+str(num)
			return str(num)
		if not fillzero: fill_zero = str
		return ":".join(map(fill_zero,time))
	else:
		return "[InModuleError]:sec2time(iItv) invalid argument type"


## url编码
def urlencode(stuff) :
	if isinstance(stuff, dict):
		return urlparse.urlencode(stuff)
	elif isinstance(stuff, str):
		return urlparse.quote(stuff)


## url解码
def urldecode(str) :
	return urlparse.unquote(str)


