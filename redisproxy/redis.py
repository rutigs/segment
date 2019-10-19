import os
import redis

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

def create_redis_client():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)