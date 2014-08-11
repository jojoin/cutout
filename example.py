#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import os, time


from cutout import cutout

datastr = '''
&lthtml&gt
  &lthead&gt
    &lttitle&gthtml网页标题&lt/title&gt
  &lt/head&gt
  &ltbody&gt
     &ltul id="img"&gt
     	&ltli&gt &ltp&gtpic1&lt/p&gt &ltimg src="/img/pic1.jpg" /&gt  &lt/li&gt
     	&ltli&gt &ltp&gtpic2&lt/p&gt &ltimg src="/img/pic2.jpg" /&gt  &lt/li&gt
     	&ltli&gt &ltp&gtpic3&lt/p&gt &ltimg src="/img/pic3.jpg" /&gt  &lt/li&gt
     &lt/ul&gt
  &lt/body&gt
&lt/html&gt
'''

# 获取网页title

title = cutout(
  data=datastr,
  start="&lttitle&gt",
  end="&lt/title&gt"
)
print(title) #  html网页标题

# 获取图片地址

href = cutout(
  data=datastr,
  start="&ltul id=\"img\"&gt",
  end="&lt/ul&gt",
  split="&ltli&gt", #分割
  dealwith=({
    "start":"&ltp&gt", #获取名称
    "end":"&lt/p&gt" 
  },{
    "start":'&ltimg src="', #获取网址
    "rid":'"',
    "end":'"'
  })

)

print(href) #  [['', None], ['pic1', '/img/pic1.jpg'], ['pic2', '/img/pic2.jpg'], ['pic3', '/img/pic3.jpg']]
# 获取的结果数组第一个为  ['', None] 因为以 &ltli&gt 分割时 第一段字符为空




exit(0);


from cutout.cache import FileCache



print('\n\n######## cache缓存测试\n')

print("\n## FileCache 文件缓存测试\n")
key = '缓存键 hash key'
c = FileCache('./cache') #指定缓存目录
c.set(key, ['2w3w','agafd'],10)
g = c.get(key)
print('取回设置的缓存值：'+g[1])



import cutout.util as util



print('\n\n######## util工具类测试')

print('\n## rangable 限定数值范围\n')
print('128  (50-100) => '+str(util.rangable(128,50,100)))
print('32.5 (50.4-100) => '+str(util.rangable(32.5,50.4,100)))
print('32   (50.4-无上限) => '+str(util.rangable(32.5,50.4)))
print('128  (无下限-100) => '+str(util.rangable(128,top=100)))


print('\n##  parse_argv 解析命令行参数\n')
print(
	"['test.py','-k','key','-n','num'] => "
	+str(util.parse_argv(['test.py','-k','key','-n','num']))
	)

print('\n## sec2time  time2sec 时间格式转化\n')
print('1324 => '+util.sec2time(1324))
print('22:04 => '+str(util.time2sec('22:04')))

print('\n## urlencode  urldncode url编码解码\n')
print('中文汉字 => '+util.urlencode('中文汉字'))
print(
	'%E4%B8%AD%E6%96%87%E6%B1%89%E5%AD%97 => '
	+util.urldecode('%E4%B8%AD%E6%96%87%E6%B1%89%E5%AD%97')
	)
print("{'name':'汉字','title':'标题'} => "
	+util.urlencode({'name':'汉字','title':'标题'}))






from cutout import cutout, cutouts, download
from cutout.common import ProgressBar





print('\n\n######## cutout抓取函数')

print('\n##  cutout 抓取百度音乐PC版软件下载地址 http://music.baidu.com\n')
exe_href = cutout(
	url='http://music.baidu.com', #第一步抓取指定内容
	start='<a class="downloadlink-pc"',
	end='>下载PC版</a>',
	dealwith={
		'start':'href="', #第二部抓取 href 链接
		'rid':'"',
		'end':'"'
	}
)
print(exe_href)
print('\n##  url_download 下载 '+exe_href+' 显示下载进度条\n')




#自定义下载进度条
bar = ProgressBar(piece_total=1);
bar.face(
	sh_piece_division=1024, #piece 除法
	sh_piece_unit='KB' #piece 单位
)
download(exe_href,showBar=bar)




print('\n\n######## 多线程数据抓取\n')

urls = []
for i in range(18):
	'''
	urls.append('http://www.tvmao.com/query.jsp?keys=%E6%B9%96%E5%8C%97%E4%BD%93%E8%82%B2')
	urls.append('http://jojoin.com/')
	urls.append('http://codekart.jojoin.com/')
	urls.append('http://docs.codekart.jojoin.com/')
	urls.append('http://v.duole.com/')
	urls.append('http://www.taobao.com/')
	urls.append('http://www.baidu.com/')
	urls.append('http://blog.csdn.net/vah101/article/details/6175406')
	urls.append('http://www.cnblogs.com/wxw0813/archive/2012/09/18/2690694.html')
	urls.append('http://woodpecker.org.cn/diveintopython3/')
	urls.append('http://www.pythonclub.org/python-basic/threading')
	urls.append('http://developer.51cto.com/art/201003/185569.htm')
	'''
	urls.append('http://v.baidu.com/tv/21331.htm')
	#urls.append('')



sti = time.time()
bdata = cutouts(urls=urls)
eti = time.time()
#print(bdata)
print('并发抓取%d个页面：'%len(urls)+'%.2f'%(eti-sti)+'秒\n')

	


bdata = []
sti = time.time()
for u in urls:
	bdata.append(cutout(u))
eti = time.time()
#print(bdata)
print('顺序抓取%d个页面：'%len(urls)+'%.2f'%(eti-sti)+'秒\n')









print('\n\n#### cutout已完成所有测试！！！')



































