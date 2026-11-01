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
    Create a background task for long-running work.

    Use this tool when the request requires substantial processing,
    external investigation, code generation, repository analysis,
    build execution, or any task that may take more than a few seconds.

    Typical use cases:
    - Writing or refactoring code
    - Reviewing large codebases
    - Research tasks
    - Web searches and information gathering
    - Build or test execution
    - Multi-step analysis

    Do NOT use this tool for:
    - Normal conversation
    - Simple explanations
    - Short answers that can be generated immediately
    - Questions that can be answered directly from existing context

    After creating a task:
    - The task will be executed asynchronously.
    - A task_id will be returned immediately.
    - Results will become available later through the task system.
    - Do not wait for task completion before responding to the user.

    Important:
    When a user requests code generation,
    repository analysis,
    research,
    search,
    build,
    test,
    or automation tasks,
    prefer create_task instead of performing the work directly.

    The user experience should be:
    1. Create background task.
    2. Inform the user that the task has been queued.
    3. Continue the conversation without blocking.

    This tool exists to keep interactive conversations responsive while
    delegating expensive work to background workers.

    Parameters:
        task_type:
            Type of work to perform.
            Valid values:
            - coding
            - search
            - research
            - build

        prompt:
            Complete description of the work to perform.
            Include all relevant requirements and constraints.

        session_id:
            Identifier for the current conversation session.

    Returns:
        task_id:
            Unique identifier for the queued task.

        status:
            Queue status, usually 'queued'.

    Decision guideline:

    Use create_task whenever:
    - Expected execution time exceeds a few seconds.
    - Specialized worker processing is required.
    - The task can continue independently of the current conversation.

    Prefer direct responses whenever:
    - The answer can be produced immediately.
    - No external processing is required.
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
