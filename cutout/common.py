#!/usr/bin/python
# -*- coding:utf8 -*-

import urllib
import urllib.request
import urllib.parse
import os.path
import sys
import re
import time

from .util import sec2time, parse_argv


#default_encoding = sys.getfilesystemencoding()
#if default_encoding.lower() == 'ascii':
#	default_encoding = 'utf-8'


# the old function

##ProgressBar 进度条组件
#注释为了方便，把所有“进度条”文字改为“bar”
class ProgressBar:

	def __init__(self
		, piece_total=0 #总数据量
		, label='' #显示在bar之前的title
		, info='' #显示在bar之后的说明
	):
		self.displayed = False #是否已经显示bar
		self.piece_total = piece_total
		self.piece_current = 0
		self.label = label
		self.face() #外观
		self.start() #数据初始化
		self.filtrate = {}

	#设置数据
	def set(self
		, piece_total=0 #bar左边的包裹符号
	):
		if piece_total>0:
			self.piece_total = piece_total

	#设置bar的ui外观
	def face(self
		, ui_wl='[' #bar左边的包裹符号
		, ui_wr=']' #bar右边的包裹符号
		, ui_fn='=' #bar已经完成的部分
		, ui_lk=' ' #bar未完成的部分
		, ui_hd='>' #bar已经完成的部分的头部
		, ui_leg=50 #bar的长度
		, ui_split='  ' #显示项目之间的分割字符
		, it_time=True  #是否显示进度时间
		, it_piece=True  #是否显示进度数量
		, it_percent=True  #是否显示当前百分比
		, it_speed=True   #是否显示速度
		, it_perspeed=True  #是否显示百分比速度
		, sh_piece_division = 1 #piece显示的时候除法
		, sh_piece_unit = ''   #piece显示的单位
	):
		self.ui_wl = ui_wl
		self.ui_wr = ui_wr
		self.ui_fn = ui_fn
		self.ui_lk = ui_lk
		self.ui_hd = ui_hd
		self.ui_leg = ui_leg
		self.ui_split = ui_split
		self.it_time = it_time
		self.it_piece = it_piece
		self.it_percent = it_percent
		self.it_speed = it_speed
		self.it_perspeed = it_perspeed
		self.sh_piece_division = sh_piece_division
		self.sh_piece_unit = sh_piece_unit

	#开始bar（初始化一些数据）
	def start(self):
		self.piece_current = 0 #当前数据量
		self.percent_current = 0 #当前百分比  0～100
		self.start_time = int(time.time()) #bar启动时间
		self.isDone = False

	#进度条数据到达
	# @type 进度的类型 percent:百分比 piece:部分数据
	# @mode 如何修改进度 add:累加 set:设置
	def step(self,step,type="piece",mode="add"):
		if type=='percent':
			if mode=='add':
				self.percent_current += step
			elif type=='percent':
				self.percent_current = step
		elif type=='piece':
			if mode=='add':
				self.piece_current += step
			elif type=='percent':
				self.piece_current = step
			#算百分比
			if self.piece_total > 0:
				self.percent_current = self.piece_current/self.piece_total*100
		#更新显示
		self.update() 
		#判断是否已经完结
		if self.percent_current >= 100:
			self.done() #已经完成

	#更新bar显示
	def update(self):
		if self.isDone:
			return
		self.displayed = True
		percent = self.percent_current
		ui_hd = self.ui_hd
		if percent >= 100:
			percent = 100
			ui_hd = self.ui_fn
		barleg = self.ui_leg - 1
		num_left = int((percent/100) * barleg)
		#print(percent)
		num_right = barleg - num_left
		barstr = (self.ui_fn*num_left
			+ ui_hd
			+ self.ui_lk*num_right
			)
		additiveTime = int(time.time()) - self.start_time
		if additiveTime==0:
			additiveTime = 1
		#print(sec2time(additiveTime))
		barstr = (self.label
			+ self.ui_wl
			+ barstr
			+ self.ui_wr
			)
		#piece格式化字符串
		p_n_f = '%d'
		ui_sp = self.ui_split
		if self.sh_piece_division>1:
			p_n_f = '%.2f'
		if self.it_percent:
			barstr += ui_sp+'%.2f'%percent + '%'
		if self.it_perspeed:
			perspeed = '%.2f'%(percent/additiveTime)
			barstr += ui_sp+perspeed + '%/s'
		if self.it_speed:
			speed = p_n_f%((self.piece_current/self.sh_piece_division)/additiveTime)
			barstr += ui_sp+speed + self.sh_piece_unit + '/s'
		if self.it_piece:
			barstr += (ui_sp+p_n_f%(self.piece_current/self.sh_piece_division)+self.sh_piece_unit
				+'/'+p_n_f%(self.piece_total/self.sh_piece_division)+self.sh_piece_unit)
		if self.it_time:
			barstr += ui_sp+sec2time(additiveTime,fillzero=True,fillhour=True)
		#print(num_left)
		#print(barstr)
		sys.stdout.write('\r'+barstr)
		sys.stdout.flush()

	#数据处理回调
	def filtrate(self,name,callback):
		self.filtrate[name] = callback;

	#进度bar完成，关闭
	def done(self):
		self.isDone = True
		if self.displayed:
			print()
			self.displayed = False





## 命令行映射器
# 从命令行映射到函数
class CommandDirect:

	def __init__(self
		, type='*' #已数组形式解包参数
		, main=None #main函数
	):
		self.maps = {}
		self.type = type
		self.main = main

	## 执行路由
	def __call__(self):
		if not self.main:
			self.direct()
			return
		#调用处理
		param = sys.argv[1:]
		self.callfunc(self.main,param)


	## 添加映射 将命令行参数 映射到函数
	def add(self,name,func):
		self.maps[name] = func


	## 调用处理
	def callfunc(self,func,param):
		if not param:
			func() #无参数
			return 
		tp = self.type
		if '**'==tp:
			param = parse_argv(param) #关键字参数解包
			func(**param)
		elif '*'==tp:
			func(*param)


	## 执行路由
	def direct(self):
		if not sys.argv:
			return
		argv = sys.argv[1:]
		if not argv:
			return
		name = argv[0]
		maps = self.maps
		if not name in maps:
			return
		param = argv[1:]
		#调用处理
		self.callfunc(maps[name],param)


			












if __name__ == "__main__":
	print('###进度条测试')
	bar = ProgressBar(label='Bar: ',total_piece=99);
	bar.face(
		ui_wl='[' #bar左边的包裹符号
		, ui_wr=']' #bar右边的包裹符号
		, ui_fn='=' #bar已经完成的部分
		, ui_lk=' ' #bar未完成的部分
		, ui_hd='>' #bar已经完成的部分的头部
	)
	bar.step(10)
	time.sleep(0.9)
	bar.step(7)
	time.sleep(0.8)
	bar.step(11)
	time.sleep(0.7)
	bar.step(13)
	time.sleep(0.6)
	bar.step(9)
	time.sleep(0.5)
	bar.step(10)
	time.sleep(0.4)
	bar.step(10)
	time.sleep(0.3)
	bar.step(10)
	time.sleep(0.2)
	bar.step(10)
	time.sleep(0.1)
	bar.step(10)













'''




def to_native_string(s):
	if type(s) == unicode:
		return s.encode(default_encoding)
	else:
		return s

def r1(pattern, text):
	m = re.search(pattern, text)
	if m:
		return m.group(1)

def r1_of(patterns, text):
	for p in patterns:
		x = r1(p, text)
		if x:
			return x

def unescape_html(html):
	import xml.sax.saxutils
	html = xml.sax.saxutils.unescape(html)
	html = re.sub(r'&#(\d+);', lambda x: unichr(int(x.group(1))), html)
	return html

def ungzip(s):
	from StringIO import StringIO
	import gzip
	buffer = StringIO(s)
	f = gzip.GzipFile(fileobj=buffer)
	return f.read()

def undeflate(s):
	import zlib
	return zlib.decompress(s, -zlib.MAX_WBITS)

def get_response(url):
	response = urllib2.urlopen(url)
	data = response.read()
	if response.info().get('Content-Encoding') == 'gzip':
		data = ungzip(data)
	elif response.info().get('Content-Encoding') == 'deflate':
		data = undeflate(data)
	response.data = data
	return response

def get_html(url, encoding=None):
	content = get_response(url).data
	if encoding:
		content = content.decode(encoding)
	return content

def get_decoded_html(url):
	response = get_response(url)
	data = response.data
	charset = r1(r'charset=([\w-]+)', response.headers['content-type'])
	if charset:
		return data.decode(charset)
	else:
		return data

def url_save(url, filepath, bar, refer=None):
	headers = {}
	if refer:
		headers['Referer'] = refer
	request = urllib2.Request(url, headers=headers)
	response = urllib2.urlopen(request)
	file_size = int(response.headers['content-length'])
	assert file_size
	if os.path.exists(filepath):
		if file_size == os.path.getsize(filepath):
			if bar:
				bar.done()
			print 'Skip %s: file already exists' % os.path.basename(filepath)
			return
		else:
			if bar:
				bar.done()
			print 'Overwriting', os.path.basename(filepath), '...'
	with open(filepath, 'wb') as output:
		received = 0
		while True:
			buffer = response.read(1024*256)
			if not buffer:
				break
			received += len(buffer)
			output.write(buffer)
			if bar:
				bar.update_received(len(buffer))
	assert received == file_size == os.path.getsize(filepath), '%s == %s == %s' % (received, file_size, os.path.getsize(filepath))

def url_size(url):
	request = urllib2.Request(url)
	request.get_method = lambda: 'HEAD'
	response = urllib2.urlopen(request)
	size = int(response.headers['content-length'])
	return size

def url_size(url):
	size = int(urllib2.urlopen(url).headers['content-length'])
	return size

def urls_size(urls):
	return sum(map(url_size, urls))

class SimpleProgressBar:
	def __init__(self, total_size, total_pieces=1):
		self.displayed = False
		self.total_size = total_size
		self.total_pieces = total_pieces
		self.current_piece = 1
		self.received = 0
	def update(self):
		self.displayed = True
		bar_size = 40
		percent = self.received*100.0/self.total_size
		if percent > 100:
			percent = 100.0
		bar_rate = 100.0 / bar_size
		dots = percent / bar_rate
		dots = int(dots)
		plus = percent / bar_rate - dots
		if plus > 0.8:
			plus = '='
		elif plus > 0.4:
			plus = '-'
		else:
			plus = ''
		bar = '=' * dots + plus
		bar = '{0:>3.0f}% [{1:<40}] {2}/{3}'.format(percent, bar, self.current_piece, self.total_pieces)
		sys.stdout.write('\r'+bar)
		sys.stdout.flush()
	def update_received(self, n):
		self.received += n
		self.update()
	def update_piece(self, n):
		self.current_piece = n
	def done(self):
		if self.displayed:
			print
			self.displayed = False

class PiecesProgressBar:
	def __init__(self, total_size, total_pieces=1):
		self.displayed = False
		self.total_size = total_size
		self.total_pieces = total_pieces
		self.current_piece = 1
		self.received = 0
	def update(self):
		self.displayed = True
		bar = '{0:>3}%[{1:<40}] {2}/{3}'.format('?', '?'*40, self.current_piece, self.total_pieces)
		sys.stdout.write('\r'+bar)
		sys.stdout.flush()
	def update_received(self, n):
		self.received += n
		self.update()
	def update_piece(self, n):
		self.current_piece = n
	def done(self):
		if self.displayed:
			print
			self.displayed = False

class DummyProgressBar:
	def __init__(self, *args):
		pass
	def update_received(self, n):
		pass
	def update_piece(self, n):
		pass
	def done(self):
		pass




def escape_file_path(path):
	path = path.replace('/', '-')
	path = path.replace('\\', '-')
	path = path.replace('*', '-')
	path = path.replace('?', '-')
	return path

def download_urls(urls, title, ext, total_size, output_dir='.', refer=None, merge=True):
	assert urls
	assert ext in ('flv', 'mp4')
	if not total_size:
		try:
			total_size = urls_size(urls)
		except:
			import traceback
			import sys
			traceback.print_exc(file=sys.stdout)
			pass
	title = to_native_string(title)
	title = escape_file_path(title)
	filename = '%s.%s' % (title, ext)
	filepath = os.path.join(output_dir, filename)
	if total_size:
		if os.path.exists(filepath) and os.path.getsize(filepath) >= total_size * 0.9:
			print 'Skip %s: file already exists' % filepath
			return
		bar = SimpleProgressBar(total_size, len(urls))
	else:
		bar = PiecesProgressBar(total_size, len(urls))
	if len(urls) == 1:
		url = urls[0]
		print 'Downloading %s ...' % filename
		url_save(url, filepath, bar, refer=refer)
		bar.done()
	else:
		flvs = []
		print 'Downloading %s.%s ...' % (title, ext)
		for i, url in enumerate(urls):
			filename = '%s[%02d].%s' % (title, i, ext)
			filepath = os.path.join(output_dir, filename)
			flvs.append(filepath)
			#print 'Downloading %s [%s/%s]...' % (filename, i+1, len(urls))
			bar.update_piece(i+1)
			url_save(url, filepath, bar, refer=refer)
		bar.done()
		if not merge:
			return
		if ext == 'flv':
			from flv_join import concat_flvs
			concat_flvs(flvs, os.path.join(output_dir, title+'.flv'))
			for flv in flvs:
				os.remove(flv)
		elif ext == 'mp4':
			from mp4_join import concat_mp4s
			concat_mp4s(flvs, os.path.join(output_dir, title+'.mp4'))
			for flv in flvs:
				os.remove(flv)
		else:
			print "Can't join %s files" % ext

def playlist_not_supported(name):
	def f(*args, **kwargs):
		raise NotImplementedError('Play list is not supported for '+name)
	return f

def script_main(script_name, download, download_playlist=None):
	if download_playlist:
		help = 'python %s.py [--playlist] [-c|--create-dir] [--no-merge] url ...' % script_name
		short_opts = 'hc'
		opts = ['help', 'playlist', 'create-dir', 'no-merge']
	else:
		help = 'python [--no-merge] %s.py url ...' % script_name
		short_opts = 'h'
		opts = ['help', 'no-merge']
	import sys, getopt
	try:
		opts, args = getopt.getopt(sys.argv[1:], short_opts, opts)
	except getopt.GetoptError, err:
		print help
		sys.exit(1)
	playlist = False
	create_dir = False
	merge = True
	for o, a in opts:
		if o in ('-h', '--help'):
			print help
			sys.exit()
		elif o in ('--playlist',):
			playlist = True
		elif o in ('-c', '--create-dir'):
			create_dir = True
		elif o in ('--no-merge'):
			merge = False
		else:
			print help
			sys.exit(1)
	if not args:
		print help
		sys.exit(1)

	for url in args:
		if playlist:
			download_playlist(url, create_dir=create_dir, merge=merge)
		else:
			download(url, merge=merge)


'''

