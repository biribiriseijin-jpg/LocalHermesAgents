"""
Dummy Worker
"""

import time
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from common.worker_base import (
    WorkerBase,
)


class DummyWorker(
    WorkerBase
):

    def process_task(
        self,
        task
    ):

        print(
            f"[Dummy] Start {task['task_id']}"
        )

        # ダミー処理
        time.sleep(20)

        return {
            "task_id":
                task["task_id"],

            "task_type":
                "dummy",

            "status":
                "completed",

            "summary":
                "Dummy task completed",
        }


if __name__ == "__main__":

    worker = DummyWorker(
        stream_name="Dummy_stream",
        group_name="Dummy_workers",
        consumer_name="Dummy_1",
    )

    worker.run()