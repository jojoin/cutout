cutout
======

A toolbox for data grabbing and processing in python 3



Introduction
------------

**cutout** is a Python toolbox for data grabbing and processing. This software is still under development, improvement and perfection.


Pre-requisites
--------------

 * Python 3.2+ 
 * import MySQLdb
 


Installation
------------

you can download **cutout** by [click here](https://github.com/yangjiePro/cutout/archive/master.zip), and use it in your code like this:

```python
from cutout import download, cutout
from cutout.common import get_html, get_argv_dict
from cutout.util import sec2time
...
```

Documentation
-------------

read or run the [test.py](https://github.com/yangjiePro/cutout/blob/master/test.py) to get more example. 

to get baidu music pc software download url, like this:

    >>> from cutout import cutout
    >>> para = {} #p aram
    >>> para['url'] = 'http://music.baidu.com/'
    >>> para['start'] = '<a class="downloadlink-pc"'
    >>> para['end'] = '>下载PC版</a>'
    >>> para['dealwith'] = { 'start':'href="', 'rid':'"', 'end':'"' } # get href url
    >>> cutout(**para) # do grab
    'http://qianqian.baidu.com/download/BaiduMusic-12345630.exe'

to create a cache, like this:

    >>> from cutout.cache import FileCache
    >>> c = FileCache('./cache') # set cache dir './cache'
    >>> c.set("foo", "value")
    >>> c.get("foo")
    'value'
    >>> c.get("missing") is None
    True

to create a ProgressBar for download, like this:

    >>> from cutout.cache import FileCache
    >>> bar = ProgressBar(piece_total=1);
    >>> face = { 'sh_piece_division':1024, 'sh_piece_unit':'KB' }
    >>> bar.face(**face)
    >>> download('http://qianqian.baidu.com/download/BaiduMusic-12345630.exe',showBar=bar)
    '[=============================>                    ]  59.23%  14.81%/s  1280.00KB/s  5120.00KB/8644.81KB  00:00:04'

read or run the [test.py](https://github.com/yangjiePro/cutout/blob/master/test.py) to get more example. 

```bash
$ python3 cutout/test.py
```

Author
------

cutout is developed and maintained by Yang Jie (yangjie@jojoin.com).
It can be found here: http://github.com/yangjiePro/cutout

contact way:

* Home : http://jojoin.com/user/1
* Email: yangjie@jojoin.com
* QQ   : 446342398
