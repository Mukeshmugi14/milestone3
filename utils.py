"""
CodeGalaxy - Utility Functions
Helper functions for validation, formatting, and common operations
"""

import bcrypt
import re
import random
import string
from datetime import datetime, timedelta
import uuid

# ============================================================
# PASSWORD FUNCTIONS
# ============================================================

def hash_password(password):
    """
    Hashes password using bcrypt
    Args:
        password: Plain text password
    Returns: Hashed password string
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8')

def verify_password(password, hashed):
    """
    Verifies password against hash
    Args:
        password: Plain text password
        hashed: Hashed password
    Returns: Boolean
    """
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False

# ============================================================
# VALIDATION FUNCTIONS
# ============================================================

def validate_email(email):
    """
    Validates email format using regex
    Args:
        email: Email address to validate
    Returns: Boolean
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password_strength(password, min_length=8, require_uppercase=True,
                               require_numbers=True, require_special=True):
    """
    Validates password strength based on requirements
    Args:
        password: Password to validate
        min_length: Minimum password length
        require_uppercase: Require at least one uppercase letter
        require_numbers: Require at least one number
        require_special: Require at least one special character
    Returns: Dict with {valid: Boolean, errors: List of error messages}
    """
    errors = []

    if len(password) < min_length:
        errors.append(f"Password must be at least {min_length} characters long")

    if require_uppercase and not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")

    if require_numbers and not re.search(r'\d', password):
        errors.append("Password must contain at least one number")

    if require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Password must contain at least one special character")

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }

# ============================================================
# TEXT FORMATTING FUNCTIONS
# ============================================================

def truncate_text(text, max_length, add_ellipsis=True):
    """
    Truncates text to maximum length
    Args:
        text: Text to truncate
        max_length: Maximum length
        add_ellipsis: Add "..." if truncated
    Returns: Truncated string
    """
    if len(text) <= max_length:
        return text

    truncated = text[:max_length]
    if add_ellipsis:
        truncated += "..."

    return truncated

def format_timestamp(datetime_obj, format_type="relative"):
    """
    Formats datetime for display
    Args:
        datetime_obj: datetime object
        format_type: "relative" (e.g., "2 hours ago"), "short" (e.g., "Jan 15, 2025"),
                     "full" (e.g., "January 15, 2025 10:30 AM")
    Returns: Formatted string
    """
    if not datetime_obj:
        return "N/A"

    if format_type == "relative":
        now = datetime.now()
        diff = now - datetime_obj

        seconds = diff.total_seconds()

        if seconds < 60:
            return "just now"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif seconds < 604800:
            days = int(seconds / 86400)
            return f"{days} day{'s' if days != 1 else ''} ago"
        elif seconds < 2592000:
            weeks = int(seconds / 604800)
            return f"{weeks} week{'s' if weeks != 1 else ''} ago"
        else:
            months = int(seconds / 2592000)
            return f"{months} month{'s' if months != 1 else ''} ago"

    elif format_type == "short":
        return datetime_obj.strftime("%b %d, %Y")

    elif format_type == "full":
        return datetime_obj.strftime("%B %d, %Y %I:%M %p")

    return str(datetime_obj)

# ============================================================
# CODE GENERATION FUNCTIONS
# ============================================================

def generate_random_code(length=6):
    """
    Generates random numeric code
    Args:
        length: Length of code (default 6)
    Returns: String of random digits
    """
    return ''.join(random.choices(string.digits, k=length))

def generate_unique_id():
    """
    Generates unique ID
    Returns: Unique string ID
    """
    return str(uuid.uuid4())

# ============================================================
# PRIVACY FUNCTIONS
# ============================================================

def mask_ip_address(ip):
    """
    Masks IP address for privacy
    Args:
        ip: IP address string (e.g., "192.168.1.100")
    Returns: Masked IP string (e.g., "xxx.xxx.1.100")
    """
    if not ip:
        return "xxx.xxx.xxx.xxx"

    parts = ip.split('.')
    if len(parts) == 4:
        return f"xxx.xxx.{parts[2]}.{parts[3]}"

    return "xxx.xxx.xxx.xxx"

def mask_email(email):
    """
    Masks email address for privacy
    Args:
        email: Email address (e.g., "john.doe@example.com")
    Returns: Masked email (e.g., "j***e@example.com")
    """
    if not email or '@' not in email:
        return email

    local, domain = email.split('@', 1)

    if len(local) <= 2:
        masked_local = local[0] + '*'
    else:
        masked_local = local[0] + '*' * (len(local) - 2) + local[-1]

    return f"{masked_local}@{domain}"

# ============================================================
# USER AGENT PARSING
# ============================================================

def parse_user_agent(user_agent_string):
    """
    Parses user agent to extract device and browser info
    Args:
        user_agent_string: User agent string
    Returns: Dict with {device: str, browser: str}
    """
    if not user_agent_string:
        return {"device": "Unknown", "browser": "Unknown"}

    user_agent_lower = user_agent_string.lower()

    # Detect device
    device = "Desktop"
    if "mobile" in user_agent_lower or "android" in user_agent_lower or "iphone" in user_agent_lower:
        device = "Mobile"
    elif "tablet" in user_agent_lower or "ipad" in user_agent_lower:
        device = "Tablet"

    # Detect browser
    browser = "Unknown"
    if "chrome" in user_agent_lower and "edge" not in user_agent_lower:
        browser = "Chrome"
    elif "safari" in user_agent_lower and "chrome" not in user_agent_lower:
        browser = "Safari"
    elif "firefox" in user_agent_lower:
        browser = "Firefox"
    elif "edge" in user_agent_lower or "edg" in user_agent_lower:
        browser = "Edge"
    elif "opera" in user_agent_lower or "opr" in user_agent_lower:
        browser = "Opera"

    return {"device": device, "browser": browser}

# ============================================================
# CALCULATION FUNCTIONS
# ============================================================

def calculate_diversity_score(model_usage_counts):
    """
    Calculates diversity score based on model usage
    Args:
        model_usage_counts: Dict with model names and counts {model: count}
    Returns: Diversity score (0-100)
    """
    if not model_usage_counts or len(model_usage_counts) == 0:
        return 0

    total = sum(model_usage_counts.values())
    if total == 0:
        return 0

    # Calculate percentages
    percentages = [(count / total) * 100 for count in model_usage_counts.values()]

    # Diversity score is the minimum percentage (encourages balanced usage)
    return min(percentages)

def calculate_review_score(review_count, helpful_votes):
    """
    Calculates contributor score
    Args:
        review_count: Number of approved reviews
        helpful_votes: Number of helpful votes received
    Returns: Score (integer)
    """
    return (review_count * 10) + helpful_votes

# ============================================================
# SEARCH FUNCTIONS
# ============================================================

def fuzzy_search(query, text, threshold=0.6):
    """
    Performs fuzzy matching between query and text
    Args:
        query: Search query
        text: Text to search in
        threshold: Similarity threshold (0-1)
    Returns: Boolean (True if match)
    """
    if not query or not text:
        return False

    query_lower = query.lower()
    text_lower = text.lower()

    # Simple substring match
    if query_lower in text_lower:
        return True

    # Check word-by-word
    query_words = query_lower.split()
    text_words = text_lower.split()

    match_count = sum(1 for word in query_words if word in text_words)
    match_ratio = match_count / len(query_words) if query_words else 0

    return match_ratio >= threshold

def sanitize_input(text):
    """
    Removes potentially harmful characters from input
    Args:
        text: Input text to sanitize
    Returns: Sanitized string
    """
    if not text:
        return ""

    # Remove potential script tags
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)

    # Remove potential SQL injection characters in specific contexts
    # (Note: Parameterized queries are the main defense, this is additional)
    dangerous_patterns = [
        r'--',  # SQL comment
        r';.*?(drop|delete|insert|update|select).*?',  # SQL commands
    ]

    for pattern in dangerous_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)

    return text.strip()

# ============================================================
# FILE FUNCTIONS
# ============================================================

def validate_file_upload(file, allowed_extensions=['jpg', 'jpeg', 'png'], max_size_mb=5):
    """
    Validates uploaded file
    Args:
        file: Uploaded file object
        allowed_extensions: List of allowed file extensions
        max_size_mb: Maximum file size in MB
    Returns: Dict with {valid: Boolean, error: str}
    """
    if not file:
        return {"valid": False, "error": "No file provided"}

    # Check extension
    file_extension = file.name.split('.')[-1].lower()
    if file_extension not in allowed_extensions:
        return {
            "valid": False,
            "error": f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
        }

    # Check size
    file_size_mb = file.size / (1024 * 1024)
    if file_size_mb > max_size_mb:
        return {
            "valid": False,
            "error": f"File too large. Maximum size: {max_size_mb}MB"
        }

    return {"valid": True, "error": None}

# ============================================================
# DATA EXPORT FUNCTIONS
# ============================================================

def export_to_txt(data_list, fields):
    """
    Exports list of dicts to TXT format
    Args:
        data_list: List of dictionaries
        fields: List of field names to include
    Returns: String in TXT format
    """
    output = []

    for i, item in enumerate(data_list, 1):
        output.append(f"{'=' * 50}")
        output.append(f"Item {i}")
        output.append(f"{'=' * 50}")

        for field in fields:
            value = item.get(field, 'N/A')
            if isinstance(value, datetime):
                value = format_timestamp(value, "full")
            output.append(f"{field}: {value}")

        output.append("")

    return "\n".join(output)

def export_to_csv(data_list, fields):
    """
    Exports list of dicts to CSV format
    Args:
        data_list: List of dictionaries
        fields: List of field names to include
    Returns: String in CSV format
    """
    import csv
    import io

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fields, extrasaction='ignore')

    writer.writeheader()

    for item in data_list:
        # Format datetime fields
        row = {}
        for field in fields:
            value = item.get(field, '')
            if isinstance(value, datetime):
                value = format_timestamp(value, "full")
            row[field] = value

        writer.writerow(row)

    return output.getvalue()

# ============================================================
# COLOR/BADGE FUNCTIONS
# ============================================================

def get_status_color(status):
    """
    Returns color for status badges
    Args:
        status: Status string
    Returns: Color string
    """
    status_colors = {
        "active": "success",
        "suspended": "danger",
        "pending": "warning",
        "approved": "success",
        "rejected": "danger",
        "completed": "success",
        "failed": "danger"
    }

    return status_colors.get(status.lower(), "default")

def get_difficulty_color(difficulty):
    """
    Returns color for difficulty badges
    Args:
        difficulty: Difficulty string
    Returns: Color string
    """
    difficulty_colors = {
        "easy": "success",
        "medium": "warning",
        "hard": "danger"
    }

    return difficulty_colors.get(difficulty.lower(), "info")

# ============================================================
# RATE LIMITING FUNCTIONS
# ============================================================

def check_rate_limit(user_id, action, limit_per_hour, cache_dict):
    """
    Checks if user has exceeded rate limit
    Args:
        user_id: User's ID
        action: Action being rate limited
        limit_per_hour: Maximum actions per hour
        cache_dict: Dictionary to store rate limit data
    Returns: Dict with {allowed: Boolean, remaining: int, reset_time: datetime}
    """
    key = f"{user_id}_{action}"
    current_time = datetime.now()

    if key not in cache_dict:
        cache_dict[key] = {
            "count": 1,
            "reset_time": current_time + timedelta(hours=1)
        }
        return {
            "allowed": True,
            "remaining": limit_per_hour - 1,
            "reset_time": cache_dict[key]["reset_time"]
        }

    # Check if time window has reset
    if current_time >= cache_dict[key]["reset_time"]:
        cache_dict[key] = {
            "count": 1,
            "reset_time": current_time + timedelta(hours=1)
        }
        return {
            "allowed": True,
            "remaining": limit_per_hour - 1,
            "reset_time": cache_dict[key]["reset_time"]
        }

    # Increment count
    cache_dict[key]["count"] += 1

    allowed = cache_dict[key]["count"] <= limit_per_hour
    remaining = max(0, limit_per_hour - cache_dict[key]["count"])

    return {
        "allowed": allowed,
        "remaining": remaining,
        "reset_time": cache_dict[key]["reset_time"]
    }

# ============================================================
# CHART DATA FORMATTING
# ============================================================

def prepare_chart_data(data_list, x_field, y_field):
    """
    Prepares data for charting libraries
    Args:
        data_list: List of dictionaries
        x_field: Field name for X axis
        y_field: Field name for Y axis
    Returns: Dict with {x: List, y: List}
    """
    x_data = []
    y_data = []

    for item in data_list:
        x_value = item.get(x_field)
        y_value = item.get(y_field)

        if x_value is not None and y_value is not None:
            x_data.append(x_value)
            y_data.append(y_value)

    return {"x": x_data, "y": y_data}

# ============================================================
# NOTIFICATION HELPERS
# ============================================================

def should_send_notification(user_preferences, notification_type):
    """
    Checks if notification should be sent based on user preferences
    Args:
        user_preferences: Dict with user notification preferences
        notification_type: Type of notification
    Returns: Boolean
    """
    if not user_preferences:
        return True  # Default to sending if no preferences

    # Check if user has email notifications enabled
    if not user_preferences.get('email_notifications', True):
        return False

    # Additional type-specific checks can be added here

    return True
