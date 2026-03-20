import json

import redis

from app.core.config import settings

redis_client = redis.Redis.from_url(
    settings.redis_url,
    decode_responses=True,
)


class RedisCache:
    @staticmethod
    def get(key: str):
        data = redis_client.get(key)
        if data is None:
            return None
        return json.loads(data)

    @staticmethod
    def set(key: str, value: dict | list, ttl: int | None = None):
        redis_client.set(
            key,
            json.dumps(value),
            ex=ttl or settings.REDIS_CACHE_TTL_SECONDS,
        )

    @staticmethod
    def delete(key: str):
        redis_client.delete(key)

    @staticmethod
    def delete_by_pattern(pattern: str):
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
