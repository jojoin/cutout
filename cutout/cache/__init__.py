# -*- coding: utf-8 -*-


'''
print('测试缓存')

#from .cache import SimpleCache
from cache import FileCache

c = FileCache('./cache')
c.set("foo", "cache_value",10)
print(c.get("foo"))


exit(0)
'''



## 文件系统缓存
from .filecache import FileCache

## 内存缓存
from .memcache import MemCache

## Rides 缓存
from .rediscache import RedisCache

## MemcachedCache 缓存
from .memcachedcache import MemcachedCache









