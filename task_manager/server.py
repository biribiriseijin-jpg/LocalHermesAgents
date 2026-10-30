"""
Task Manager MCP Server

責務:
- Hermesからcreate_taskを受け取る
- Redis Streamsへ投入する
- task_idを返す
"""

import uuid
from datetime import datetime

import redis
from fastmcp import FastMCP

from config import (
    REDIS_HOST,
    REDIS_PORT,
    VALID_TASK_TYPES,
)

# --------------------------------------------------
# MCP Server初期化
# --------------------------------------------------

mcp = FastMCP(
    name="TaskManager"
)

# --------------------------------------------------
# Redis接続
# --------------------------------------------------

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

# --------------------------------------------------
# ユーティリティ
# --------------------------------------------------

def get_stream_name(task_type: str) -> str:
    """
    タスク種別からRedis Stream名を生成する。
    coding  -> coding_stream
    search  -> search_stream
    research -> research_stream
    """
    return f"{task_type}_stream"

# --------------------------------------------------
# MCP Tool
# --------------------------------------------------

@mcp.tool()
def create_task(
    task_type: str,
    prompt: str,
    session_id: str = "default"
) -> dict:

    """
    非同期タスクをキューへ登録する。
    
    Parameters
    ----------
    task_type:
        coding / search / research / build
        
    prompt:
        Workerに渡すタスク内容
        
    session_id:
        Hermes側の会話識別子
        将来的に履歴管理で利用

    Returns
    -------
    task_id:
        発行されたID

    status:
        queued
    """

    # ------------------------------
    # 入力チェック
    # ------------------------------

    if task_type not in VALID_TASK_TYPES:
        return {
            "status": "error",
            "message": (
                f"Unsupported task type: {task_type}"
            )
        }

    # ------------------------------
    # タスクID生成
    # ------------------------------

    task_id = str(uuid.uuid4())

    # ------------------------------
    # Redisへ保存するレコード
    # ------------------------------

    payload = {
        "task_id": task_id,
        "session_id": session_id,
        "task_type": task_type,
        "prompt": prompt,
        "created_at": datetime.utcnow().isoformat()
    }

    # ------------------------------
    # Stream選択
    # ------------------------------

    stream_name = get_stream_name(task_type)

    # ------------------------------
    # Redis Streamsへ投入
    # ------------------------------

    redis_client.xadd(
        stream_name,
        payload
    )

    # ------------------------------
    # Hermesへ返却
    # ------------------------------

    return {
        "task_id": task_id,
        "status": "queued",
        "stream": stream_name
    }

# --------------------------------------------------
# エントリポイント
# --------------------------------------------------

if __name__ == "__main__":
    mcp.run()
