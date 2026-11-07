from dataclasses import dataclass

@dataclass
class Task:

    task_id: str

    session_id: str

    chat_id: str

    thread_id: str

    task_type: str

    status: str

    failure_reason: str | None = None

    prompt: str

    created_at: str

    started_at: str | None = None

    completed_at: str | None = None


@dataclass
class TaskResult:

    task_id: str

    status: str

    summary: str

    result_text: str

    created_at: str
