"""
Webhook送信共通処理
"""

import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from config import WEBHOOK_URL


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
            timeout=5
        )

        response.raise_for_status()

        print(
            f"[Webhook] sent task={payload.get('task_id')}"
        )

    except Exception as e:

        print(
            f"[Webhook Error] {e}"
        )