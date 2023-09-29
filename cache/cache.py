import redis

from config import CACHE_HOST, CACHE_HOST_PORT, CACHE_PASS


pool = redis.ConnectionPool(host=CACHE_HOST, port=CACHE_HOST_PORT, decode_responses=True, password=CACHE_PASS)


def get_cache_instance():
    return redis.StrictRedis(connection_pool=pool)
