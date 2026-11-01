"""
Webhook送信共通処理
"""

import requests
from dotenv import load_dotenv
import sys
import os
upper_path = os.path.dirname(os.path.abspath(__file__)) + '../'
sys.path.append(upper_path)

from config import WEBHOOK_URL

load_dotenv(upper_path + '.env')

headers = {
    "X-Webhook-Secret":
        WEBHOOK_SECRET
}


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
            headers=headers,
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