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








class RedisCache(BaseCache):
    """Uses the Redis key-value store as a cache backend.

    The first argument can be either a string denoting address of the Redis
    server or an object resembling an instance of a redis.Redis class.

    Note: Python Redis API already takes care of encoding unicode strings on
    the fly.

    .. versionadded:: 0.7

    .. versionadded:: 0.8
       `key_prefix` was added.

    .. versionchanged:: 0.8
       This cache backend now properly serializes objects.

    .. versionchanged:: 0.8.3
       This cache backend now supports password authentication.

    :param host: address of the Redis server or an object which API is
                 compatible with the official Python Redis client (redis-py).
    :param port: port number on which Redis server listens for connections.
    :param password: password authentication for the Redis server.
    :param default_timeout: the default timeout that is used if no timeout is
                            specified on :meth:`~BaseCache.set`.
    :param key_prefix: A prefix that should be added to all keys.
    """

    def __init__(self, host='localhost', port=6379, password=None,
                 default_timeout=300, key_prefix=None):
        BaseCache.__init__(self, default_timeout)
        if isinstance(host, basestring):
            try:
                import redis
            except ImportError:
                raise RuntimeError('no redis module found')
            self._client = redis.Redis(host=host, port=port, password=password)
        else:
            self._client = host
        self.key_prefix = key_prefix or ''

    def dump_object(self, value):
        """Dumps an object into a string for redis.  By default it serializes
        integers as regular string and pickle dumps everything else.
        """
        t = type(value)
        if t is int or t is long:
            return str(value)
        return '!' + pickle.dumps(value)

    def load_object(self, value):
        """The reversal of :meth:`dump_object`.  This might be callde with
        None.
        """
        if value is None:
            return None
        if value.startswith('!'):
            return pickle.loads(value[1:])
        try:
            return int(value)
        except ValueError:
            # before 0.8 we did not have serialization.  Still support that.
            return value

    def get(self, key):
        return self.load_object(self._client.get(self.key_prefix + key))

    def get_many(self, *keys):
        if self.key_prefix:
            keys = [self.key_prefix + key for key in keys]
        return [self.load_object(x) for x in self._client.mget(keys)]

    def set(self, key, value, timeout=None):
        if timeout is None:
            timeout = self.default_timeout
        dump = self.dump_object(value)
        self._client.setex(self.key_prefix + key, dump, timeout)

    def add(self, key, value, timeout=None):
        if timeout is None:
            timeout = self.default_timeout
        dump = self.dump_object(value)
        added = self._client.setnx(self.key_prefix + key, dump)
        if added:
            self._client.expire(self.key_prefix + key, timeout)

    def set_many(self, mapping, timeout=None):
        if timeout is None:
            timeout = self.default_timeout
        pipe = self._client.pipeline()
        for key, value in _items(mapping):
            dump = self.dump_object(value)
            pipe.setex(self.key_prefix + key, dump, timeout)
        pipe.execute()

    def delete(self, key):
        self._client.delete(self.key_prefix + key)

    def delete_many(self, *keys):
        if not keys:
            return
        if self.key_prefix:
            keys = [self.key_prefix + key for key in keys]
        self._client.delete(*keys)

    def clear(self):
        if self.key_prefix:
            keys = self._client.keys(self.key_prefix + '*')
            if keys:
                self._client.delete(*keys)
        else:
            self._client.flushdb()

    def inc(self, key, delta=1):
        return self._client.incr(self.key_prefix + key, delta)

    def dec(self, key, delta=1):
        return self._client.decr(self.key_prefix + key, delta)
