"""
Webhook Receiver

責務:
- Workerから結果を受信
- ログ出力
- 将来的なSQLite保存の入口
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class TaskResult(BaseModel):
    task_id: str
    status: str
    summary: str
    task_type: str


@app.post("/task_completed")
async def task_completed(
    result: TaskResult
):
    """
    Workerからの完了通知
    """

    print("\n=== TASK COMPLETED ===")

    print(result.model_dump())

    return {
        "status": "received"
    }
