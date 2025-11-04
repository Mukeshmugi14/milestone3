"""
CodeGalaxy - Database Operations
All CRUD operations for Firebase Firestore.
"""
from firebase_config import db
from datetime import datetime, timedelta
import pytz

# ============================================================
# USER FUNCTIONS
# ============================================================

def create_user(name, email, firebase_uid, auth_provider="email", oauth_data=None):
    """
    Creates a new user document in Firestore.
    """
    try:
        user_ref = db.collection('users').document(firebase_uid)
        user_doc = {
            "name": name,
            "email": email,
            "firebase_uid": firebase_uid,
            "role": "user",
            "status": "active",
            "avatar_url": oauth_data.get('avatar_url', '') if oauth_data else '',
            "bio": "",
            "theme_preference": "dark",
            "email_notifications": True,
            "auth_provider": auth_provider,
            "signup_date": datetime.now(pytz.UTC),
            "last_login": datetime.now(pytz.UTC),
        }
        user_ref.set(user_doc)
        return user_doc
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

def get_user_by_firebase_uid(firebase_uid):
    """
    Retrieves a user document from Firestore by Firebase UID.
    """
    try:
        user_ref = db.collection('users').document(firebase_uid)
        user = user_ref.get()
        if user.exists:
            return user.to_dict()
        return None
    except Exception as e:
        print(f"Error getting user by firebase_uid: {e}")
        return None

def update_user(firebase_uid, updates):
    """
    Updates a user document in Firestore.
    """
    try:
        user_ref = db.collection('users').document(firebase_uid)
        updates['updated_at'] = datetime.now(pytz.UTC)
        user_ref.update(updates)
        return get_user_by_firebase_uid(firebase_uid)
    except Exception as e:
        print(f"Error updating user: {e}")
        return None

# ============================================================
# CODE FUNCTIONS
# ============================================================

def save_code(firebase_uid, model_name, task_type, language, prompt, code_output, metadata=None):
    """
    Saves generated code to a user's 'codes' subcollection in Firestore.
    """
    try:
        code_ref = db.collection('users').document(firebase_uid).collection('codes').document()
        code_doc = {
            "firebase_uid": firebase_uid,
            "model_name": model_name,
            "task_type": task_type,
            "language": language,
            "prompt": prompt,
            "code_output": code_output,
            "metadata": metadata or {},
            "created_at": datetime.now(pytz.UTC),
        }
        code_ref.set(code_doc)
        return code_doc
    except Exception as e:
        print(f"Error saving code: {e}")
        return None

def get_user_codes(firebase_uid, limit=10):
    """
    Retrieves a user's code history from Firestore.
    """
    try:
        codes_ref = db.collection('users').document(firebase_uid).collection('codes')
        query = codes_ref.order_by("created_at", direction="DESCENDING").limit(limit)
        codes = [doc.to_dict() for doc in query.stream()]
        return codes
    except Exception as e:
        print(f"Error getting user codes: {e}")
        return []

# ============================================================
# REVIEW FUNCTIONS
# ============================================================

def submit_review(firebase_uid, rating, title, comment, category):
    """
    Submits a new review to the 'reviews' collection in Firestore.
    """
    try:
        review_ref = db.collection('reviews').document()
        review_doc = {
            "firebase_uid": firebase_uid,
            "rating": rating,
            "title": title,
            "comment": comment,
            "category": category,
            "status": "pending",
            "created_at": datetime.now(pytz.UTC),
        }
        review_ref.set(review_doc)
        return review_doc
    except Exception as e:
        print(f"Error submitting review: {e}")
        return None

def get_reviews(status="approved", limit=20):
    """
    Retrieves reviews from Firestore, optionally filtering by status.
    """
    try:
        reviews_ref = db.collection('reviews')
        query = reviews_ref.where("status", "==", status).order_by("created_at", direction="DESCENDING").limit(limit)
        reviews = [doc.to_dict() for doc in query.stream()]
        return reviews
    except Exception as e:
        print(f"Error getting reviews: {e}")
        return []
