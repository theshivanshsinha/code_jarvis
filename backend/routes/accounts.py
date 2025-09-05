from flask import Blueprint, jsonify, request
from ..db import get_db
from ..config import settings
import jwt


accounts_bp = Blueprint("accounts", __name__)


def _get_user_from_auth() -> dict | None:
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.flask_secret, algorithms=["HS256"])
        return payload
    except Exception:
        return None


@accounts_bp.get("")
def get_accounts():
    payload = _get_user_from_auth()
    if not payload:
        return jsonify({"error": "unauthorized"}), 401
    db = get_db()
    user = db.users.find_one({"sub": payload.get("sub")}) or {}
    accounts = user.get("accounts", {})
    return jsonify({"accounts": accounts})


@accounts_bp.post("")
def set_accounts():
    payload = _get_user_from_auth()
    if not payload:
        return jsonify({"error": "unauthorized"}), 401
    body = request.get_json(force=True, silent=True) or {}
    accounts = body.get("accounts", {})
    db = get_db()
    db.users.update_one(
        {"sub": payload.get("sub")},
        {"$set": {
            "sub": payload.get("sub"),
            "email": payload.get("email"),
            "name": payload.get("name"),
            "accounts": accounts,
        }},
        upsert=True,
    )
    return jsonify({"ok": True})


