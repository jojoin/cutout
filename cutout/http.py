#!/usr/bin/env python
# -*- coding: UTF-8 -*-


#监听 http 端口 用于返回数据  与其他语言交互


import io
import shutil
import urllib
from http.server import HTTPServer, SimpleHTTPRequestHandler


class MyRequestHandler(SimpleHTTPRequestHandler):
	respondFunc = {}
	def respond(path,func):
		MyRequestHandler.respondFunc[path] = func
		#print(str(MyRequestHandler.respondFunc))

	def do_GET(self):
		self.process(1) #get

	def do_POST(self):
		self.process(2) #post

	##获取 get 和 post 数据
	def get_post_data(self, query):
		get, post = {}, {}
		if query[1]:
			for qp in query[1].split('&'):
				kv = qp.split('=')
				get[kv[0]] = urllib.parse.unquote(kv[1])
		return get, post

	def process(self, type):
		#是否注册了处理程序
		query = urllib.parse.splitquery(self.path)
		path = query[0]
		if not path in self.respondFunc:
			return self.send_error(404, 'File Not Found: %s' % path)
		#获取get和post数据
		get, post = self.get_post_data(query)
		content = self.respondFunc[path](get, post)
		try:
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			if content:
				self.wfile.write(content.encode())
			else:
				self.wfile.write(b'')
			#f.close()
		except IOError:
			self.send_error(500, 'System error : %s' % path)


		'''
		#print(str(self))
		#return
		content = ""
		if type==1:#post方法，接收post参数
			datas = self.rfile.read(int(self.headers['content-length']))
			datas = urllib.unquote(datas).decode("utf-8", 'ignore')#指定编码方式
			datas = transDicts(datas)#将参数转换为字典
			if datas.has_key('data'):
				content = "data:"+datas['data']+"\r\n"
		if '?' in self.path:
			query = urllib.splitquery(self.path)
			action = query[0]
			if query[1]:#接收get参数
				queryParams = {}
				for qp in query[1].split('&'):
					kv = qp.split('=')
					queryParams[kv[0]] = urllib.unquote(kv[1]).decode("utf-8", 'ignore')
					content+= kv[0]+':'+queryParams[kv[0]]+"\r\n"
		#指定返回编码
		enc="UTF-8"
		content = content.encode(enc)
		f = io.BytesIO()
		f.write(content)
		f.seek(0)
		self.send_response(200)
		self.send_header("Content-type", "text/html; charset=%s" % enc)
		self.send_header("Content-Length", str(len(content)))
		self.end_headers()
		shutil.copyfileobj(f,self.wfile)
		'''


##注册处理程序
def respond(path,func):
	MyRequestHandler.respond(path,func)



#服务器是否已经启动
__isstart = False


##启动http服务器
def start(port=3636):
	global __isstart
	if __isstart: return
	httpd = HTTPServer(('127.0.0.1', port), MyRequestHandler)
	httpd.serve_forever() #设置一直监听并接收请求
	__isstart = True

'''
start()

def testfunc(get, post):
	return 'test func'

respond('/test',testfunc)
'''












