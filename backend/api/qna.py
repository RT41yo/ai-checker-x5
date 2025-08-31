from flask import Blueprint, request, jsonify
from services.qna import answer_question


bp = Blueprint("qna", __name__)

@bp.post("/qna")
def qna():
    payload = request.get_json() or {}
    text = payload.get("submission_text", "")
    explanations = payload.get("explanations", {})
    question = payload.get("question", "")
    if not question:
        return jsonify({"error": "question is required"}), 400
    ans = answer_question(text, explanations, question)
    return jsonify({"answer": ans})
