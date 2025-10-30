"""
CodeGalaxy - Review System
Review submission and moderation workflows
"""

import database
import email_service

def submit_user_review(user_id, rating, title, comment, category):
    """
    Submits a review from user with validation
    """
    # Validate inputs
    if not title or not comment:
        return {"success": False, "error": "Title and comment are required"}

    if rating < 1 or rating > 5:
        return {"success": False, "error": "Rating must be between 1 and 5"}

    # Submit review
    review = database.submit_review(user_id, rating, title, comment, category)

    if review:
        # Log action
        database.create_log(
            "user_action",
            "review_submitted",
            {"review_id": str(review['_id']), "rating": rating},
            user_id=user_id
        )

        return {"success": True, "review_id": str(review['_id'])}
    else:
        return {"success": False, "error": "Failed to submit review"}

def moderate_review_action(review_id, action, admin_id, reason=None, response=None):
    """
    Performs moderation action on review
    """
    # Moderate review
    updated_review = database.moderate_review(review_id, action, admin_id, reason, response)

    if updated_review:
        # If responding, send email to user
        if action == "respond" and response:
            user = database.get_user_by_id(updated_review['user_id'])
            if user:
                email_service.send_review_response_email(
                    user['email'],
                    user['name'],
                    updated_review['title'],
                    response
                )

        # Log admin action
        database.create_log(
            "admin_action",
            f"review_{action}",
            {"review_id": str(review_id), "action": action},
            admin_id=admin_id
        )

        return {"success": True}
    else:
        return {"success": False, "error": "Failed to moderate review"}

def get_approved_reviews_for_display(limit=50):
    """
    Gets all approved reviews for community display
    """
    return database.get_reviews(status="approved", limit=limit)
