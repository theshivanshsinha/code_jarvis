import requests
from datetime import datetime, timezone
from collections import defaultdict


RESULTS_API = "https://kenkoooo.com/atcoder/atcoder-api/results"
USER_INFO_API = "https://kenkoooo.com/atcoder/atcoder-api/v3/user/info"
PROBLEM_MODELS = "https://kenkoooo.com/atcoder/resources/problem-models.json"


def _get_json(url: str, params: dict | None = None) -> dict | list:
    resp = requests.get(url, params=params, timeout=20)
    resp.raise_for_status()
    return resp.json()


def fetch_user_results(username: str) -> list[dict]:
    data = _get_json(RESULTS_API, {"user": username})
    return data if isinstance(data, list) else []


def fetch_user_info(username: str) -> dict:
    # Contains current rating and highest rating
    try:
        data = _get_json(USER_INFO_API, {"user": username})
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def fetch_problem_models() -> dict:
    try:
        data = _get_json(PROBLEM_MODELS)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def build_stats_from_results(results: list[dict]) -> dict:
    solved = {}
    for r in results:
        if (r.get("result") or "").upper() != "AC":
            continue
        prob_id = r.get("problem_id") or ""
        solved[prob_id] = True

    total = len(solved)
    models = fetch_problem_models()
    easy = medium = hard = 0
    for pid in solved.keys():
        model = models.get(pid) or {}
        diff = model.get("difficulty")
        if diff is None:
            continue
        # heuristic thresholds (AtCoder difficulty ~ expected score)
        if diff < 400:
            easy += 1
        elif diff < 1200:
            medium += 1
        else:
            hard += 1

    return {"totalSolved": total, "easy": easy, "medium": medium, "hard": hard}


def build_daily_activity(results: list[dict], days: int = 90) -> list[dict]:
    now = datetime.now(timezone.utc)
    start_ts = int(now.timestamp()) - days * 86400
    counts = defaultdict(int)
    for r in results:
        if (r.get("result") or "").upper() != "AC":
            continue
        ep = r.get("epoch_second")
        if ep is None or ep < start_ts:
            continue
        day = datetime.fromtimestamp(ep, tz=timezone.utc).date().isoformat()
        counts[day] += 1
    series = []
    for i in range(days):
        day = (now.date()).fromordinal(now.date().toordinal() - (days - 1 - i)).isoformat()
        series.append({"date": day, "count": counts.get(day, 0)})
    return series


def fetch_atcoder_stats(username: str) -> dict:
    info = fetch_user_info(username)
    results = fetch_user_results(username)
    solved = build_stats_from_results(results)
    rating = info.get("rating") or 0
    highest = info.get("highest_rating") or rating
    return {
        **solved,
        "rank": info.get("rank") or "-",
        "contestCount": info.get("accepted_count") or 0,
        "rating": int(rating or 0),
        "maxRating": int(highest or 0),
        "streak": 0,
    }


def fetch_atcoder_daily(username: str, days: int = 90) -> list[dict]:
    results = fetch_user_results(username)
    return build_daily_activity(results, days=days)


