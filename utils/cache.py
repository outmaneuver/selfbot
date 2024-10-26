import cachetools

class CacheManager:
    def __init__(self):
        self.local_cache = cachetools.LRUCache(maxsize=1000)

    def fetch_from_cache(self, key):
        return self.local_cache.get(key)

    def store_in_cache(self, key, value):
        self.local_cache[key] = value
