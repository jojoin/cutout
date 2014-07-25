#!/usr/bin/python
# -*- coding:utf8 -*-

'''
You can use this model to get and save your data
Support MySQL database if you installed PyMySQL Python modules
'''


import os
import copy
import time
import pymysql


''' cursor 类型
pymysql.cursors.Cursor
pymysql.cursors.SSCursor 
pymysql.cursors.DictCursor
pymysql.cursors.SSDictCursor
'''

#conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='mysql')


## 默认的数据库连接配置
_dbConfig = {
	'host':'localhost',
	'user':'root',
	'passwd':'',
	'db':'',
	'port':3306,
	'charset': 'utf8'
}


## 连接池
_connects = {
	#'default':{
	#	'name':'default',
	#	'connect':None, #连接
	#	'config':{},
	#	'timevalid':0 #有效时间截止
	#}
}


## 当前上下文连接
_curcon = None


## 配置
_config = {
	'connect_timeout': 3600, #链接过期时间 1小时
	'cursor_type':pymysql.cursors.Cursor # 游标风格
}



## 设置额外配置
def setconf(**conf):
	global _config
	for (k,v) in conf.items():
		_config[k] = v
	#cursor_type
	ct = 'cursor_type'
	if ct in conf:
		cct = conf[ct]
		if cct=='ss':
			_config[ct] = pymysql.cursors.SSCursor
		elif cct=='dict':
			_config[ct] = pymysql.cursors.DictCursor
		elif cct=='ssdict':
			_config[ct] = pymysql.cursors.SSDictCursor
		else:
			_config[ct] = pymysql.cursors.Cursor



## 获得数据库连接
# @param conf 数据库配置
# @param reset 覆盖(重设)默认数据库连接
# @param name 把数据库链接缓存起来，或者获取被缓存的链接
def connect(dbconf=None, reset=None, name='default', timeout=3600):
	global _connects, _curcon, _config
	con = None
	# 新连接
	if dbconf:
		for (k,v) in _dbConfig.items():
			if not k in dbconf:
				dbconf[k] = v
		con = pymysql.connect(**dbconf)
	# 读取缓存的连接
	if not dbconf and name:
		conn = _connects[name]
		tiv = conn['timevalid']
		ti = int(time.time())
		if(ti>=tiv): # 重新激活连接
			dbconf = conn['config']
			conn['connect'].close()
			conn['connect'] = pymysql.connect(**dbconf)
			conn['timevalid'] = ti+timeout
		con = conn['connect']
	# 缓存新的连接
	if dbconf and name:
		ti = int(time.time())
		_connects[name] = {
			'name': name,
			'connect': con,
			'config': dbconf,
			'timevalid': ti+timeout
		}
	# 设置默认连接
	if reset or not _curcon:
		_curcon = name
	# 返回连接
	return con



## 断开连接
def disconnect(name='default'):
	global _connects
	if name in _connects:
		_connects[name]['connect'].close()
		del _connects[name]



## 获得数据库操作游标
def cursor(type=None):
	global _connects, _curcon, _config
	if type:
		return _connects[_curcon]['connect'].cursor(type)
	else:
		return _connects[_curcon]['connect'].cursor(_config['cursor_type'])
	



# 以下查询接口 使用者必须调用
# cur.close()



## 执行sql语句
def query(sql, cursor_type=None):
	cur = cursor(cursor_type=None)
	cur.execute(sql)
	return cur



## 查询
# @param cursor=None 返回查询的list数组
#        cursor=True 直接返回cursor
def select(table, field='*', where='', limit='', orderby='', cursor=None):

	sql = ''

	return query(sql)







## 获得格式化的 INSERT INTO 语句
def fixsql_insert(table,field):
	na=[]
	var = []
	for f in field:
		na.append(f)
		var.append('%('+f+')s')
	return ('INSERT INTO '+table+' ('
		+(','.join(na))
		+') VALUE ('
		+(','.join(var))
		+')')



## 获得格式化的 UPDATE 语句
def fixsql_update(table,field,where='',limit=''):
	var = []
	for f in field:
		var.append(f+'=%('+f+')s')
	sql = 'UPDATE '+table+' SET '+(','.join(var))
	if where:
		sql += 'WHERE '+where
	if limit:
		sql += ' LIMIT '+limit
	return sql




## 单元测试
def main():
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='mysql')
	cur = conn.cursor(pymysql.cursors.DictCursor)
	#cur = conn.cursor()
	cur.execute("SELECT Host,User FROM user")
	print(cur.description)
	print(cur.rowcount)
	print(repr(cur))
	for row in cur:
	   print(row)
	cur.close()
	conn.close()


if __name__ == '__main__':
	main()
