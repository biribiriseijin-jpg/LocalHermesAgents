"""
Redis関連ユーティリティ
"""

import redis

from task_manager.config import (
    REDIS_HOST,
    REDIS_PORT,
    SOCKET_CONNECT_TIMEOUT,
    SOCKET_TIMEOUT,
    RETRY_ON_TIMEOUT,
)

pool = redis.ConnectionPool(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
)

redis_client = redis.Redis(
    connection_pool=pool,
    socket_connect_timeout=SOCKET_CONNECT_TIMEOUT,
    socket_timeout=SOCKET_TIMEOUT,
    retry_on_timeout=RETRY_ON_TIMEOUT,
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