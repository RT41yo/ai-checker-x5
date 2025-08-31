from core.prompts import QNA_SYSTEM_PROMPT, build_qna_prompt
from core.llm import ask_json


def answer_question(submission_text: str, explanations: dict, question: str) -> str:
    # Здесь нам не нужен JSON — вернём просто текст (через ask_json не обязательно)
    system_prompt = QNA_SYSTEM_PROMPT
    user_prompt = build_qna_prompt(submission_text, explanations, question)
    # Переиспользуем низкоуровневый вызов
    data, raw = ask_json(system_prompt, user_prompt, retries=1)
    # Если модель вернула JSON — достанем поле answer, иначе вернём сырой текст
    if isinstance(data, dict) and "answer" in data:
        return str(data["answer"])
    return raw  # как текст
