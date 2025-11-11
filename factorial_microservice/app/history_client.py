import os
import httpx
from typing import Dict

HISTORY_ENABLED = os.getenv("HISTORY_ENABLED", "false").lower() == "true"
HISTORY_BASE_URL = os.getenv("HISTORY_BASE_URL", "")
HISTORY_API_KEY = os.getenv("HISTORY_API_KEY", "")

async def try_send_history(payload: Dict) -> None:
    if not HISTORY_ENABLED or not HISTORY_BASE_URL:
        return
    url = f"{HISTORY_BASE_URL}/api/historial"
    headers = {"Authorization": f"Bearer {HISTORY_API_KEY}"} if HISTORY_API_KEY else {}
    timeout = httpx.Timeout(2.0, connect=2.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            await client.post(url, json=payload, headers=headers)
        except Exception:
            # En un proyecto real, loggear y exponer métricas
            pass
