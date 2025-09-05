from flask import Blueprint, jsonify
from ..services.contests import fetch_upcoming_contests


contests_bp = Blueprint("contests", __name__)


@contests_bp.get("")
def list_contests():
    contests = fetch_upcoming_contests()
    return jsonify(contests)


