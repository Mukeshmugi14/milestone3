"""
CodeGalaxy - Mock Database
Provides mock data for UI development without a real database connection.
"""
from datetime import datetime, timedelta
from bson import ObjectId

# ============================================================
# MOCK DATA
# ============================================================

MOCK_USERS = {
    "user_1": {
        "_id": ObjectId(),
        "name": "Demo User",
        "email": "demo@codegalaxy.com",
        "role": "user",
        "status": "active",
        "bio": "A passionate developer exploring the world of AI-powered code generation.",
        "signup_date": datetime.now() - timedelta(days=30),
        "last_login": datetime.now() - timedelta(hours=2),
    },
    "admin_1": {
        "_id": ObjectId(),
        "name": "Admin User",
        "email": "admin@codegalaxy.com",
        "role": "admin",
        "status": "active",
        "bio": "Administrator of the CodeGalaxy platform.",
        "signup_date": datetime.now() - timedelta(days=100),
        "last_login": datetime.now() - timedelta(minutes=15),
    }
}

MOCK_CODES = [
    {
        "_id": ObjectId(),
        "user_id": MOCK_USERS["user_1"]["_id"],
        "model_name": "gemma-2b",
        "language": "Python",
        "prompt": "Create a function to calculate the factorial of a number.",
        "code_output": "def factorial(n):\n    if n == 0:\n        return 1\n    else:\n        return n * factorial(n-1)",
        "created_at": datetime.now() - timedelta(days=1),
    },
    {
        "_id": ObjectId(),
        "user_id": MOCK_USERS["user_1"]["_id"],
        "model_name": "phi-2",
        "language": "JavaScript",
        "prompt": "Write a Javascript function to reverse a string.",
        "code_output": "function reverseString(str) {\n    return str.split('').reverse().join('');\n}",
        "created_at": datetime.now() - timedelta(days=2),
    }
]

MOCK_REVIEWS = [
    {
        "_id": ObjectId(),
        "user_id": MOCK_USERS["user_1"]["_id"],
        "rating": 5,
        "title": "Excellent Tool!",
        "comment": "CodeGalaxy has significantly improved my productivity.",
        "category": "General Feedback",
        "status": "approved",
        "created_at": datetime.now() - timedelta(days=5),
        "helpful_count": 10,
    }
]

# ============================================================
# MOCK FUNCTIONS
# ============================================================

def get_user_code_stats(user_id):
    return {
        "total_codes": len(MOCK_CODES),
        "favorite_model": "gemma-2b",
        "favorite_language": "Python",
    }

def get_user_codes(user_id, limit=10, offset=0):
    return MOCK_CODES

def get_all_users(filters=None, limit=20, offset=0):
    return list(MOCK_USERS.values())

def get_platform_stats():
    return {
        "total_users": len(MOCK_USERS),
        "total_codes": len(MOCK_CODES),
        "active_today": 1,
        "pending_reviews": 0,
    }

def get_model_stats(model_name, date_range=30):
    return {
        "total_uses": 50,
        "successful_uses": 48,
        "failed_uses": 2,
        "avg_response_time": 1.2,
        "success_rate": 96.0,
    }

def get_reviews(status=None, limit=50):
    return MOCK_REVIEWS

def get_user_by_id(user_id):
    for user in MOCK_USERS.values():
        if user["_id"] == user_id:
            return user
    return None

def search_codes(user_id, search_query=None, filters=None):
    return MOCK_CODES

def delete_code(code_id, user_id):
    return True

def update_user(user_id, updates):
    return True

def submit_review(user_id, rating, title, comment, category):
    return True

def vote_helpful(review_id, user_id):
    return True
