import time

import redis

from config import CACHE_HOST, CACHE_HOST_PORT, CACHE_PASS

r = redis.Redis(host=CACHE_HOST, port=CACHE_HOST_PORT, decode_responses=True, password=CACHE_PASS)

r.set('foo', 'bar', ex=1)
print(r.get('foo'))
time.sleep(2)
print(r.get('foo'))
