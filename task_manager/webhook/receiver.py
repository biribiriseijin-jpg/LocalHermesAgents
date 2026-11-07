"""
Webhook Receiver

責務:
- Workerから結果を受信
- ログ出力
- 将来的なSQLite保存の入口
"""

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from task_manager.config import WEBHOOK_SECRET


app = FastAPI()


class TaskResult(BaseModel):
    task_id: str
    status: str
    summary: str
    task_type: str


@app.post("/task_completed")
async def task_completed(
    result: TaskResult,
    x_webhook_secret: str = Header(None),
):
    """
    Workerからの完了通知
    """

    if x_webhook_secret != WEBHOOK_SECRET:

        raise HTTPException(
            status_code=401,
            detail="Invalid secret"
        )

    print("\n=== TASK COMPLETED ===")

    print(result.model_dump())

    return {
        "status": "received"
    }
