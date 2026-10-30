"""
Dummy Coding Worker

責務:
- Redis Streamを監視
- タスク受信
- ダミー処理
- ログ表示
"""

import json
import time
import redis

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from config import REDIS_HOST, REDIS_PORT

STREAM_NAME = "coding_stream"

GROUP_NAME = "coding_workers"

CONSUMER_NAME = "worker_1"

# Redis接続

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,

    socket_connect_timeout=3,
    socket_timeout=3,

    retry_on_timeout=True,

    health_check_interval=30
)

def create_group():
    """
    Consumer Group作成

    既に存在する場合は無視
    """

    try:
        r.xgroup_create(
            STREAM_NAME,
            GROUP_NAME,
            id="0",
            mkstream=True
        )

        print(
            f"Created group: {GROUP_NAME}"
        )

    except redis.exceptions.ResponseError:

        print(
            f"Group already exists: {GROUP_NAME}"
        )

def process_task(task):
    """
    ダミー処理

    将来的にはLaguna呼び出しに置換
    """

    print("\n=== TASK RECEIVED ===")

    print(
        json.dumps(
            task,
            indent=2,
            ensure_ascii=False
        )
    )

    # 処理中を再現
    time.sleep(3)

    print(
        f"Task completed: {task['task_id']}"
    )

    return {
        "status": "completed",
        "summary": (
            "Dummy task completed"
        )
    }

def worker_loop():

    create_group()

    print(
        f"Listening on {STREAM_NAME}"
    )

    while True:

        messages = r.xreadgroup(
            groupname=GROUP_NAME,
            consumername=CONSUMER_NAME,
            streams={
                STREAM_NAME: ">"
            },
            count=1,
            block=5000
        )

        if not messages:
            continue

        for _, entries in messages:

            for message_id, payload in entries:

                try:

                    result = process_task(
                        payload
                    )

                    print(
                        f"Result: {result}"
                    )

                    # ACK
                    r.xack(
                        STREAM_NAME,
                        GROUP_NAME,
                        message_id
                    )

                except Exception as e:

                    print(
                        f"ERROR: {e}"
                    )

if __name__ == "__main__":
    worker_loop()
