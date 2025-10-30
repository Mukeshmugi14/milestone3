"""
CodeGalaxy - Database Operations
MongoDB connection and all CRUD operations
"""
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, OperationFailure
import bcrypt
import os
from datetime import datetime, timedelta
from bson import ObjectId
import re

# MongoDB Connection
def get_database():
    """
    Establishes and returns MongoDB database connection
    Returns: MongoDB database object
    """
    try:
        mongo_uri = os.getenv('MONGO_URI')
        if not mongo_uri:
            raise ValueError("MONGO_URI not found in environment variables")

        client = MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000
        )


        # Test connection
        client.admin.command('ping')

        db = client['codegalaxy']
        return db

    except ConnectionFailure as e:
        print(f"Failed to connect to MongoDB: {e}")
        return None
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# Initialize database and create indexes
def create_indexes():
    """
    Creates all necessary indexes on collections
    Called on application startup
    """
    try:
        db = get_database()
        if not db:
            return False

        # Users collection indexes
        db.users.create_index([("email", ASCENDING)], unique=True)
        db.users.create_index([("role", ASCENDING)])
        db.users.create_index([("status", ASCENDING)])
        db.users.create_index([("signup_date", DESCENDING)])

        # OTPs collection indexes
        db.otps.create_index([("email", ASCENDING)])
        db.otps.create_index([("otp_code", ASCENDING)])
        db.otps.create_index([("expires_at", ASCENDING)], expireAfterSeconds=0)

        # Codes collection indexes
        db.codes.create_index([("user_id", ASCENDING)])
        db.codes.create_index([("model_name", ASCENDING)])
        db.codes.create_index([("language", ASCENDING)])
        db.codes.create_index([("created_at", DESCENDING)])
        db.codes.create_index([("user_id", ASCENDING), ("created_at", DESCENDING)])

        # Reviews collection indexes
        db.reviews.create_index([("user_id", ASCENDING)])
        db.reviews.create_index([("status", ASCENDING)])
        db.reviews.create_index([("created_at", DESCENDING)])
        db.reviews.create_index([("rating", ASCENDING)])

        # Logs collection indexes
        db.logs.create_index([("type", ASCENDING)])
        db.logs.create_index([("user_id", ASCENDING)])
        db.logs.create_index([("admin_id", ASCENDING)])
        db.logs.create_index([("created_at", DESCENDING)])
        db.logs.create_index([("severity", ASCENDING)])

        # Models collection indexes
        db.models.create_index([("model_name", ASCENDING)])
        db.models.create_index([("date", DESCENDING)])
        db.models.create_index([("model_name", ASCENDING), ("date", DESCENDING)])

        # Challenges collection indexes
        db.challenges.create_index([("user_id", ASCENDING)])
        db.challenges.create_index([("challenge_date", ASCENDING)])
        db.challenges.create_index([("user_id", ASCENDING), ("challenge_date", ASCENDING)], unique=True)

        # Challenges global collection indexes
        db.challenges_global.create_index([("date", ASCENDING)], unique=True)

        return True

    except Exception as e:
        print(f"Error creating indexes: {e}")
        return False

# ============================================================
# USER FUNCTIONS
# ============================================================

def create_user(name, email, password=None, auth_provider="email", oauth_data=None):
    """
    Creates a new user account
    Args:
        name: User's full name
        email: User's email address
        password: Plain password (will be hashed if provided)
        auth_provider: "email", "google", or "github"
        oauth_data: Dict with OAuth info (provider_id, tokens, avatar)
    Returns: User document or None if error
    """
    try:
        db = get_database()
        if not db:
            return None

        # Check if email already exists
        existing = db.users.find_one({"email": email})
        if existing:
            return None

        user_doc = {
            "name": name,
            "email": email,
            "password": bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8') if password else None,
            "role": "user",
            "status": "active",
            "suspended_at": None,
            "avatar_url": oauth_data.get('avatar_url', '') if oauth_data else '',
            "bio": "",
            "theme_preference": "dark",
            "email_notifications": True,
            "auth_provider": auth_provider,
            "oauth_provider_id": oauth_data.get('provider_id', '') if oauth_data else '',
            "oauth_access_token": oauth_data.get('access_token', '') if oauth_data else '',
            "oauth_refresh_token": oauth_data.get('refresh_token', '') if oauth_data else '',
            "signup_date": datetime.now(),
            "last_login": datetime.now(),
            "login_history": [],
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }

        result = db.users.insert_one(user_doc)
        user_doc['_id'] = result.inserted_id

        return user_doc

    except Exception as e:
        print(f"Error creating user: {e}")
        return None

def verify_email_password(email, password):
    """
    Verifies email and password combination
    Args:
        email: User's email
        password: Plain password to verify
    Returns: User document if valid, None if invalid
    """
    try:
        db = get_database()
        if not db:
            return None

        user = db.users.find_one({"email": email})
        if not user or not user.get('password'):
            return None

        # Verify password
        if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return user

        return None

    except Exception as e:
        print(f"Error verifying credentials: {e}")
        return None

def get_user_by_id(user_id):
    """
    Retrieves user by ID
    Args:
        user_id: User's ObjectId or string ID
    Returns: User document or None
    """
    try:
        db = get_database()
        if not db:
            return None

        if isinstance(user_id, str):
            user_id = ObjectId(user_id)

        return db.users.find_one({"_id": user_id})

    except Exception as e:
        print(f"Error getting user: {e}")
        return None

def get_user_by_email(email):
    """
    Retrieves user by email
    Args:
        email: User's email address
    Returns: User document or None
    """
    try:
        db = get_database()
        if not db:
            return None

        return db.users.find_one({"email": email})

    except Exception as e:
        print(f"Error getting user by email: {e}")
        return None

def update_user(user_id, updates):
    """
    Updates user document with provided fields
    Args:
        user_id: User's ObjectId or string ID
        updates: Dict of fields to update
    Returns: Updated user document or None
    """
    try:
        db = get_database()
        if not db:
            return None

        if isinstance(user_id, str):
            user_id = ObjectId(user_id)

        updates['updated_at'] = datetime.now()

        db.users.update_one(
            {"_id": user_id},
            {"$set": updates}
        )

        return db.users.find_one({"_id": user_id})

    except Exception as e:
        print(f"Error updating user: {e}")
        return None

def delete_user(user_id):
    """
    Deletes user and all related data (cascading delete)
    Args:
        user_id: User's ObjectId or string ID
    Returns: Number of documents deleted
    """
    try:
        db = get_database()
        if not db:
            return 0

        if isinstance(user_id, str):
            user_id = ObjectId(user_id)

        # Delete user
        user_result = db.users.delete_one({"_id": user_id})

        # Delete related data
        codes_result = db.codes.delete_many({"user_id": user_id})
        reviews_result = db.reviews.delete_many({"user_id": user_id})
        challenges_result = db.challenges.delete_many({"user_id": user_id})

        total_deleted = (
            user_result.deleted_count +
            codes_result.deleted_count +
            reviews_result.deleted_count +
            challenges_result.deleted_count
        )

        return total_deleted

    except Exception as e:
        print(f"Error deleting user: {e}")
        return 0

def update_login_history(user_id, ip_address, user_agent):
    """
    Updates user's login history
    Args:
        user_id: User's ObjectId or string ID
        ip_address: User's IP address
        user_agent: User's browser user agent
    Returns: True if successful, False otherwise
    """
    try:
        db = get_database()
        if not db:
            return False

        if isinstance(user_id, str):
            user_id = ObjectId(user_id)

        # Parse user agent for device info
        device = "Unknown"
        if "Mobile" in user_agent:
            device = "Mobile"
        elif "Tablet" in user_agent:
            device = "Tablet"
        else:
            device = "Desktop"

        login_entry = {
            "timestamp": datetime.now(),
            "ip_address": ip_address,
            "user_agent": user_agent,
            "device": device
        }

        # Update last login and add to history (keep last 20)
        db.users.update_one(
            {"_id": user_id},
            {
                "$set": {"last_login": datetime.now()},
                "$push": {
                    "login_history": {
                        "$each": [login_entry],
                        "$slice": -20
                    }
                }
            }
        )

        return True

    except Exception as e:
        print(f"Error updating login history: {e}")
        return False

def get_all_users(filters=None, limit=20, offset=0):
    """
    Retrieves all users with optional filters
    Args:
        filters: Dict of filter criteria
        limit: Number of users to return
        offset: Number of users to skip
    Returns: List of user documents
    """
    try:
        db = get_database()
        if not db:
            return []

        query = {}
        if filters:
            if filters.get('role'):
                query['role'] = filters['role']
            if filters.get('status'):
                query['status'] = filters['status']
            if filters.get('search'):
                search_term = filters['search']
                query['$or'] = [
                    {"name": {"$regex": search_term, "$options": "i"}},
                    {"email": {"$regex": search_term, "$options": "i"}}
                ]

        users = list(db.users.find(query).skip(offset).limit(limit).sort("created_at", DESCENDING))
        return users

    except Exception as e:
        print(f"Error getting all users: {e}")
        return []

# ============================================================
# OTP FUNCTIONS
# ============================================================

def create_otp(email, purpose):
    """
    Generates and stores a 6-digit OTP
    Args:
        email: User's email address
        purpose: "signup", "password_reset", or "login"
    Returns: OTP code (6-digit string)
    """
    try:
        import random

        db = get_database()
        if not db:
            return None

        # Generate 6-digit OTP
        otp_code = str(random.randint(100000, 999999))

        otp_doc = {
            "email": email,
            "otp_code": otp_code,
            "purpose": purpose,
            "expires_at": datetime.now() + timedelta(minutes=10),
            "used": False,
            "created_at": datetime.now()
        }

        db.otps.insert_one(otp_doc)

        return otp_code

    except Exception as e:
        print(f"Error creating OTP: {e}")
        return None

def verify_otp(email, otp_code, purpose):
    """
    Verifies OTP code
    Args:
        email: User's email address
        otp_code: 6-digit OTP code
        purpose: OTP purpose to match
    Returns: True if valid, False if invalid/expired
    """
    try:
        db = get_database()
        if not db:
            return False

        otp_doc = db.otps.find_one({
            "email": email,
            "otp_code": otp_code,
            "purpose": purpose,
            "used": False,
            "expires_at": {"$gt": datetime.now()}
        })

        if otp_doc:
            # Mark as used
            db.otps.update_one(
                {"_id": otp_doc['_id']},
                {"$set": {"used": True}}
            )
            return True

        return False

    except Exception as e:
        print(f"Error verifying OTP: {e}")
        return False

# ============================================================
# CODE FUNCTIONS
# ============================================================

def save_code(user_id, model_name, task_type, language, prompt, code_output, metadata=None):
    """
    Saves generated code to history
    Args:
        user_id: User's ObjectId or string ID
        model_name: "gemma-2b", "phi-2", or "codebert"
        task_type: "generate", "explain", or "improve"
        language: Programming language
        prompt: User's input prompt
        code_output: Generated code
        metadata: Dict with tokens_used, response_time, success
    Returns: Code document or None
    """
    try:
        db = get_database()
        if not db:
            return None

        if isinstance(user_id, str):
            user_id = ObjectId(user_id)

        code_doc = {
            "user_id": user_id,
            "model_name": model_name,
            "task_type": task_type,
            "language": language,
            "prompt": prompt,
            "code_output": code_output,
            "explanation": metadata.get('explanation', '') if metadata else '',
            "improvement_notes": metadata.get('improvement_notes', '') if metadata else '',
            "tokens_used": metadata.get('tokens_used', 0) if metadata else 0,
            "response_time": metadata.get('response_time', 0) if metadata else 0,
            "success": metadata.get('success', True) if metadata else True,
            "error_message": metadata.get('error_message', '') if metadata else '',
            "created_at": datetime.now()
        }

        result = db.codes.insert_one(code_doc)
        code_doc['_id'] = result.inserted_id

        return code_doc

    except Exception as e:
        print(f"Error saving code: {e}")
        return None

def get_user_codes(user_id, limit=10, offset=0):
    """
    Retrieves user's code history
    Args:
        user_id: User's ObjectId or string ID
        limit: Number of codes to return
        offset: Number of codes to skip
    Returns: List of code documents
    """
    try:
        db = get_database()
        if not db:
            return []

        if isinstance(user_id, str):
            user_id = ObjectId(user_id)

        codes = list(
            db.codes.find({"user_id": user_id})
            .skip(offset)
            .limit(limit)
            .sort("created_at", DESCENDING)
        )

        return codes

    except Exception as e:
        print(f"Error getting user codes: {e}")
        return []

def search_codes(user_id, search_query=None, filters=None):
    """
    Searches user's code history with fuzzy matching
    Args:
        user_id: User's ObjectId or string ID
        search_query: Text to search for
        filters: Dict with date_range, models, languages
    Returns: List of matching code documents
    """
    try:
        db = get_database()
        if not db:
            return []

        if isinstance(user_id, str):
            user_id = ObjectId(user_id)

        query = {"user_id": user_id}

        # Add search query
        if search_query:
            query['$or'] = [
                {"prompt": {"$regex": search_query, "$options": "i"}},
                {"code_output": {"$regex": search_query, "$options": "i"}}
            ]

        # Add filters
        if filters:
            if filters.get('models'):
                query['model_name'] = {"$in": filters['models']}
            if filters.get('languages'):
                query['language'] = {"$in": filters['languages']}
            if filters.get('date_from') and filters.get('date_to'):
                query['created_at'] = {
                    "$gte": filters['date_from'],
                    "$lte": filters['date_to']
                }

        codes = list(db.codes.find(query).sort("created_at", DESCENDING))
        return codes

    except Exception as e:
        print(f"Error searching codes: {e}")
        return []

def delete_code(code_id, user_id):
    """
    Deletes a code document (with user verification)
    Args:
        code_id: Code's ObjectId or string ID
        user_id: User's ObjectId or string ID (for verification)
    Returns: True if deleted, False otherwise
    """
    try:
        db = get_database()
        if not db:
            return False

        if isinstance(code_id, str):
            code_id = ObjectId(code_id)
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)

        result = db.codes.delete_one({
            "_id": code_id,
            "user_id": user_id
        })

        return result.deleted_count > 0

    except Exception as e:
        print(f"Error deleting code: {e}")
        return False

def get_user_code_stats(user_id):
    """
    Gets statistics about user's code generation
    Args:
        user_id: User's ObjectId or string ID
    Returns: Dict with stats (total_codes, favorite_model, favorite_language)
    """
    try:
        db = get_database()
        if not db:
            return {"total_codes": 0, "favorite_model": "N/A", "favorite_language": "N/A"}

        if isinstance(user_id, str):
            user_id = ObjectId(user_id)

        # Total codes
        total_codes = db.codes.count_documents({"user_id": user_id})

        # Favorite model (most used)
        model_pipeline = [
            {"$match": {"user_id": user_id}},
            {"$group": {"_id": "$model_name", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 1}
        ]
        model_result = list(db.codes.aggregate(model_pipeline))
        favorite_model = model_result[0]['_id'] if model_result else "N/A"

        # Favorite language
        lang_pipeline = [
            {"$match": {"user_id": user_id}},
            {"$group": {"_id": "$language", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 1}
        ]
        lang_result = list(db.codes.aggregate(lang_pipeline))
        favorite_language = lang_result[0]['_id'] if lang_result else "N/A"

        return {
            "total_codes": total_codes,
            "favorite_model": favorite_model,
            "favorite_language": favorite_language
        }

    except Exception as e:
        print(f"Error getting user stats: {e}")
        return {"total_codes": 0, "favorite_model": "N/A", "favorite_language": "N/A"}

# ============================================================
# REVIEW FUNCTIONS
# ============================================================

def submit_review(user_id, rating, title, comment, category):
    """
    Submits a new review
    Args:
        user_id: User's ObjectId or string ID
        rating: 1-5 star rating
        title: Review title
        comment: Review comment
        category: "Feature Request", "Bug Report", or "General Feedback"
    Returns: Review document or None
    """
    try:
        db = get_database()
        if not db:
            return None

        if isinstance(user_id, str):
            user_id = ObjectId(user_id)

        review_doc = {
            "user_id": user_id,
            "rating": rating,
            "title": title,
            "comment": comment,
            "category": category,
            "status": "pending",
            "rejection_reason": "",
            "admin_response": "",
            "admin_id": None,
            "helpful_count": 0,
            "helpful_by": [],
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "moderated_at": None
        }

        result = db.reviews.insert_one(review_doc)
        review_doc['_id'] = result.inserted_id

        return review_doc

    except Exception as e:
        print(f"Error submitting review: {e}")
        return None

def get_reviews(status=None, limit=50):
    """
    Retrieves reviews with optional status filter
    Args:
        status: "pending", "approved", or "rejected" (None for all)
        limit: Number of reviews to return
    Returns: List of review documents
    """
    try:
        db = get_database()
        if not db:
            return []

        query = {}
        if status:
            query['status'] = status

        reviews = list(
            db.reviews.find(query)
            .limit(limit)
            .sort("created_at", DESCENDING)
        )

        return reviews

    except Exception as e:
        print(f"Error getting reviews: {e}")
        return []

def moderate_review(review_id, action, admin_id, reason=None, response=None):
    """
    Moderates a review (approve, reject, respond)
    Args:
        review_id: Review's ObjectId or string ID
        action: "approve", "reject", or "respond"
        admin_id: Admin user's ObjectId or string ID
        reason: Rejection reason (for reject action)
        response: Admin response (for respond action)
    Returns: Updated review document or None
    """
    try:
        db = get_database()
        if not db:
            return None

        if isinstance(review_id, str):
            review_id = ObjectId(review_id)
        if isinstance(admin_id, str):
            admin_id = ObjectId(admin_id)

        updates = {
            "admin_id": admin_id,
            "moderated_at": datetime.now(),
            "updated_at": datetime.now()
        }

        if action == "approve":
            updates['status'] = "approved"
        elif action == "reject":
            updates['status'] = "rejected"
            if reason:
                updates['rejection_reason'] = reason
        elif action == "respond":
            if response:
                updates['admin_response'] = response

        db.reviews.update_one(
            {"_id": review_id},
            {"$set": updates}
        )

        return db.reviews.find_one({"_id": review_id})

    except Exception as e:
        print(f"Error moderating review: {e}")
        return None

def vote_helpful(review_id, user_id):
    """
    Votes a review as helpful
    Args:
        review_id: Review's ObjectId or string ID
        user_id: User's ObjectId or string ID
    Returns: True if voted, False if already voted
    """
    try:
        db = get_database()
        if not db:
            return False

        if isinstance(review_id, str):
            review_id = ObjectId(review_id)
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)

        # Check if already voted
        review = db.reviews.find_one({"_id": review_id})
        if review and user_id in review.get('helpful_by', []):
            return False

        # Add vote
        db.reviews.update_one(
            {"_id": review_id},
            {
                "$inc": {"helpful_count": 1},
                "$push": {"helpful_by": user_id}
            }
        )

        return True

    except Exception as e:
        print(f"Error voting helpful: {e}")
        return False

def delete_review(review_id):
    """
    Deletes a review
    Args:
        review_id: Review's ObjectId or string ID
    Returns: True if deleted, False otherwise
    """
    try:
        db = get_database()
        if not db:
            return False

        if isinstance(review_id, str):
            review_id = ObjectId(review_id)

        result = db.reviews.delete_one({"_id": review_id})
        return result.deleted_count > 0

    except Exception as e:
        print(f"Error deleting review: {e}")
        return False

# ============================================================
# LOG FUNCTIONS
# ============================================================

def create_log(log_type, action, details, user_id=None, admin_id=None, severity="info"):
    """
    Creates a log entry
    Args:
        log_type: "user_action", "admin_action", "system_event", "security_event"
        action: Description of action
        details: Dict with additional context
        user_id: User's ObjectId or string ID (optional)
        admin_id: Admin's ObjectId or string ID (optional)
        severity: "info", "warning", "error", "critical"
    Returns: Log document or None
    """
    try:
        db = get_database()
        if not db:
            return None

        if user_id and isinstance(user_id, str):
            user_id = ObjectId(user_id)
        if admin_id and isinstance(admin_id, str):
            admin_id = ObjectId(admin_id)

        log_doc = {
            "type": log_type,
            "user_id": user_id,
            "admin_id": admin_id,
            "action": action,
            "details": details or {},
            "ip_address": "",  # To be filled from request context if available
            "user_agent": "",  # To be filled from request context if available
            "severity": severity,
            "created_at": datetime.now()
        }

        result = db.logs.insert_one(log_doc)
        log_doc['_id'] = result.inserted_id

        return log_doc

    except Exception as e:
        print(f"Error creating log: {e}")
        return None

def get_logs(filters=None, limit=50, offset=0):
    """
    Retrieves logs with optional filters
    Args:
        filters: Dict with type, user_id, severity, date_range
        limit: Number of logs to return
        offset: Number of logs to skip
    Returns: List of log documents
    """
    try:
        db = get_database()
        if not db:
            return []

        query = {}
        if filters:
            if filters.get('type'):
                query['type'] = filters['type']
            if filters.get('user_id'):
                query['user_id'] = ObjectId(filters['user_id']) if isinstance(filters['user_id'], str) else filters['user_id']
            if filters.get('severity'):
                query['severity'] = filters['severity']
            if filters.get('date_from') and filters.get('date_to'):
                query['created_at'] = {
                    "$gte": filters['date_from'],
                    "$lte": filters['date_to']
                }

        logs = list(
            db.logs.find(query)
            .skip(offset)
            .limit(limit)
            .sort("created_at", DESCENDING)
        )

        return logs

    except Exception as e:
        print(f"Error getting logs: {e}")
        return []

# ============================================================
# MODEL FUNCTIONS
# ============================================================

def record_model_usage(model_name, language, response_time, success):
    """
    Records model usage statistics
    Args:
        model_name: "gemma-2b", "phi-2", or "codebert"
        language: Programming language used
        response_time: Time taken in seconds
        success: True if successful, False if failed
    Returns: True if recorded, False otherwise
    """
    try:
        db = get_database()
        if not db:
            return False

        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # Find or create model stat document for today
        model_stat = db.models.find_one({
            "model_name": model_name,
            "date": today
        })

        if model_stat:
            # Update existing
            updates = {
                "$inc": {
                    "total_uses": 1,
                    "successful_uses": 1 if success else 0,
                    "failed_uses": 0 if success else 1,
                    "total_response_time": response_time,
                    f"languages_used.{language}": 1
                }
            }
            db.models.update_one(
                {"_id": model_stat['_id']},
                updates
            )

            # Recalculate average
            updated = db.models.find_one({"_id": model_stat['_id']})
            avg_time = updated['total_response_time'] / updated['total_uses']
            db.models.update_one(
                {"_id": model_stat['_id']},
                {"$set": {"average_response_time": avg_time}}
            )
        else:
            # Create new
            model_doc = {
                "model_name": model_name,
                "date": today,
                "total_uses": 1,
                "successful_uses": 1 if success else 0,
                "failed_uses": 0 if success else 1,
                "total_response_time": response_time,
                "average_response_time": response_time,
                "languages_used": {language: 1}
            }
            db.models.insert_one(model_doc)

        return True

    except Exception as e:
        print(f"Error recording model usage: {e}")
        return False

def get_model_stats(model_name, date_range=30):
    """
    Gets aggregated model statistics
    Args:
        model_name: "gemma-2b", "phi-2", or "codebert"
        date_range: Number of days to look back
    Returns: Dict with aggregated stats
    """
    try:
        db = get_database()
        if not db:
            return None

        date_from = datetime.now() - timedelta(days=date_range)

        pipeline = [
            {
                "$match": {
                    "model_name": model_name,
                    "date": {"$gte": date_from}
                }
            },
            {
                "$group": {
                    "_id": "$model_name",
                    "total_uses": {"$sum": "$total_uses"},
                    "successful_uses": {"$sum": "$successful_uses"},
                    "failed_uses": {"$sum": "$failed_uses"},
                    "avg_response_time": {"$avg": "$average_response_time"}
                }
            }
        ]

        result = list(db.models.aggregate(pipeline))

        if result:
            stats = result[0]
            stats['success_rate'] = (stats['successful_uses'] / stats['total_uses'] * 100) if stats['total_uses'] > 0 else 0
            return stats

        return {
            "total_uses": 0,
            "successful_uses": 0,
            "failed_uses": 0,
            "avg_response_time": 0,
            "success_rate": 0
        }

    except Exception as e:
        print(f"Error getting model stats: {e}")
        return None

# ============================================================
# CHALLENGE FUNCTIONS
# ============================================================

def get_daily_challenge(date):
    """
    Gets the daily challenge for a specific date
    Args:
        date: Date object
    Returns: Challenge document or None
    """
    try:
        db = get_database()
        if not db:
            return None

        challenge_date = date.replace(hour=0, minute=0, second=0, microsecond=0)

        return db.challenges_global.find_one({"date": challenge_date})

    except Exception as e:
        print(f"Error getting daily challenge: {e}")
        return None

def create_daily_challenge(date, difficulty, description, language, hint, solution):
    """
    Creates a new daily challenge
    Args:
        date: Date object
        difficulty: "Easy", "Medium", or "Hard"
        description: Challenge description
        language: Programming language
        hint: Hint text
        solution: Solution code
    Returns: Challenge document or None
    """
    try:
        db = get_database()
        if not db:
            return None

        challenge_date = date.replace(hour=0, minute=0, second=0, microsecond=0)

        challenge_doc = {
            "date": challenge_date,
            "difficulty": difficulty,
            "description": description,
            "language": language,
            "topic": "",  # Can be extracted from description
            "hint": hint,
            "solution": solution,
            "created_at": datetime.now()
        }

        result = db.challenges_global.insert_one(challenge_doc)
        challenge_doc['_id'] = result.inserted_id

        return challenge_doc

    except Exception as e:
        print(f"Error creating daily challenge: {e}")
        return None

def mark_challenge_complete(user_id, challenge_date):
    """
    Marks a challenge as completed for a user
    Args:
        user_id: User's ObjectId or string ID
        challenge_date: Date of the challenge
    Returns: True if marked, False otherwise
    """
    try:
        db = get_database()
        if not db:
            return False

        if isinstance(user_id, str):
            user_id = ObjectId(user_id)

        challenge_date = challenge_date.replace(hour=0, minute=0, second=0, microsecond=0)

        db.challenges.update_one(
            {"user_id": user_id, "challenge_date": challenge_date},
            {
                "$set": {
                    "completed": True,
                    "completed_at": datetime.now()
                }
            },
            upsert=True
        )

        return True

    except Exception as e:
        print(f"Error marking challenge complete: {e}")
        return False

def get_user_challenge_stats(user_id):
    """
    Gets user's challenge completion statistics
    Args:
        user_id: User's ObjectId or string ID
    Returns: Dict with completed_count and current_streak
    """
    try:
        db = get_database()
        if not db:
            return {"completed_count": 0, "current_streak": 0}

        if isinstance(user_id, str):
            user_id = ObjectId(user_id)

        # Count completed challenges
        completed_count = db.challenges.count_documents({
            "user_id": user_id,
            "completed": True
        })

        # Calculate streak (consecutive days)
        challenges = list(
            db.challenges.find({"user_id": user_id, "completed": True})
            .sort("challenge_date", DESCENDING)
        )

        streak = 0
        if challenges:
            current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            for challenge in challenges:
                if challenge['challenge_date'] == current_date - timedelta(days=streak):
                    streak += 1
                else:
                    break

        return {
            "completed_count": completed_count,
            "current_streak": streak
        }

    except Exception as e:
        print(f"Error getting user challenge stats: {e}")
        return {"completed_count": 0, "current_streak": 0}

# ============================================================
# LEADERBOARD FUNCTIONS
# ============================================================

def get_top_coders(limit=100):
    """
    Gets top users by code generation count
    Args:
        limit: Number of users to return
    Returns: List of dicts with user info and code count
    """
    try:
        db = get_database()
        if not db:
            return []

        pipeline = [
            {
                "$group": {
                    "_id": "$user_id",
                    "code_count": {"$sum": 1}
                }
            },
            {
                "$sort": {"code_count": -1}
            },
            {
                "$limit": limit
            },
            {
                "$lookup": {
                    "from": "users",
                    "localField": "_id",
                    "foreignField": "_id",
                    "as": "user"
                }
            },
            {
                "$unwind": "$user"
            },
            {
                "$project": {
                    "user_id": "$_id",
                    "name": "$user.name",
                    "email": "$user.email",
                    "avatar_url": "$user.avatar_url",
                    "code_count": 1
                }
            }
        ]

        results = list(db.codes.aggregate(pipeline))
        return results

    except Exception as e:
        print(f"Error getting top coders: {e}")
        return []

def get_top_contributors(limit=100):
    """
    Gets top users by review contribution score
    Args:
        limit: Number of users to return
    Returns: List of dicts with user info and score
    """
    try:
        db = get_database()
        if not db:
            return []

        pipeline = [
            {
                "$match": {"status": "approved"}
            },
            {
                "$group": {
                    "_id": "$user_id",
                    "review_count": {"$sum": 1},
                    "helpful_votes": {"$sum": "$helpful_count"}
                }
            },
            {
                "$addFields": {
                    "score": {
                        "$add": [
                            {"$multiply": ["$review_count", 10]},
                            "$helpful_votes"
                        ]
                    }
                }
            },
            {
                "$sort": {"score": -1}
            },
            {
                "$limit": limit
            },
            {
                "$lookup": {
                    "from": "users",
                    "localField": "_id",
                    "foreignField": "_id",
                    "as": "user"
                }
            },
            {
                "$unwind": "$user"
            },
            {
                "$project": {
                    "user_id": "$_id",
                    "name": "$user.name",
                    "email": "$user.email",
                    "avatar_url": "$user.avatar_url",
                    "review_count": 1,
                    "helpful_votes": 1,
                    "score": 1
                }
            }
        ]

        results = list(db.reviews.aggregate(pipeline))
        return results

    except Exception as e:
        print(f"Error getting top contributors: {e}")
        return []

def get_model_masters(limit=100):
    """
    Gets users with most diverse model usage
    Args:
        limit: Number of users to return
    Returns: List of dicts with user info and diversity score
    """
    try:
        db = get_database()
        if not db:
            return []

        # This is a complex aggregation - getting percentage distribution per user
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "user_id": "$user_id",
                        "model": "$model_name"
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$group": {
                    "_id": "$_id.user_id",
                    "models": {
                        "$push": {
                            "model": "$_id.model",
                            "count": "$count"
                        }
                    },
                    "total": {"$sum": "$count"}
                }
            },
            {
                "$lookup": {
                    "from": "users",
                    "localField": "_id",
                    "foreignField": "_id",
                    "as": "user"
                }
            },
            {
                "$unwind": "$user"
            },
            {
                "$project": {
                    "user_id": "$_id",
                    "name": "$user.name",
                    "email": "$user.email",
                    "avatar_url": "$user.avatar_url",
                    "models": 1,
                    "total": 1
                }
            }
        ]

        results = list(db.codes.aggregate(pipeline))

        # Calculate diversity score (minimum percentage across all models)
        for result in results:
            percentages = []
            for model_data in result['models']:
                percentage = (model_data['count'] / result['total']) * 100
                percentages.append(percentage)

            result['diversity_score'] = min(percentages) if percentages else 0

        # Sort by diversity score
        results.sort(key=lambda x: x['diversity_score'], reverse=True)

        return results[:limit]

    except Exception as e:
        print(f"Error getting model masters: {e}")
        return []

# ============================================================
# ANALYTICS FUNCTIONS
# ============================================================

def get_platform_stats():
    """
    Gets overall platform statistics
    Returns: Dict with various platform metrics
    """
    try:
        db = get_database()
        if not db:
            return {}

        total_users = db.users.count_documents({})
        total_codes = db.codes.count_documents({})
        pending_reviews = db.reviews.count_documents({"status": "pending"})

        # Active today (users with activity in last 24 hours)
        yesterday = datetime.now() - timedelta(days=1)
        active_today = db.codes.distinct("user_id", {"created_at": {"$gte": yesterday}})

        return {
            "total_users": total_users,
            "total_codes": total_codes,
            "pending_reviews": pending_reviews,
            "active_today": len(active_today)
        }

    except Exception as e:
        print(f"Error getting platform stats: {e}")
        return {}
