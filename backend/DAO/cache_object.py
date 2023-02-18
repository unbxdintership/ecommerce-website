'''
- declaration of cache objects
'''

import redis


class RedisCache:

    def __init__(self):
        self.redis = redis.Redis(host='redis', port=6379)
