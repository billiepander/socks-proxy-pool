import redis
pool = redis.ConnectionPool(password='pdREDIS123', port=6388)
redis_conn = redis.Redis(connection_pool=pool)
