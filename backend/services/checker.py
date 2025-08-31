import json
from typing import Tuple
from core.prompts import SCORING_SYSTEM_PROMPT, build_scoring_prompt
from core.llm import ask_json
from core.scoring import compute_total
from core.rules import build_recommendations
from config import DATA_CASES_PATH, DATA_RUBRIC_PATH


def _load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _get_case_and_rubric(case_id: str) -> Tuple[dict, dict]:
    cases = _load_json(DATA_CASES_PATH)          # <-- это массив кейсов
    rubrics = _load_json(DATA_RUBRIC_PATH)       # <-- это массив рубрик
    case = next((c for c in cases if c["id"] == case_id), None)
    if not case:
        raise ValueError(f"Unknown case_id: {case_id}")
    rubric_id = case.get("rubric_id")
    rubric = next((r for r in rubrics if r["id"] == rubric_id), None)
    if not rubric:
        raise ValueError(f"Unknown rubric_id: {rubric_id}")
    return case, rubric

def check_submission(case_id: str, submission_text: str) -> dict:
    case, rubric = _get_case_and_rubric(case_id)
    user_prompt = build_scoring_prompt(rubric, case["best_answer"], submission_text)

    data, raw = ask_json(SCORING_SYSTEM_PROMPT, user_prompt, retries=2)
    if not data:
        # fallback "жёсткий" — минимально валидная структура
        data = {
            "scores": {
                "hard": {"correctness": 1, "completeness": 2},
                "soft": {"clarity": 2, "structure": 1}
            },
            "explanations": {
                "correctness": "Не удалось распарсить ответ модели, используем дефолт.",
                "completeness": "—",
                "clarity": "—",
                "structure": "—"
            },
            "suggestions": []
        }

    total = compute_total(data["scores"], rubric["weights"])
    # объединяем советы: из модели + правила
    merged_sugs = data.get("suggestions", []) + build_recommendations(data["scores"])

    return {
        "case_id": case_id,
        "scores": data["scores"],
        "total": total,
        "explanations": data.get("explanations", {}),
        "recommendations": merged_sugs,
        "raw_model": raw  # удобно для отладки; на UI можно не показывать
    }
