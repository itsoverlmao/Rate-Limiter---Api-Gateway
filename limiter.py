import time
import threading


class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill_time = time.time()
        self.lock = threading.Lock()

    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill_time
        new_tokens = (int)(elapsed)
        self.tokens = min(self.capacity, self.tokens + new_tokens)
        self.last_refill_time = now

    def consume(self, tokens=1):
        with self.lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
        
    def get_tokens(self):
        with self.lock:
            self._refill()
            return self.tokens
        
    
    def get_reset_time(self) -> float:
        with self.lock:
            return self.last_refill_time + 1.0


class RateLimiter:
    def __init__(self, capacity, refill_rate):
        self._lock = threading.Lock()
        self.capacity = capacity
        self.refill_rate = refill_rate
        self._buckets: dict[str, TokenBucket] = {}


    def get_bucket(self, key: str) -> TokenBucket:
        with self._lock:
            if key not in self._buckets:
                self._buckets[key] = TokenBucket(self.capacity, self.refill_rate)
            return self._buckets[key]