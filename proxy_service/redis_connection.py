import redis
pool = redis.ConnectionPool(password='yourpasswd', port=6388)
redis_conn = redis.Redis(connection_pool=pool)
