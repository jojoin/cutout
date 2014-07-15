#!/usr/bin/python
#-*- coding:utf8 -*-



import re
from .common import get_html





#“剪”出数据
def cutout(
		url=None,
		data=None,
		start=0,  #开始位置或字符串
		end=0, #结束位置或字符串
		pure=True,  #是否不包含 start 和 end 字符
		match=False, #正则匹配
		rid=False, # “不包含/排除”的字符
		split=None, #分割为数组
		encoding=None, #编码
		dealwith=None #对“剪”的结果进行再次处理，可递归进行
	):
	if url:
		data = get_html(url,encoding)
	if not data:
		return None
	#正则匹配 match
	if match:
		m = re.search(match, data)
		if m:
			return _dealwith(m.group(),dealwith)
		else:
			return None
	#正则匹配 rid
	if rid:
		match = start+'[^'+rid+']*'+end
		m = re.search(match, data)
		if m:
			restr = m.group()
			if pure:
				restr = restr.replace(start,'').replace(end,'')
			return _dealwith(restr,dealwith)
		else:
			return None
	#字符串搜索
	if end==0:
		end = len(data)
	try: #搜索的字符串是否存在
		if isinstance(end,str):
			len_end = len(end)
			end = data.index(end)
			if not pure: end += len_end;
		if isinstance(start,str):
			len_start = len(start)
			start = data.index(start)
			if pure: start += len_start;
	except:
		return None
	#剪切出数据
	cutstr = data[start:end]
	if split:
		return _dealwith(cutstr.split(split),dealwith)
	else:
		return _dealwith(cutstr,dealwith)

#cutout递归再处理
def _dealwith(data,deal):
	if not deal:
		return data
	if isinstance(data,list):
		relist = []
		for one in data:
			deal['data'] = one;
			one = cutout(**deal)
			relist.append(one)
		return relist
	if isinstance(data,str):
		deal['data'] = data;
		return cutout(**deal)


##过滤HTML中的标签
#将HTML中标签等信息去掉
#@param htmlstr HTML字符串.
def remove_html_tags(htmlstr):
    #先过滤CDATA
    re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
    re_br = re.compile('<br\s*?/?>')#处理换行
    re_h = re.compile('</?\w+[^>]*>')#HTML标签
    re_comment = re.compile('<!--[^>]*-->')#HTML注释
    s = re_cdata.sub('',htmlstr)#去掉CDATA
    s = re_script.sub('',s) #去掉SCRIPT
    s = re_style.sub('',s)#去掉style
    s = re_br.sub('\n',s)#将br转换为换行
    s = re_h.sub('',s) #去掉HTML 标签
    s = re_comment.sub('',s)#去掉HTML注释
    #去掉多余的空行
    blank_line = re.compile('\n+')
    s = blank_line.sub('\n',s)
    #s = recover_html_char_entity(s)#替换实体
    return s



##替换常用HTML字符实体.
def replace_html_char_entity(htmlstr):
	pass


##恢复常用HTML字符实体.
#使用正常的字符替换HTML中特殊的字符实体.
#你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
#@param htmlstr HTML字符串.
def recover_html_char_entity(htmlstr):
    CHAR_ENTITIES={
		'nbsp':' ','160':' ',
		'lt':'<','60':'<',
		'gt':'>','62':'>',
		'amp':'&','38':'&',
		'quot':'"''"','34':'"',
	}
    re_charEntity = re.compile(r'&#?(?P<name>\w+);')
    sz = re_charEntity.search(htmlstr)
    while sz:
        entity = sz.group()#entity全称，如>
        key = sz.group('name')#去除&;后entity,如>为gt
        try:
            htmlstr = re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
            sz = re_charEntity.search(htmlstr)
        except KeyError:
            #以空串代替
            htmlstr = re_charEntity.sub('',htmlstr,1)
            sz = re_charEntity.search(htmlstr)
    return htmlstr




if __name__=='__main__':
	testurl = "http://www.baidu.com"
	print(testurl)
	htmlstr = get_html(testurl,encoding='utf-8')
	print(htmlstr)
	string = remove_html_tags(htmlstr)
	print(string)









