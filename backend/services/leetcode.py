import requests
from datetime import datetime, timezone
from collections import defaultdict
import json


GRAPHQL = "https://leetcode.com/graphql"


def _post_json(url: str, json_data: dict) -> dict:
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://leetcode.com/",
        "Origin": "https://leetcode.com"
    }
    resp = requests.post(url, json=json_data, headers=headers, timeout=20)
    resp.raise_for_status()
    return resp.json()


def fetch_user_overview(username: str) -> dict:
    # Updated working GraphQL query for LeetCode
    query = """
    query getUserProfile($username: String!) {
      matchedUser(username: $username) {
        username
        submitStats {
          acSubmissionNum {
            difficulty
            count
          }
        }
        profile {
          ranking
          userAvatar
        }
      }
    }
    """
    try:
        data = _post_json(GRAPHQL, {"query": query, "variables": {"username": username}})
        return data.get("data", {}).get("matchedUser") or {}
    except Exception as e:
        print(f"LeetCode API error for user {username}: {e}")
        return {}


def fetch_recent_submissions(username: str, limit: int = 20) -> list[dict]:
    # Updated working GraphQL query for recent submissions
    query = """
    query getRecentSubmissionList($username: String!, $limit: Int) {
      recentSubmissionList(username: $username, limit: $limit) {
        title
        titleSlug
        timestamp
        statusDisplay
        lang
      }
    }
    """
    try:
        data = _post_json(GRAPHQL, {"query": query, "variables": {"username": username, "limit": limit}})
        return data.get("data", {}).get("recentSubmissionList") or []
    except Exception as e:
        print(f"LeetCode submissions API error for user {username}: {e}")
        return []


def fetch_user_contest_info(username: str) -> dict:
    # Get contest information
    query = """
    query getUserContestRanking($username: String!) {
      userContestRanking(username: $username) {
        attendedContestsCount
        rating
        globalRanking
        topPercentage
      }
    }
    """
    try:
        data = _post_json(GRAPHQL, {"query": query, "variables": {"username": username}})
        return data.get("data", {}).get("userContestRanking") or {}
    except Exception as e:
        print(f"LeetCode contest API error for user {username}: {e}")
        return {}


def build_overview(user: dict, contest_info: dict = None) -> dict:
    # Updated to use the correct API structure
    stats = user.get("submitStats", {}).get("acSubmissionNum", [])
    by_diff = {row.get("difficulty"): row.get("count", 0) for row in stats}
    
    # LeetCode uses "Easy", "Medium", "Hard" (capitalized)
    easy = by_diff.get("Easy", 0)
    medium = by_diff.get("Medium", 0)
    hard = by_diff.get("Hard", 0)
    total = easy + medium + hard
    
    # Also get total from "All" if available as backup
    if total == 0 and "All" in by_diff:
        total = by_diff.get("All", 0)
        # If we have total but no breakdown, distribute roughly
        if total > 0:
            easy = int(total * 0.4)  # Rough approximation
            medium = int(total * 0.4)
            hard = total - easy - medium
    
    ranking = user.get("profile", {}).get("ranking")
    
    # Use contest info if available
    contest_count = 0
    rating = 0
    if contest_info:
        contest_count = contest_info.get("attendedContestsCount", 0)
        rating = int(contest_info.get("rating", 0))
    
    return {
        "totalSolved": total,
        "easy": easy,
        "medium": medium,
        "hard": hard,
        "rank": str(ranking) if ranking is not None else "-",
        "contestCount": contest_count,
        "rating": rating,
        "maxRating": rating,  # LeetCode doesn't separate current vs max rating easily
        "streak": 0,  # Would need additional API calls to calculate
    }


def build_daily_activity(submissions: list[dict], days: int = 90) -> list[dict]:
    counts = defaultdict(int)
    now = datetime.now(timezone.utc)
    start_ts = int(now.timestamp()) - days * 86400
    
    for submission in submissions:
        # LeetCode timestamps are usually in seconds, but let's handle both
        ts = submission.get("timestamp")
        if ts is None:
            continue
        
        # Ensure timestamp is a number
        try:
            ts = float(ts)
        except (ValueError, TypeError):
            continue
            
        # Convert timestamp to seconds if it's in milliseconds
        if ts > 9999999999:  # If timestamp is > year 2001 in seconds, it's probably milliseconds
            ts = ts / 1000
            
        if ts < start_ts:
            continue
            
        # Only count successful submissions
        status = submission.get("statusDisplay", "")
        if status == "Accepted":
            day = datetime.fromtimestamp(ts, tz=timezone.utc).date().isoformat()
            counts[day] += 1
    
    series = []
    for i in range(days):
        day = (now.date()).fromordinal(now.date().toordinal() - (days - 1 - i)).isoformat()
        series.append({"date": day, "count": counts.get(day, 0)})
    
    return series


def get_problem_details_from_submissions(submissions: list[dict], days_back: int = 90) -> list[dict]:
    """Convert LeetCode submissions to problem history format"""
    problems = []
    now = datetime.now(timezone.utc)
    start_ts = int(now.timestamp()) - days_back * 86400
    
    for submission in submissions:
        ts = submission.get("timestamp")
        if ts is None:
            continue
        
        # Ensure timestamp is a number
        try:
            ts = float(ts)
        except (ValueError, TypeError):
            continue
            
        # Convert timestamp if needed
        if ts > 9999999999:
            ts = ts / 1000
            
        if ts < start_ts:
            continue
            
        # Create problem entry
        title = submission.get("title", "Unknown Problem")
        title_slug = submission.get("titleSlug", "")
        status = submission.get("statusDisplay", "Unknown")
        language = submission.get("lang", "Unknown")
        
        # Map LeetCode status to standard format
        verdict = "AC" if status == "Accepted" else status.upper().replace(" ", "_")
        
        # Estimate difficulty (would need additional API call for exact difficulty)
        difficulty = "medium"  # Default, could be enhanced with title-based heuristics
        
        problem = {
            "platform": "leetcode",
            "problemId": title_slug or title.lower().replace(" ", "-"),
            "title": title,
            "difficulty": difficulty,
            "verdict": verdict,
            "language": language,
            "rating": 0,  # LeetCode doesn't expose problem ratings in this API
            "tags": [],  # Would need additional API calls
            "date": datetime.fromtimestamp(ts, tz=timezone.utc).isoformat(),
            "timestamp": int(ts),
            "url": f"https://leetcode.com/problems/{title_slug}/" if title_slug else "https://leetcode.com/",
            "contestName": ""  # LeetCode doesn't always link problems to contests
        }
        
        problems.append(problem)
    
    return problems


def fetch_leetcode_stats(username: str) -> dict:
    user = fetch_user_overview(username)
    contest_info = fetch_user_contest_info(username)
    return build_overview(user, contest_info)


def fetch_leetcode_daily(username: str, days: int = 90) -> list[dict]:
    submissions = fetch_recent_submissions(username, limit=100)
    return build_daily_activity(submissions, days=days)


def fetch_leetcode_problems(username: str, days_back: int = 90) -> list[dict]:
    """Fetch LeetCode problems for problem history"""
    submissions = fetch_recent_submissions(username, limit=100)
    return get_problem_details_from_submissions(submissions, days_back)


