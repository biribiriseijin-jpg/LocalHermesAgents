from datetime import datetime, UTC

from task_manager.config import (
    TASK_STATUS_RUNNING,
    TASK_STATUS_COMPLETED,
    TASK_STATUS_FAILED,
)

from task_manager.storage.database import (
    get_db,
)

from task_manager.storage.models import (
    Task,
    TaskResult,
)


# --------------------------------------------------
# DB書き込み
# --------------------------------------------------

def create_task_record(
    task: Task
):
    with get_db() as conn:
        conn.exeute(
            """
            INSERT INTO tasks (

                task_id,

                session_id,
                chat_id,
                thread_id,

                task_type,
                status,

                prompt,

                created_at
            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                task.task_id,

                task.session_id,
                task.chat_id,
                task.thread_id,

                task.task_type,
                task.status,

                task.prompt,

                task.created_at,
            )
        )
        conn.commit()


def mark_running(
    task_id: str
):
    with get_db() as conn:
        conn.exeute(
            """
            UPDATE tasks

            SET
                status = ?,
                started_at = ?

            WHERE task_id = ?
            """,
            (
                TASK_STATUS_RUNNING,
                datetime.now(
                    UTC
                ).isoformat(),
                task_id,
            ),
        )
        conn.commit()


def mark_completed(
    task_id: str
):
    with get_db() as conn:
        conn.exeute(
            """
            UPDATE tasks

            SET
                status = ?,
                completed_at = ?

            WHERE task_id = ?
            """,
            (
                TASK_STATUS_COMPLETED,
                datetime.now(
                    UTC
                ).isoformat(),
                task_id,
            ),
        )
    conn.commit()


def mark_failed(
    task_id: str,
    reason: str,
):
    with get_db() as conn:
        conn.exeute(
            """
            UPDATE tasks

            SET
                status = ?,
                failure_reason = ?,
                completed_at = ?

            WHERE task_id = ?
            """,
            (
                TASK_STATUS_FAILED,
                reason,
                datetime.now(
                    UTC
                ).isoformat(),
                task_id,
            ),
        )
    conn.commit()


def save_result(
    result: TaskResult
):
    with get_db() as conn:
        conn.exeute(
            """
            INSERT INTO results (

                task_id,

                status,

                summary,

                result_text,

                created_at

            )

            VALUES (?, ?, ?, ?, ?)
            """,
            (
                result.task_id,

                result.status,

                result.summary,

                result.result_text,

                result.created_at,
            )
        )
    conn.commit()


# --------------------------------------------------
# DB読み込み
# --------------------------------------------------

def task_exists(
    task_id: str
) -> bool:

    with get_db() as conn:

        row = conn.execute(
            """
            SELECT 1
            FROM tasks
            WHERE task_id = ?
            """,
            (task_id,)
        ).fetchone()

    return row is not None


def get_task(
    task_id: str
) -> Task | None:

    with get_db() as conn:

        row = conn.execute(
            """
            SELECT *
            FROM tasks
            WHERE task_id = ?
            """,
            (task_id,)
        ).fetchone()

    if row is None:
        return None

    return Task(
        task_id=row["task_id"],
        session_id=row["session_id"],
        chat_id=row["chat_id"],
        thread_id=row["thread_id"],
        task_type=row["task_type"],
        status=row["status"],
        prompt=row["prompt"],
        created_at=row["created_at"],
        started_at=row["started_at"],
        completed_at=row["completed_at"],
        failure_reason=row["failure_reason"],
    )


def list_recent_tasks(
    limit: int = 20
):

    with get_db() as conn:

        rows = conn.execute(
            """
            SELECT *
            FROM tasks

            ORDER BY created_at DESC

            LIMIT ?
            """,
            (limit,)
        ).fetchall()

    return rows


def get_failed_tasks():

    with get_db() as conn:

        rows = conn.execute(
            """
            SELECT *
            FROM tasks

            WHERE status = 'failed'

            ORDER BY completed_at DESC
            """
        ).fetchall()

    return rows