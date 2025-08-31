import json
import os
import time
import requests
from typing import Optional, Tuple
from config import OPENAI_API_KEY, MODEL_NAME, REQUEST_TIMEOUT


OPENAI_API_BASE = "https://api.openai.com/v1/chat/completions"

def _openai_chat(messages, model=MODEL_NAME, timeout=REQUEST_TIMEOUT) -> str:
    if not OPENAI_API_KEY:
        # Мок: если ключа нет — возвращаем фиктивный, но валидный JSON
        return json.dumps({
            "scores": {
                "hard": {"correctness": 2, "completeness": 3},
                "soft": {"clarity": 2, "structure": 2}
            },
            "explanations": {
                "correctness": "Есть общие подходы, но мало чисел.",
                "completeness": "Покрыты основные шаги.",
                "clarity": "Формулировки понятны.",
                "structure": "Есть пункты, но без выводов."
            },
            "suggestions": [
                {"criterion": "hard.correctness", "tip": "Добавьте расчёты и метрики эффекта."},
                {"criterion": "soft.structure", "tip": "В конце сделайте 2–3 вывода."}
            ]
        })

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "temperature": 0.2,
        "messages": messages
    }
    r = requests.post(OPENAI_API_BASE, headers=headers, json=payload, timeout=timeout)
    r.raise_for_status()
    content = r.json()["choices"][0]["message"]["content"]
    return content

def ask_json(system_prompt: str, user_prompt: str, retries: int = 2) -> Tuple[Optional[dict], str]:
    """
    Возвращает (parsed_json_or_none, raw_text).
    Делает пару ретраев, если JSON парсится криво.
    """
    last_text = ""
    for i in range(retries + 1):
        text = _openai_chat([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ])
        last_text = text
        try:
            # В некоторых моделях ответ может содержать ```json ...```
            cleaned = text.strip().strip("`")
            if cleaned.startswith("json"):
                cleaned = cleaned[4:].strip()
            data = json.loads(cleaned)
            return data, text
        except Exception:
            time.sleep(0.8)
            # Ужесточим запрос на последней попытке
            system_prompt += "\nВерни строго валидный JSON без комментариев, без текста вне JSON."
    return None, last_text
