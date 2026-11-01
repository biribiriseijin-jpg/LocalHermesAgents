"""
Redis関連ユーティリティ
"""

import redis
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from config import (
    REDIS_HOST,
    REDIS_PORT,
)

pool = redis.ConnectionPool(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
)

redis_client = redis.Redis(
    connection_pool=pool
)


def create_consumer_group(
    stream_name: str,
    group_name: str
):
    """
    Consumer Group作成
    """

    try:

        redis_client.xgroup_create(
            stream_name,
            group_name,
            id="0",
            mkstream=True
        )

        print(
            f"[Redis] Created group {group_name}"
        )

    except redis.exceptions.ResponseError:

        print(
            f"[Redis] Group exists {group_name}"
        )