#encoding:utf-8
__author__ = 'yangjie'



import sys,re

# 将计时器"时:分:秒"字符串转换为秒数间隔
def time2sec(sTime):
    p="^([0-9]+):([0-5][0-9]):([0-5][0-9])$"
    cp=re.compile(p)
    try:
    	mTime=cp.match(sTime)
    except TypeError:
    	return "[InModuleError]:time2itv(sTime) invalid argument type"
    if mTime:
		t=map(int,mTime.group(1,2,3))
		return 3600*t[0]+60*t[1]+t[2]
    else:
    	return "[InModuleError]:time2itv(sTime) invalid argument value"


# 将秒数间隔转换为计时器"时:分:秒"字符串
# @fillzero 是否补全0位
# @fillhour 是否补全小时位
def sec2time(iItv,fillzero=True,fillhour=False):
	if type(iItv)==type(1):
		h=iItv/3600
		sUp_h=iItv-3600*h
		m=sUp_h/60
		sUp_m=sUp_h-60*m
		s=sUp_m
		time = (m,s)
		if h>0 or fillhour: time = (h,m,s)
		def fill_zero(num):
			if num<10:
				return '0'+str(num)
			return str(num)
		if not fillzero: fill_zero = str
		return ":".join(map(fill_zero,time))
	else:
		return "[InModuleError]:itv2time(iItv) invalid argument type"

