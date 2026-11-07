"""
共通Worker処理
"""

from datetime import datetime, UTC

from task_manager.config import (
    TASK_STATUS_COMPLETED,
)

from task_manager.common.redis_utils import (
    redis_client,
    create_consumer_group,
)

from task_manager.common.webhook import (
    send_webhook,
)

from task_manager.storage.task_repository import (
    task_exists,
    mark_running,
    mark_completed,
    mark_failed,
    save_result,
)

from task_manager.storage.models import (
    TaskResult
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
            try:
                messages = redis_client.xreadgroup(
                    groupname=self.group_name,
                    consumername=self.consumer_name,
                    streams={
                        self.stream_name: ">"
                    },
                    count=1,
                    block=5000,
                )
            except Exception as e:
                if type(e).__name__ == "TimeoutError":
                    continue
                else:
                    print(
                        f"[Worker Error] {e}"
                    )
                    exit(1)

            if not messages:
                continue

            for _, entries in messages:

                for message_id, payload in entries:

                    try:
                        #------------------------------
                        # タスク存在チェック
                        #------------------------------

                        task_id = payload["task_id"]
                        if not task_exists(task_id):
                            print(
                                f"[Worker Error] Unknown task {task_id}"
                            )
                            continue


                        # ------------------------------
                        # SQLite処理をマーク
                        # ------------------------------

                        mark_running(
                            task_id
                        )


                        # ------------------------------
                        # タスク処理
                        # ------------------------------

                        result = self.process_task(
                            payload
                        )


                        # ------------------------------
                        # SQLiteに結果を保存
                        # ------------------------------
                        save_result(
                            TaskResult(
                                task_id=task_id,

                                status=TASK_STATUS_COMPLETED,

                                summary=result["summary"],

                                result_text=result.get("result"),

                                created_at=datetime.now(
                                    UTC
                                ).isoformat(),
                            )
                        )

                        mark_completed(
                            task_id
                        )

                        # ------------------------------
                        # Webhook送信
                        # ------------------------------

                        send_webhook(
                            result
                        )

                        # ------------------------------
                        # Redis StreamからACK
                        # ------------------------------

                        redis_client.xack(
                            self.stream_name,
                            self.group_name,
                            message_id
                        )

                    except Exception as e:

                        print(
                            f"[Worker Error] {e}"
                        )

                        mark_failed(
                            task_id,
                            str(e)
                        )

                        redis_client.xack(
                            self.stream_name,
                            self.group_name,
                            message_id
                        )