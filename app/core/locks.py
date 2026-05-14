import redis


redis_client = redis.Redis(host="redis", port=6379, db=2)


def acquire_lock(key: str, ttl: int = 60) -> bool:
    return redis_client.set(key, "1", nx=True, ex=ttl)

def release_lock(key: str) -> None:
    redis_client.delete(key)
    