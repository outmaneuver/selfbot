class RateLimiter {
    private lock: Promise<void> | null;
    private retryAfter: number;

    constructor() {
        this.lock = null;
        this.retryAfter = 0;
    }

    async wait(): Promise<void> {
        if (this.lock) {
            await this.lock;
        }
        if (this.retryAfter > Date.now()) {
            await new Promise(resolve => setTimeout(resolve, this.retryAfter - Date.now()));
        }
    }

    updateRateLimit(retryAfter: number): void {
        this.retryAfter = Date.now() + retryAfter;
    }
}

export default RateLimiter;
