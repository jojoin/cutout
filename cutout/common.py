#encoding:utf-8
'''
You can use this model to get and save your data
Support MySQL database if you installed MySQLdb Python modules
'''
import os
import copy
import MySQLdb

_defaultConfig = {
	'host':'localhost',
	'user':'root',
	'passwd':'',
	'db':'',
	'port':3306,
	'charset': 'utf8',
	'cursorclass':MySQLdb.cursors.DictCursor
}

def set_config(conf):
	global _defaultConfig
	_defaultConfig = conf



def get_db(conf={}):
	global _defaultConfig
	newcon = copy.deepcopy(_defaultConfig)
	for one in conf:
		newcon[one] = conf[one]
	try:
		conn = MySQLdb.connect(
			host=newcon['host'],
			user=newcon['user'],
			passwd=newcon['passwd'],
			db=newcon['db'],
			charset=newcon['charset'],
			cursorclass=newcon['cursorclass'],
			port=newcon['port'])
		conn.set_character_set('utf8')
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1])
		os._exit(0) # error ! ! !
	else:
		return conn


def get_cursor(conn):

	conn.set_character_set('utf8')
	cur = conn.cursor()
	return cur


# 获得格式化的 INSERT INTO 语句
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

# 获得格式化的 UPDATE 语句
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
