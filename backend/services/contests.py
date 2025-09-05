from datetime import datetime, timedelta, timezone
from typing import List, Dict


def fetch_upcoming_contests() -> List[Dict]:
    """Placeholder aggregator. Replace with real platform fetchers.
    Returns a normalized list: platform, name, url, start, durationMinutes.
    """
    now = datetime.now(timezone.utc)
    return [
        {
            "platform": "Codeforces",
            "name": "Educational Round 200",
            "url": "https://codeforces.com/contests",
            "start": (now + timedelta(days=1)).isoformat(),
            "durationMinutes": 120,
        },
        {
            "platform": "LeetCode",
            "name": "Weekly Contest 450",
            "url": "https://leetcode.com/contest/",
            "start": (now + timedelta(days=2, hours=3)).isoformat(),
            "durationMinutes": 90,
        },
        {
            "platform": "AtCoder",
            "name": "ABC 400",
            "url": "https://atcoder.jp/contests/",
            "start": (now + timedelta(days=3, hours=6)).isoformat(),
            "durationMinutes": 100,
        },
    ]


