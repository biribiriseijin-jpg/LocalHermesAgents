"""
設定ファイル
"""

# Redis接続先
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379

# 利用可能なタスク種別
VALID_TASK_TYPES = {
    "coding",
    "search",
    "research",
    "build",
    "dummy",
}

# Webhook URL
WEBHOOK_URL = (
    "http://localhost:8644/webhooks/task_manager_completed"
)