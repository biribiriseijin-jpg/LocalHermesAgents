CREATE TABLE IF NOT EXISTS tasks (

    task_id TEXT PRIMARY KEY,

    session_id TEXT,

    chat_id TEXT,

    thread_id TEXT,

    task_type TEXT NOT NULL,

    status TEXT NOT NULL,

    prompt TEXT NOT NULL,

    failure_reason TEXT,

    created_at TEXT NOT NULL,

    started_at TEXT,

    completed_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_tasks_status
ON tasks(status);

CREATE INDEX IF NOT EXISTS idx_tasks_chat
ON tasks(chat_id);


CREATE TABLE IF NOT EXISTS results (

    result_id INTEGER PRIMARY KEY AUTOINCREMENT,

    task_id TEXT NOT NULL,

    status TEXT NOT NULL,

    summary TEXT,

    result_text TEXT,

    created_at TEXT NOT NULL,

    FOREIGN KEY(task_id)
    REFERENCES tasks(task_id)
);