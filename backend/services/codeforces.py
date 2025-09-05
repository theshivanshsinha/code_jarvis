import requests
from datetime import datetime, timezone
from collections import defaultdict


API_BASE = "https://codeforces.com/api"


def _get_json(url: str, params: dict | None = None) -> dict:
    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    if not isinstance(data, dict) or data.get("status") != "OK":
        raise RuntimeError(f"Codeforces API error at {url}")
    return data["result"]


def fetch_user_info(username: str) -> dict:
    result = _get_json(f"{API_BASE}/user.info", {"handles": username})
    return result[0] if isinstance(result, list) and result else result


def fetch_user_submissions(username: str) -> list[dict]:
    # Returns list of submissions (may be large). Limit not supported, returns recent first.
    result = _get_json(f"{API_BASE}/user.status", {"handle": username})
    return result if isinstance(result, list) else []


def build_stats_from_submissions(submissions: list[dict]) -> dict:
    solved_by_problem = set()
    easy = medium = hard = 0
    solved_count = 0
    for s in submissions:
        if s.get("verdict") != "OK":
            continue
        prob = s.get("problem") or {}
        prob_key = f"{prob.get('contestId','')}-{prob.get('index','')}"
        if prob_key in solved_by_problem:
            continue
        solved_by_problem.add(prob_key)
        rating = prob.get("rating") or 0
        if rating <= 1200:
            easy += 1
        elif rating <= 1700:
            medium += 1
        else:
            hard += 1
        solved_count += 1
    return {
        "totalSolved": solved_count,
        "easy": easy,
        "medium": medium,
        "hard": hard,
    }


def build_daily_activity(submissions: list[dict], days: int = 90) -> list[dict]:
    now = datetime.now(timezone.utc)
    start_ts = int((now.timestamp()) - days * 86400)
    counts = defaultdict(int)
    for s in submissions:
        if s.get("verdict") != "OK":
            continue
        ct = s.get("creationTimeSeconds")
        if ct is None or ct < start_ts:
            continue
        day = datetime.fromtimestamp(ct, tz=timezone.utc).date().isoformat()
        counts[day] += 1
    # Build continuous series
    series = []
    for i in range(days):
        day = (now.date()).fromordinal(now.date().toordinal() - (days - 1 - i)).isoformat()
        series.append({"date": day, "count": counts.get(day, 0)})
    return series


def fetch_codeforces_stats(username: str) -> dict:
    info = fetch_user_info(username)
    subs = fetch_user_submissions(username)
    solved = build_stats_from_submissions(subs)
    rating = info.get("rating") or 0
    rank = info.get("rank") or "unrated"
    # Contest count approximation from rating changes requires user.rating, fallback to submissions contests
    try:
        rating_changes = _get_json(f"{API_BASE}/user.rating", {"handle": username})
        contest_count = len(rating_changes)
        max_rating = max((rc.get("newRating", 0) for rc in rating_changes), default=rating)
    except Exception:
        contest_count = 0
        max_rating = rating
    return {
        **solved,
        "rank": str(rank),
        "contestCount": contest_count,
        "rating": int(rating or 0),
        "maxRating": int(max_rating or 0),
        "streak": 0,  # streak requires more logic; keep 0 for now
    }


def fetch_codeforces_daily(username: str, days: int = 90) -> list[dict]:
    subs = fetch_user_submissions(username)
    return build_daily_activity(subs, days=days)


