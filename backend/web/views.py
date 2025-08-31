from flask import Blueprint, render_template, request, json
import json
from services.checker import check_submission
from config import DATA_CASES_PATH


bp = Blueprint("web", __name__, template_folder="templates", static_folder="static")

def _load_cases():
    with open(DATA_CASES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@bp.get("/")
def index():
    cases = _load_cases()
    return render_template("index.html", cases=cases)

@bp.post("/preview")
def preview():
    case_id = request.form.get("case_id", "demo-1")
    text = request.form.get("answer", "")
    if not text:
        cases = _load_cases()
        return render_template("index.html", cases=cases, error="Введите ответ")
    result = check_submission(case_id, text)
    return render_template("result.html", result=result)
