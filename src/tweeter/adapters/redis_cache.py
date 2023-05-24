import datetime
import logging
from uuid import UUID

import redis

from tweeter.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()
r = redis.Redis(**settings.get_redis_uri())


def write(tweet_id: UUID, user_id: UUID, content: str, create_dt: datetime.datetime):
    logging.info(f"writing to cache: {tweet_id}")
    r.hset(
        name=f"{user_id}:tweets",
        key=tweet_id,
        value={
            "id": tweet_id,
            "content": content,
            "create_dt": create_dt.isoformat(),
        },
    )


def read(user_id: UUID):
    logging.info(f"reading from cache: {user_id}")
    return r.hgetall(f"{user_id}:tweets").values()
