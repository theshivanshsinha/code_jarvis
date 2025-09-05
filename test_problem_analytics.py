#!/usr/bin/env python3
"""
Test script for comprehensive problem analytics features
Run this after starting the server to see the new analytics capabilities
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000/api/stats"

def test_daily_activity():
    """Test enhanced daily activity endpoint"""
    print("🔥 Testing Enhanced Daily Activity")
    print("=" * 50)
    
    try:
        # Test basic daily activity
        response = requests.get(f"{BASE_URL}/daily")
        if response.status_code == 200:
            data = response.json()
            print("✅ Daily activity endpoint working!")
            print(f"  Total Activity: {data.get('totalActivity', 0)} submissions")
            print(f"  Active Days: {data.get('activeDays', 0)} days")
            print(f"  Date Range: {data.get('dateRange', {}).get('start')} to {data.get('dateRange', {}).get('end')}")
            
            # Show some sample days with activity
            days_with_activity = [day for day in data.get('days', []) if day.get('count', 0) > 0][:5]
            if days_with_activity:
                print(f"  Sample Active Days:")
                for day in days_with_activity:
                    print(f"    {day['date']} ({day['weekday']}): {day['count']} submissions")
        else:
            print(f"❌ Daily activity failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing daily activity: {e}")
    
    # Test platform-specific activity
    print("\n📊 Testing Platform-Specific Activity:")
    for platform in ["codeforces", "leetcode", "atcoder"]:
        try:
            response = requests.get(f"{BASE_URL}/daily?platform={platform}")
            if response.status_code == 200:
                data = response.json()
                print(f"  {platform.title()}: {data.get('totalActivity', 0)} submissions in {data.get('activeDays', 0)} days")
        except:
            print(f"  {platform.title()}: Error fetching data")

def test_problem_history():
    """Test comprehensive problem history endpoint"""
    print("\n\n🧩 Testing Problem History")
    print("=" * 50)
    
    try:
        # Test basic problem history
        response = requests.get(f"{BASE_URL}/problems?limit=10")
        if response.status_code == 200:
            data = response.json()
            print("✅ Problem history endpoint working!")
            print(f"  Total Problems: {data.get('total', 0)}")
            print(f"  Showing: {data.get('showing', 0)}")
            
            # Show sample problems
            problems = data.get('problems', [])[:3]
            if problems:
                print(f"  Sample Problems:")
                for problem in problems:
                    print(f"    📝 {problem.get('title', 'Unknown')} ({problem.get('platform', 'unknown')})")
                    print(f"       Difficulty: {problem.get('difficulty', 'unknown')}, Verdict: {problem.get('verdict', 'unknown')}")
                    print(f"       URL: {problem.get('url', 'No URL')}")
                    print(f"       Date: {problem.get('date', 'Unknown')[:19]}")
            
            # Show statistics
            stats = data.get('statistics', {})
            if stats:
                print(f"\n  📈 Statistics:")
                print(f"    Success Rate: {stats.get('successRate', 0)}%")
                print(f"    Platform Distribution: {stats.get('platformDistribution', {})}")
                print(f"    Difficulty Distribution: {stats.get('difficultyDistribution', {})}")
                print(f"    Average Problems/Day: {stats.get('averageProblemsPerDay', 0)}")
        else:
            print(f"❌ Problem history failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing problem history: {e}")
    
    # Test filtering
    print("\n🔍 Testing Problem Filters:")
    filters_to_test = [
        ("difficulty=hard", "Hard Problems"),
        ("verdict=AC", "Accepted Solutions"),
        ("platform=codeforces", "Codeforces Problems"),
        ("days=30&sort=date&order=desc", "Last 30 Days (Recent First)")
    ]
    
    for filter_param, description in filters_to_test:
        try:
            response = requests.get(f"{BASE_URL}/problems?{filter_param}&limit=5")
            if response.status_code == 200:
                data = response.json()
                count = data.get('total', 0)
                print(f"  {description}: {count} problems")
        except:
            print(f"  {description}: Error")

def test_advanced_analytics():
    """Test advanced problem analytics"""
    print("\n\n🔬 Testing Advanced Analytics")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/analytics")
        if response.status_code == 200:
            data = response.json()
            analytics = data.get('analytics', {})
            
            print("✅ Advanced analytics working!")
            print(f"  Total Problems Analyzed: {data.get('totalProblems', 0)}")
            
            # Time Analysis
            time_analysis = analytics.get('timeAnalysis', {})
            print(f"\n  ⏰ Time Analysis:")
            print(f"    Daily Average: {time_analysis.get('dailyAverage', 0)} problems/day")
            print(f"    Total Active Days: {time_analysis.get('totalActiveDays', 0)}")
            most_active = time_analysis.get('mostActiveDay')
            if most_active:
                print(f"    Most Active Day: {most_active[0]} ({most_active[1]} problems)")
            
            # Performance Analysis
            performance = analytics.get('performance', {})
            print(f"\n  📊 Performance Analysis:")
            
            by_difficulty = performance.get('byDifficulty', {})
            for difficulty, stats in by_difficulty.items():
                print(f"    {difficulty.title()}: {stats.get('success', 0)}/{stats.get('attempts', 0)} ({stats.get('successRate', 0)}%)")
            
            by_platform = performance.get('byPlatform', {})
            for platform, stats in by_platform.items():
                print(f"    {platform.title()}: {stats.get('success', 0)}/{stats.get('attempts', 0)} ({stats.get('successRate', 0)}%)")
            
            # Streaks
            streaks = analytics.get('streaks', {})
            print(f"\n  🔥 Streaks:")
            print(f"    Current Streak: {streaks.get('current', 0)} days")
            print(f"    Maximum Streak: {streaks.get('maximum', 0)} days")
            print(f"    Total Active Days: {streaks.get('activeDays', 0)} days")
            
            # Patterns
            patterns = analytics.get('patterns', {})
            hour_dist = patterns.get('hourDistribution', {})
            if hour_dist:
                # Find most active hours
                active_hours = [(hour, count) for hour, count in hour_dist.items() if count > 0]
                active_hours.sort(key=lambda x: x[1], reverse=True)
                print(f"\n  🕐 Activity Patterns:")
                print(f"    Most Active Hours: {', '.join(f'{h}:00 ({c})' for h, c in active_hours[:3])}")
            
            # Success trends
            success_trend = patterns.get('successTrend', [])
            if success_trend:
                recent_trends = success_trend[-5:]  # Last 5 days
                avg_success = sum(day.get('successRate', 0) for day in recent_trends) / len(recent_trends)
                print(f"    Recent Success Rate: {avg_success:.1f}%")
        
        else:
            print(f"❌ Advanced analytics failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing analytics: {e}")

def main():
    """Run all tests"""
    print("🚀 CodeJarvis Problem Analytics Test Suite")
    print("=" * 60)
    print("Testing comprehensive problem tracking, filtering, and analytics")
    print()
    
    # Test all endpoints
    test_daily_activity()
    test_problem_history()
    test_advanced_analytics()
    
    print("\n" + "=" * 60)
    print("🎉 Problem Analytics Testing Complete!")
    
    print(f"\n🆕 NEW FEATURES IMPLEMENTED:")
    print(f"")
    print(f"📅 ENHANCED DAILY ACTIVITY:")
    print(f"  • Real submission data from all platforms")
    print(f"  • Platform-specific filtering (codeforces, leetcode, atcoder)")
    print(f"  • Customizable date ranges")
    print(f"  • Activity statistics and summaries")
    print(f"")
    print(f"🧩 COMPREHENSIVE PROBLEM HISTORY:")
    print(f"  • Complete problem tracking with URLs")
    print(f"  • Advanced filtering by difficulty, platform, verdict, tags")
    print(f"  • Sortable by date, difficulty, platform")
    print(f"  • Success rate and performance statistics")
    print(f"")
    print(f"🔬 ADVANCED ANALYTICS:")
    print(f"  • Time-based analysis (daily, weekly, monthly)")
    print(f"  • Performance breakdowns by difficulty and platform")
    print(f"  • Streak tracking (current and maximum)")
    print(f"  • Activity patterns (hourly distribution)")
    print(f"  • Difficulty progression over time")
    print(f"  • Success rate trends")
    print(f"")
    print(f"🔗 API ENDPOINTS:")
    print(f"  • GET /api/stats/daily - Enhanced daily activity")
    print(f"  • GET /api/stats/problems - Problem history with filtering")
    print(f"  • GET /api/stats/analytics - Advanced analytics dashboard")
    print(f"")
    print(f"🎯 FILTERING OPTIONS:")
    print(f"  • platform=all|codeforces|leetcode|atcoder")
    print(f"  • difficulty=all|easy|medium|hard")
    print(f"  • verdict=all|AC|WA|TLE|etc")
    print(f"  • days=90 (customizable range)")
    print(f"  • limit=100 (results limit)")
    print(f"  • sort=date|difficulty|platform")
    print(f"  • order=desc|asc")
    print(f"  • tags=comma,separated,list")

if __name__ == "__main__":
    print("Make sure your server is running with: python run.py")
    print("Then press Enter to test the new problem analytics...")
    input()
    main()
