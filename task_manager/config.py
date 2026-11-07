"""
設定ファイル

"""

import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path.home() / "LocalHermesAgents"
load_dotenv()


# Redis settings
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379

SOCKET_CONNECT_TIMEOUT = 3
SOCKET_TIMEOUT = 3
RETRY_ON_TIMEOUT = True


# Task Types
TASK_TYPES = (
    "coding",
    "search",
    "research",
    "build",
    "dummy",
)


# Task Status
TASK_STATUS_QUEUED = "queued"
TASK_STATUS_RUNNING = "running"
TASK_STATUS_COMPLETED = "completed"
TASK_STATUS_FAILED = "failed"


# Webhook settings
WEBHOOK_URL = ("http://127.0.0.1:8644/webhooks/task_complte")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

WEBHOOK_TIMEOUT = 10
WEBHOOK_RETRY_COUNT = 3


# SQLite Settings
DB_FILE = (
    PROJECT_ROOT
    / "task_manager"
    / "storage"
    / "task_manager.db"
)

SCHEMA_FILE = (
    PROJECT_ROOT
    / "task_manager"
    / "storage"
    / "schema.sql"
)

DB_TIMEOUT = 30
SQLITE_JOURNAL_MODE = "WAL"