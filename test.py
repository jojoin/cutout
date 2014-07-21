#!/usr/bin/env python
# -*- coding: UTF-8 -*-


# cutout 汇总测试脚本
# 你可以在这里找到工具箱使用的示例
# 或者执行本文件查看效果
# 请留意 print() ， 它给出了详细的提示(注释)




import os, time


from cutout.cache import FileCache
from cutout.cache import MemCache





print('\n\n######## cache缓存测试')

print("\n## FileCache 文件缓存测试\n")
key = '缓存键 hash key'
c = FileCache('./cache') #指定缓存目录
c.set(key, ['2w3w','agafd'],10)
g = c.get(key)
print(g[1])



import cutout.util as util




print('\n\n######## util工具类测试')

print('\n##  rangable 限定数值范围\n')
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






from cutout import cutout, url_download
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
url_download(exe_href,showBar=bar)




print('\n\n#### cutout已完成所有测试！！！')



































