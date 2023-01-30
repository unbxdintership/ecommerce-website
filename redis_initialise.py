import redis
class redis_initialise():
    def __init__(self):
        self.pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
        self.redis = redis.Redis(connection_pool=self.pool)
    def close_redis():
        return 1