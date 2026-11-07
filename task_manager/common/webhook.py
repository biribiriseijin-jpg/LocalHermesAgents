"""
Webhook送信共通処理
"""

import requests
from task_manager.config import (
    WEBHOOK_URL,
    WEBHOOK_SECRET,
    WEBHOOK_TIMEOUT,
    WEBHOOK_RETRY_COUNT,
)


def send_webhook(payload: dict):
    """
    Worker完了時のWebhook送信

    Parameters
    ----------
    payload:
        Webhook送信内容
    """

    try:

        response = requests.post(
            WEBHOOK_URL,
            json=payload,
            timeout=WEBHOOK_TIMEOUT,
        )

        response.raise_for_status()

        print(
            f"[Webhook] sent task={payload.get('task_id')} \n payload={payload}"
        )

    except Exception as e:

        print(
            f"[Webhook Error] {e}"
        )