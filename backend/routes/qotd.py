from flask import Blueprint, jsonify
from ..services.qotd_service import qotd_service

qotd_bp = Blueprint("qotd", __name__)

@qotd_bp.get("")
def get_question_of_the_day():
    """Get daily questions from all platforms"""
    try:
        questions = qotd_service.get_daily_questions()
        motivation = qotd_service.get_motivational_message()
        difficulty_stats = qotd_service.get_difficulty_stats(questions)
        
        return jsonify({
            "questions": questions,
            "motivation": motivation,
            "difficulty_stats": difficulty_stats,
            "total_questions": len(questions),
            "platforms": [q["platform"] for q in questions],
            "message": "Fresh problems picked just for you!"
        })
    except Exception as e:
        return jsonify({"error": f"Failed to get daily questions: {str(e)}"}), 500

@qotd_bp.get("/platform/<platform>")
def get_platform_question(platform):
    """Get question of the day for a specific platform"""
    try:
        questions = qotd_service.get_daily_questions()
        platform_question = next((q for q in questions if q["platform"] == platform), None)
        
        if not platform_question:
            return jsonify({"error": f"No question available for {platform} today"}), 404
        
        return jsonify({
            "question": platform_question,
            "motivation": qotd_service.get_motivational_message()
        })
    except Exception as e:
        return jsonify({"error": f"Failed to get {platform} question: {str(e)}"}), 500

@qotd_bp.get("/refresh")
def refresh_questions():
    """Refresh the daily questions cache"""
    try:
        # Clear cache to force refresh
        from datetime import datetime
        today = datetime.now().date().isoformat()
        if today in qotd_service.cache:
            del qotd_service.cache[today]
        
        questions = qotd_service.get_daily_questions()
        return jsonify({
            "questions": questions,
            "message": "Questions refreshed successfully!",
            "total_questions": len(questions)
        })
    except Exception as e:
        return jsonify({"error": f"Failed to refresh questions: {str(e)}"}), 500
