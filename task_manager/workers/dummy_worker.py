"""
Dummy Worker
"""

import time
from datetime import datetime, UTC

from task_manager.common.worker_base import (
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
            f"[Dummy] Start {task['task_id']} at {datetime.now(UTC).isoformat()}"
        )

        # ダミー処理
        time.sleep(60)

        print(
            f"[Dummy] Completed {task['task_id']} at {datetime.now(UTC).isoformat()}"
        )

        return {
            "task_id":
                task["task_id"],

            "task_type":
                "dummy",

            "status":
                "completed",

            "summary":
                "Dummy task completed",

            "deliver":
                {
                    "chat_id": task["deliver"]["chat_id"],
                    "thread_id": task["deliver"]["thread_id"]
                }
        }


if __name__ == "__main__":

    worker = DummyWorker(
        stream_name="dummy_stream",
        group_name="dummy_workers",
        consumer_name="dummy_1",
    )

    worker.run()