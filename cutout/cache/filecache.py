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





#class FileSystemCache(BaseCache):
class FileCache(BaseCache):
    """A cache that stores the items on the file system.  This cache depends
    on being the only user of the `cache_dir`.  Make absolutely sure that
    nobody but this cache stores files there or otherwise the cache will
    randomly delete files therein.

    :param cache_dir: the directory where cache files are stored.
    :param threshold: the maximum number of items the cache stores before
                      it starts deleting some.
    :param default_timeout: the default timeout that is used if no timeout is
                            specified on :meth:`~BaseCache.set`.
    :param mode: the file mode wanted for the cache files, default 0600
    """

    #: used for temporary files by the FileSystemCache
    _fs_transaction_suffix = '.__wz_cache'

    def __init__(self, cache_dir, threshold=500, default_timeout=300, mode=0o600):
        BaseCache.__init__(self, default_timeout)
        self._path = cache_dir
        self._threshold = threshold
        self._mode = mode
        if not os.path.exists(self._path):
            os.makedirs(self._path)

    def _list_dir(self):
        """return a list of (fully qualified) cache filenames
        """
        return [os.path.join(self._path, fn) for fn in os.listdir(self._path)
                if not fn.endswith(self._fs_transaction_suffix)]

    def _prune(self):
        entries = self._list_dir()
        if len(entries) > self._threshold:
            now = time()
            for idx, fname in enumerate(entries):
                remove = False
                f = None
                try:
                    try:
                        f = open(fname, 'rb')
                        expires = pickle.load(f)
                        remove = expires <= now or idx % 3 == 0
                    finally:
                        if f is not None:
                            f.close()
                except Exception:
                    pass
                if remove:
                    try:
                        os.remove(fname)
                    except (IOError, OSError):
                        pass

    def clear(self):
        for fname in self._list_dir():
            try:
                os.remove(fname)
            except (IOError, OSError):
                pass

    def _get_filename(self, key):
        hash = md5(key.encode("utf8")).hexdigest()
        return os.path.join(self._path, hash)

    def get(self, key):
        filename = self._get_filename(key)
        try:
            f = open(filename, 'rb')
            try:
                if pickle.load(f) >= time():
                    return pickle.load(f)
            finally:
                f.close()
            os.remove(filename)
        except Exception:
            return None

    def add(self, key, value, timeout=None):
        filename = self._get_filename(key)
        if not os.path.exists(filename):
            self.set(key, value, timeout)

    def set(self, key, value, timeout=None):
        if timeout is None:
            timeout = self.default_timeout
        filename = self._get_filename(key)
        self._prune()
        try:
            fd, tmp = tempfile.mkstemp(suffix=self._fs_transaction_suffix,
                                       dir=self._path)
            f = os.fdopen(fd, 'wb')
            try:
                pickle.dump(int(time() + timeout), f, 1)
                pickle.dump(value, f, pickle.HIGHEST_PROTOCOL)
            finally:
                f.close()
            rename(tmp, filename)
            os.chmod(filename, self._mode)
        except (IOError, OSError):
            pass

    def delete(self, key):
        try:
            os.remove(self._get_filename(key))
        except (IOError, OSError):
            pass
