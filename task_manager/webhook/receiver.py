"""
Webhook Receiver

責務:
- Workerから結果を受信
- ログ出力
- 将来的なSQLite保存の入口
"""

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import sys
import os
upper_path = os.path.dirname(os.path.abspath(__file__)) + '../'
load_dotenv(upper_path + '.env')


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
