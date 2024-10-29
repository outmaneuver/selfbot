import { LRUCache } from 'cachetools';

class CacheManager {
    private localCache: LRUCache<string, any>;

    constructor() {
        this.localCache = new LRUCache({ maxSize: 1000 });
    }

    fetchFromCache(key: string): any {
        return this.localCache.get(key);
    }

    storeInCache(key: string, value: any): void {
        this.localCache.set(key, value);
    }
}

export default CacheManager;
