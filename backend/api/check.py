from flask import Blueprint, request, jsonify
from services.checker import check_submission


bp = Blueprint("check", __name__)

@bp.post("/check")
def check():
    payload = request.get_json() or {}
    case_id = payload.get("case_id", "demo-1")
    text = payload.get("text", "").strip()
    if not text:
        return jsonify({"error": "text is required"}), 400
    try:
        result = check_submission(case_id, text)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
