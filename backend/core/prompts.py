SCORING_SYSTEM_PROMPT = """Ты — проверяющий решений по обучающим кейсам.
Оценивай строго по рубрике. Верни только валидный JSON по схеме:
{
  "scores": {
    "hard": {"correctness": int, "completeness": int},
    "soft": {"clarity": int, "structure": int}
  },
  "explanations": {
    "correctness": "строка",
    "completeness": "строка",
    "clarity": "строка",
    "structure": "строка"
  },
  "suggestions": [
    {"criterion": "hard.correctness", "tip": "строка"},
    {"criterion": "soft.clarity", "tip": "строка"}
  ]
}
Значения int в диапазоне 0..3 без дробей.
"""

def build_scoring_prompt(rubric: dict, best_answer: str, submission: str) -> str:
    return (
        "RUBRIC:\n" + str(rubric) + "\n\n"
        "BEST_ANSWER:\n" + best_answer + "\n\n"
        "SUBMISSION:\n" + submission + "\n\n"
        "Проанализируй SUBMISSION по RUBRIC с учетом BEST_ANSWER и верни JSON."
    )

QNA_SYSTEM_PROMPT = """Ты — ассистент, который объясняет выставленные оценки по критериям. Коротко и по делу."""
def build_qna_prompt(submission_text: str, explanations: dict, question: str) -> str:
    return (
        f"SUBMISSION:\n{submission_text}\n\n"
        f"EXPLANATIONS:\n{explanations}\n\n"
        f"QUESTION:\n{question}\n\n"
        "Дай краткий ответ, ссылаясь на проблемные места."
    )
