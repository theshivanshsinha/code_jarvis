from datetime import datetime, timedelta
import requests
import random
from typing import List, Dict, Optional
from .leetcode import _post_json as leetcode_post_json
from .codeforces import _get_json as codeforces_get_json
from .atcoder import _get_json as atcoder_get_json

class QuestionOfTheDayService:
    def __init__(self):
        self.platforms = ['leetcode', 'codeforces', 'atcoder']
        self.cache = {}
        self.cache_expiry = timedelta(hours=12)  # Cache for 12 hours
    
    def get_daily_questions(self) -> List[Dict]:
        """Get question of the day from all platforms"""
        today = datetime.now().date().isoformat()
        
        # Check if cached data is still valid
        if (today in self.cache and 
            datetime.now() - self.cache[today]['timestamp'] < self.cache_expiry):
            return self.cache[today]['questions']
        
        questions = []
        
        # Get LeetCode daily question
        leetcode_question = self._get_leetcode_daily()
        if leetcode_question:
            questions.append(leetcode_question)
        
        # Get Codeforces interesting problem
        codeforces_question = self._get_codeforces_daily()
        if codeforces_question:
            questions.append(codeforces_question)
        
        # Get AtCoder recent contest problem
        atcoder_question = self._get_atcoder_daily()
        if atcoder_question:
            questions.append(atcoder_question)
        
        # Cache the results
        self.cache[today] = {
            'questions': questions,
            'timestamp': datetime.now()
        }
        
        return questions
    
    def _get_leetcode_daily(self) -> Optional[Dict]:
        """Get LeetCode daily coding challenge"""
        try:
            # LeetCode GraphQL query for daily coding challenge
            query = """
            query questionOfToday {
                activeDailyCodingChallengeQuestion {
                    date
                    userStatus
                    link
                    question {
                        acRate
                        difficulty
                        freqBar
                        frontendQuestionId: questionFrontendId
                        isFavor
                        paidOnly: isPaidOnly
                        status
                        title
                        titleSlug
                        hasVideoSolution
                        hasSolution
                        topicTags {
                            name
                            id
                            slug
                        }
                    }
                }
            }
            """
            
            url = "https://leetcode.com/graphql"
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.post(url, json={'query': query}, headers=headers, timeout=10)
            data = response.json()
            
            if 'data' in data and data['data']['activeDailyCodingChallengeQuestion']:
                challenge = data['data']['activeDailyCodingChallengeQuestion']
                question = challenge['question']
                
                return {
                    'platform': 'leetcode',
                    'id': question['frontendQuestionId'],
                    'title': question['title'],
                    'difficulty': question['difficulty'].lower(),
                    'url': f"https://leetcode.com{challenge['link']}",
                    'description': f"Daily Coding Challenge #{question['frontendQuestionId']}",
                    'acceptance_rate': f"{question['acRate']:.1f}%",
                    'is_premium': question['paidOnly'],
                    'tags': [tag['name'] for tag in question.get('topicTags', [])],
                    'color': '#FFA116',
                    'icon': '💻',
                    'type': 'daily_challenge',
                    'estimated_time': self._estimate_time(question['difficulty']),
                }
        except Exception as e:
            print(f"Failed to get LeetCode daily question: {str(e)}")
        
        # Fallback to a curated problem
        return self._get_leetcode_fallback()
    
    def _get_codeforces_daily(self) -> Optional[Dict]:
        """Get an interesting Codeforces problem"""
        try:
            # Get recent contest problems with good ratings
            url = "https://codeforces.com/api/problemset.problems"
            params = {'tags': 'implementation'}  # Start with implementation problems
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            if data.get('status') != 'OK':
                return None
            problems = data.get('result', {}).get('problems', [])
            
            if not problems:
                return None
            
            # Filter problems with rating between 1200-1600 (good for daily practice)
            good_problems = [
                p for p in problems 
                if p.get('rating', 0) >= 1200 and p.get('rating', 0) <= 1600
                and len(p.get('tags', [])) <= 3  # Not too complex
            ]
            
            if not good_problems:
                good_problems = problems[:50]  # Fallback to recent problems
            
            # Select a random problem
            problem = random.choice(good_problems[:20])  # From top 20
            
            return {
                'platform': 'codeforces',
                'id': f"{problem['contestId']}{problem['index']}",
                'title': problem['name'],
                'difficulty': self._map_codeforces_difficulty(problem.get('rating', 1400)),
                'url': f"https://codeforces.com/problemset/problem/{problem['contestId']}/{problem['index']}",
                'description': f"Contest {problem['contestId']} - Problem {problem['index']}",
                'rating': problem.get('rating', 'Unrated'),
                'tags': problem.get('tags', []),
                'color': '#1F8ACB',
                'icon': '🏆',
                'type': 'practice_problem',
                'estimated_time': self._estimate_time_by_rating(problem.get('rating', 1400)),
            }
        except Exception as e:
            print(f"Failed to get Codeforces daily question: {str(e)}")
        
        return self._get_codeforces_fallback()
    
    def _get_atcoder_daily(self) -> Optional[Dict]:
        """Get an AtCoder problem from recent contests"""
        try:
            # Get recent contests
            url = "https://kenkoooo.com/atcoder/resources/contests.json"
            response = requests.get(url, timeout=10)
            contests = response.json()
            
            if not contests:
                return None
            
            # Get ABC (AtCoder Beginner Contest) problems - most accessible
            abc_contests = [
                c for c in contests 
                if c['id'].startswith('abc') and 
                datetime.fromtimestamp(c['start_epoch_second']) > datetime.now() - timedelta(days=90)
            ]
            
            if not abc_contests:
                abc_contests = [c for c in contests if c['id'].startswith('abc')][-10:]  # Latest 10
            
            # Pick a random recent contest
            contest = random.choice(abc_contests[:10])
            
            # Generate problem (A, B, C are good for daily practice)
            problem_letters = ['a', 'b', 'c']
            problem_letter = random.choice(problem_letters)
            
            return {
                'platform': 'atcoder',
                'id': f"{contest['id']}_{problem_letter}",
                'title': f"{contest['title']} - Problem {problem_letter.upper()}",
                'difficulty': self._map_atcoder_difficulty(problem_letter),
                'url': f"https://atcoder.jp/contests/{contest['id']}/tasks/{contest['id']}_{problem_letter}",
                'description': f"From {contest['title']}",
                'contest': contest['title'],
                'tags': ['algorithm', 'beginner' if problem_letter in ['a', 'b'] else 'intermediate'],
                'color': '#3F7FBF',
                'icon': '🎯',
                'type': 'contest_problem',
                'estimated_time': self._estimate_time(self._map_atcoder_difficulty(problem_letter)),
            }
        except Exception as e:
            print(f"Failed to get AtCoder daily question: {str(e)}")
        
        return self._get_atcoder_fallback()
    
    def _get_leetcode_fallback(self) -> Dict:
        """Fallback LeetCode problems when API fails"""
        fallback_problems = [
            {
                'id': '1', 'title': 'Two Sum', 'difficulty': 'easy',
                'tags': ['Array', 'Hash Table'], 'description': 'Classic array problem'
            },
            {
                'id': '121', 'title': 'Best Time to Buy and Sell Stock', 'difficulty': 'easy',
                'tags': ['Array', 'Dynamic Programming'], 'description': 'Popular DP problem'
            },
            {
                'id': '206', 'title': 'Reverse Linked List', 'difficulty': 'easy',
                'tags': ['Linked List'], 'description': 'Essential linked list problem'
            },
            {
                'id': '20', 'title': 'Valid Parentheses', 'difficulty': 'easy',
                'tags': ['String', 'Stack'], 'description': 'Stack implementation practice'
            },
            {
                'id': '104', 'title': 'Maximum Depth of Binary Tree', 'difficulty': 'easy',
                'tags': ['Tree', 'DFS', 'BFS'], 'description': 'Tree traversal basics'
            },
        ]
        
        problem = random.choice(fallback_problems)
        return {
            'platform': 'leetcode',
            'id': problem['id'],
            'title': problem['title'],
            'difficulty': problem['difficulty'],
            'url': f"https://leetcode.com/problems/{problem['title'].lower().replace(' ', '-')}/",
            'description': problem['description'],
            'tags': problem['tags'],
            'color': '#FFA116',
            'icon': '💻',
            'type': 'curated_problem',
            'estimated_time': self._estimate_time(problem['difficulty']),
        }
    
    def _get_codeforces_fallback(self) -> Dict:
        """Fallback Codeforces problems"""
        fallback_problems = [
            {
                'id': '4A', 'title': 'Watermelon', 'rating': 800,
                'tags': ['math', 'brute force'], 'description': 'Simple math problem'
            },
            {
                'id': '71A', 'title': 'Way Too Long Words', 'rating': 800,
                'tags': ['strings'], 'description': 'String manipulation'
            },
            {
                'id': '158A', 'title': 'Next Round', 'rating': 800,
                'tags': ['implementation'], 'description': 'Basic implementation'
            },
            {
                'id': '282A', 'title': 'Bit++', 'rating': 800,
                'tags': ['implementation'], 'description': 'Simple counting'
            },
        ]
        
        problem = random.choice(fallback_problems)
        return {
            'platform': 'codeforces',
            'id': problem['id'],
            'title': problem['title'],
            'difficulty': self._map_codeforces_difficulty(problem['rating']),
            'url': f"https://codeforces.com/problemset/problem/{problem['id'][:-1]}/{problem['id'][-1]}",
            'description': problem['description'],
            'rating': problem['rating'],
            'tags': problem['tags'],
            'color': '#1F8ACB',
            'icon': '🏆',
            'type': 'curated_problem',
            'estimated_time': self._estimate_time_by_rating(problem['rating']),
        }
    
    def _get_atcoder_fallback(self) -> Dict:
        """Fallback AtCoder problems"""
        fallback_problems = [
            {
                'id': 'abc100_a', 'title': 'Happy Birthday!', 'difficulty': 'easy',
                'tags': ['implementation'], 'description': 'Basic input/output'
            },
            {
                'id': 'abc100_b', 'title': 'Ringo\'s Favorite Numbers', 'difficulty': 'easy',
                'tags': ['math'], 'description': 'Mathematical thinking'
            },
            {
                'id': 'abc200_a', 'title': 'Century', 'difficulty': 'easy',
                'tags': ['math'], 'description': 'Simple calculation'
            },
        ]
        
        problem = random.choice(fallback_problems)
        return {
            'platform': 'atcoder',
            'id': problem['id'],
            'title': problem['title'],
            'difficulty': problem['difficulty'],
            'url': f"https://atcoder.jp/contests/{problem['id'].split('_')[0]}/tasks/{problem['id']}",
            'description': problem['description'],
            'tags': problem['tags'],
            'color': '#3F7FBF',
            'icon': '🎯',
            'type': 'curated_problem',
            'estimated_time': self._estimate_time(problem['difficulty']),
        }
    
    def _map_codeforces_difficulty(self, rating: int) -> str:
        """Map Codeforces rating to difficulty"""
        if rating <= 1200:
            return 'easy'
        elif rating <= 1600:
            return 'medium'
        else:
            return 'hard'
    
    def _map_atcoder_difficulty(self, problem_letter: str) -> str:
        """Map AtCoder problem letter to difficulty"""
        if problem_letter.lower() in ['a', 'b']:
            return 'easy'
        elif problem_letter.lower() in ['c', 'd']:
            return 'medium'
        else:
            return 'hard'
    
    def _estimate_time(self, difficulty: str) -> str:
        """Estimate time to solve based on difficulty"""
        time_map = {
            'easy': '15-30 min',
            'medium': '30-60 min',
            'hard': '60+ min'
        }
        return time_map.get(difficulty.lower(), '30 min')
    
    def _estimate_time_by_rating(self, rating: int) -> str:
        """Estimate time based on Codeforces rating"""
        if rating <= 1000:
            return '10-20 min'
        elif rating <= 1400:
            return '20-40 min'
        elif rating <= 1800:
            return '40-90 min'
        else:
            return '90+ min'
    
    def get_motivational_message(self) -> str:
        """Get a random motivational message for the day"""
        messages = [
            "🚀 Start your day with a coding challenge!",
            "💪 Every problem solved makes you stronger!",
            "🧠 Exercise your brain with these handpicked problems!",
            "⭐ Today's challenges are tomorrow's skills!",
            "🎯 Ready to level up your programming?",
            "🔥 Consistency is key - solve something today!",
            "💻 Great programmers are made, not born!",
            "🏆 Challenge yourself with today's problems!",
            "📚 Learning never stops - keep coding!",
            "✨ Turn today's struggle into tomorrow's strength!"
        ]
        return random.choice(messages)
    
    def get_difficulty_stats(self, questions: List[Dict]) -> Dict:
        """Get difficulty distribution statistics"""
        if not questions:
            return {'easy': 0, 'medium': 0, 'hard': 0}
        
        difficulty_count = {'easy': 0, 'medium': 0, 'hard': 0}
        for question in questions:
            difficulty = question.get('difficulty', 'medium')
            difficulty_count[difficulty] = difficulty_count.get(difficulty, 0) + 1
        
        return difficulty_count

# Global service instance
qotd_service = QuestionOfTheDayService()
