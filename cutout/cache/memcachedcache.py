# -*- coding: utf-8 -*-




import os
import re
import tempfile
from time import time
from .basecache import BaseCache
from .posixemulation import rename, _items
try:
    import cPickle as pickle
except ImportError:
    import pickle
try:
    from hashlib import md5
except ImportError:
    from md5 import new as md5



_test_memcached_key = re.compile(r'[^\x00-\x21\xff]{1,250}$').match

class MemcachedCache(BaseCache):
    """A cache that uses memcached as backend.

    The first argument can either be an object that resembles the API of a
    :class:`memcache.Client` or a tuple/list of server addresses. In the
    event that a tuple/list is passed, Werkzeug tries to import the best
    available memcache library.

    Implementation notes:  This cache backend works around some limitations in
    memcached to simplify the interface.  For example unicode keys are encoded
    to utf-8 on the fly.  Methods such as :meth:`~BaseCache.get_dict` return
    the keys in the same format as passed.  Furthermore all get methods
    silently ignore key errors to not cause problems when untrusted user data
    is passed to the get methods which is often the case in web applications.

    :param servers: a list or tuple of server addresses or alternatively
                    a :class:`memcache.Client` or a compatible client.
    :param default_timeout: the default timeout that is used if no timeout is
                            specified on :meth:`~BaseCache.set`.
    :param key_prefix: a prefix that is added before all keys.  This makes it
                       possible to use the same memcached server for different
                       applications.  Keep in mind that
                       :meth:`~BaseCache.clear` will also clear keys with a
                       different prefix.
    """

    def __init__(self, servers=None, default_timeout=300, key_prefix=None):
        BaseCache.__init__(self, default_timeout)
        if servers is None or isinstance(servers, (list, tuple)):
            if servers is None:
                servers = ['127.0.0.1:11211']
            self._client = self.import_preferred_memcache_lib(servers)
            if self._client is None:
                raise RuntimeError('no memcache module found')
        else:
            # NOTE: servers is actually an already initialized memcache
            # client.
            self._client = servers

        self.key_prefix = key_prefix

    def get(self, key):
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if self.key_prefix:
            key = self.key_prefix + key
        # memcached doesn't support keys longer than that.  Because often
        # checks for so long keys can occour because it's tested from user
        # submitted data etc we fail silently for getting.
        if _test_memcached_key(key):
            return self._client.get(key)

    def get_dict(self, *keys):
        key_mapping = {}
        have_encoded_keys = False
        for key in keys:
            if isinstance(key, unicode):
                encoded_key = key.encode('utf-8')
                have_encoded_keys = True
            else:
                encoded_key = key
            if self.key_prefix:
                encoded_key = self.key_prefix + encoded_key
            if _test_memcached_key(key):
                key_mapping[encoded_key] = key
        d = rv = self._client.get_multi(key_mapping.keys())
        if have_encoded_keys or self.key_prefix:
            rv = {}
            for key, value in d.iteritems():
                rv[key_mapping[key]] = value
        if len(rv) < len(keys):
            for key in keys:
                if key not in rv:
                    rv[key] = None
        return rv

    def add(self, key, value, timeout=None):
        if timeout is None:
            timeout = self.default_timeout
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if self.key_prefix:
            key = self.key_prefix + key
        self._client.add(key, value, timeout)

    def set(self, key, value, timeout=None):
        if timeout is None:
            timeout = self.default_timeout
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if self.key_prefix:
            key = self.key_prefix + key
        self._client.set(key, value, timeout)

    def get_many(self, *keys):
        d = self.get_dict(*keys)
        return [d[key] for key in keys]

    def set_many(self, mapping, timeout=None):
        if timeout is None:
            timeout = self.default_timeout
        new_mapping = {}
        for key, value in _items(mapping):
            if isinstance(key, unicode):
                key = key.encode('utf-8')
            if self.key_prefix:
                key = self.key_prefix + key
            new_mapping[key] = value
        self._client.set_multi(new_mapping, timeout)

    def delete(self, key):
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if self.key_prefix:
            key = self.key_prefix + key
        if _test_memcached_key(key):
            self._client.delete(key)

    def delete_many(self, *keys):
        new_keys = []
        for key in keys:
            if isinstance(key, unicode):
                key = key.encode('utf-8')
            if self.key_prefix:
                key = self.key_prefix + key
            if _test_memcached_key(key):
                new_keys.append(key)
        self._client.delete_multi(new_keys)

    def clear(self):
        self._client.flush_all()

    def inc(self, key, delta=1):
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if self.key_prefix:
            key = self.key_prefix + key
        self._client.incr(key, delta)

    def dec(self, key, delta=1):
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if self.key_prefix:
            key = self.key_prefix + key
        self._client.decr(key, delta)

    def import_preferred_memcache_lib(self, servers):
        """Returns an initialized memcache client.  Used by the constructor."""
        try:
            import pylibmc
        except ImportError:
            pass
        else:
            return pylibmc.Client(servers)

        try:
            from google.appengine.api import memcache
        except ImportError:
            pass
        else:
            return memcache.Client()

        try:
            import memcache
        except ImportError:
            pass
        else:
            return memcache.Client(servers)


# backwards compatibility
GAEMemcachedCache = MemcachedCache

