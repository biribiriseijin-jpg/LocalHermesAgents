"""
共通Worker処理
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from common.redis_utils import (
    redis_client,
    create_consumer_group,
)

from common.webhook import (
    send_webhook,
)


class WorkerBase:
    """
    Worker基底クラス

    CodingWorker
    SearchWorker
    BuildWorker
    が継承する
    """

    def __init__(
        self,
        stream_name: str,
        group_name: str,
        consumer_name: str,
    ):

        self.stream_name = stream_name
        self.group_name = group_name
        self.consumer_name = consumer_name

    def process_task(self, task):
        """
        子クラスで実装
        """

        raise NotImplementedError()

    def run(self):

        create_consumer_group(
            self.stream_name,
            self.group_name
        )

        print(
            f"[Worker] Listening {self.stream_name}"
        )

        while True:

            messages = redis_client.xreadgroup(
                groupname=self.group_name,
                consumername=self.consumer_name,
                streams={
                    self.stream_name: ">"
                },
                count=1,
                block=5000,
            )

            if not messages:
                continue

            for _, entries in messages:

                for message_id, payload in entries:

                    try:

                        result = self.process_task(
                            payload
                        )

                        send_webhook(
                            result
                        )

                        redis_client.xack(
                            self.stream_name,
                            self.group_name,
                            message_id
                        )

                    except Exception as e:

                        print(
                            f"[Worker Error] {e}"
                        )