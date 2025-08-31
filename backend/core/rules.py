def build_recommendations(scores: dict) -> list:
    """
    Простые правила: если критерий < 2 — даём совет.
    """
    out = []
    mapping = {
        "hard.correctness": "Проверьте точность: добавьте источники, расчёты, формулы эффекта.",
        "hard.completeness": "Покройте пропущенные шаги и уточните план внедрения.",
        "soft.clarity": "Упростите формулировки, избегайте воды, используйте конкретику.",
        "soft.structure": "Добавьте структурирование: шаги, заголовки, 2–3 вывода в конце."
    }
    for path, tip in mapping.items():
        part = scores
        for k in path.split("."):
            part = part[k]
        if part < 2:
            out.append({"criterion": path, "tip": tip})
    return out
