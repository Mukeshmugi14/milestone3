"""
CodeGalaxy - Email Service
Email sending for OTPs, notifications, and reports via Gmail SMTP
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

# ============================================================
# SMTP CONFIGURATION
# ============================================================

def get_smtp_connection():
    """
    Creates and returns SMTP connection
    Returns: SMTP object or None
    """
    try:
        email_user = os.getenv('EMAIL_USER')
        email_password = os.getenv('EMAIL_PASSWORD')

        if not email_user or not email_password:
            print("Email credentials not found in environment variables")
            return None

        # Connect to Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_password)

        return server

    except Exception as e:
        print(f"Failed to connect to SMTP server: {e}")
        return None

# ============================================================
# OTP EMAIL FUNCTIONS
# ============================================================

def send_otp_email(to_email, otp_code, purpose):
    """
    Sends OTP email to user
    Args:
        to_email: Recipient email address
        otp_code: 6-digit OTP code
        purpose: "signup", "password_reset", or "login"
    Returns: Boolean (success or failure)
    """
    try:
        # Determine subject and message based on purpose
        if purpose == "signup":
            subject = "Verify Your Email - CodeGalaxy 🚀"
            title = "Welcome to CodeGalaxy!"
            message_text = "Thank you for signing up. Please use the OTP code below to verify your email address."
        elif purpose == "password_reset":
            subject = "Reset Your Password - CodeGalaxy 🚀"
            title = "Password Reset Request"
            message_text = "You requested to reset your password. Use the OTP code below to proceed."
        else:
            subject = "Your Login Code - CodeGalaxy 🚀"
            title = "Login Verification"
            message_text = "Use the OTP code below to complete your login."

        # Create HTML email body
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 40px auto;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 40px;
                    border-radius: 16px;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                }}
                .content {{
                    background: white;
                    padding: 30px;
                    border-radius: 12px;
                }}
                h1 {{
                    color: #333;
                    margin-top: 0;
                }}
                .otp-box {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    font-size: 32px;
                    font-weight: bold;
                    text-align: center;
                    padding: 20px;
                    border-radius: 12px;
                    margin: 30px 0;
                    letter-spacing: 8px;
                }}
                .message {{
                    color: #666;
                    font-size: 16px;
                    line-height: 1.6;
                    margin: 20px 0;
                }}
                .warning {{
                    color: #e74c3c;
                    font-size: 14px;
                    margin-top: 20px;
                }}
                .footer {{
                    text-align: center;
                    color: white;
                    margin-top: 30px;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="content">
                    <h1>{title}</h1>
                    <p class="message">{message_text}</p>

                    <div class="otp-box">
                        {otp_code}
                    </div>

                    <p class="message">
                        This code will expire in <strong>10 minutes</strong>.
                    </p>

                    <p class="warning">
                        If you didn't request this code, please ignore this email.
                    </p>
                </div>

                <div class="footer">
                    <p>CodeGalaxy 🚀 - AI-Powered Code Generation</p>
                    <p>&copy; 2025 CodeGalaxy. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        return send_email(to_email, subject, html_body)

    except Exception as e:
        print(f"Error sending OTP email: {e}")
        return False

# ============================================================
# GENERIC EMAIL FUNCTION
# ============================================================

def send_email(to_email, subject, html_body):
    """
    Sends HTML email
    Args:
        to_email: Recipient email address
        subject: Email subject
        html_body: HTML email body
    Returns: Boolean (success or failure)
    """
    try:
        email_user = os.getenv('EMAIL_USER')

        if not email_user:
            print("Email user not found in environment variables")
            return False

        # Create message
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = f"CodeGalaxy <{email_user}>"
        message['To'] = to_email

        # Attach HTML body
        html_part = MIMEText(html_body, 'html')
        message.attach(html_part)

        # Connect and send
        server = get_smtp_connection()
        if not server:
            return False

        server.sendmail(email_user, to_email, message.as_string())
        server.quit()

        return True

    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# ============================================================
# WEEKLY REPORT EMAIL
# ============================================================

def send_weekly_report(user_email, user_name, stats):
    """
    Sends weekly activity report to user
    Args:
        user_email: User's email address
        user_name: User's name
        stats: Dict with codes_generated, favorite_model, favorite_language, leaderboard_rank
    Returns: Boolean (success or failure)
    """
    try:
        subject = "Your CodeGalaxy Weekly Report 🚀"

        # Extract stats
        codes_generated = stats.get('codes_generated', 0)
        favorite_model = stats.get('favorite_model', 'N/A')
        favorite_language = stats.get('favorite_language', 'N/A')
        leaderboard_rank = stats.get('leaderboard_rank', 'N/A')

        app_url = os.getenv('APP_URL', 'http://localhost:8501')

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 40px auto;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 40px;
                    border-radius: 16px;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                }}
                .content {{
                    background: white;
                    padding: 30px;
                    border-radius: 12px;
                }}
                h1 {{
                    color: #333;
                    margin-top: 0;
                }}
                .stats-grid {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 20px;
                    margin: 30px 0;
                }}
                .stat-card {{
                    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                    padding: 20px;
                    border-radius: 12px;
                    text-align: center;
                }}
                .stat-value {{
                    font-size: 32px;
                    font-weight: bold;
                    color: #667eea;
                    margin: 10px 0;
                }}
                .stat-label {{
                    color: #666;
                    font-size: 14px;
                }}
                .button {{
                    display: inline-block;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 15px 30px;
                    text-decoration: none;
                    border-radius: 12px;
                    margin: 10px;
                    font-weight: bold;
                }}
                .footer {{
                    text-align: center;
                    color: white;
                    margin-top: 30px;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="content">
                    <h1>Hi {user_name}! 👋</h1>
                    <p>Here's your weekly CodeGalaxy activity summary:</p>

                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-value">{codes_generated}</div>
                            <div class="stat-label">Codes Generated</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">#{leaderboard_rank}</div>
                            <div class="stat-label">Your Rank</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{favorite_model}</div>
                            <div class="stat-label">Favorite Model</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{favorite_language}</div>
                            <div class="stat-label">Favorite Language</div>
                        </div>
                    </div>

                    <p style="text-align: center; margin-top: 30px;">
                        <a href="{app_url}" class="button">Generate More Code</a>
                        <a href="{app_url}?page=challenges" class="button">Try Daily Challenge</a>
                    </p>
                </div>

                <div class="footer">
                    <p>CodeGalaxy 🚀 - AI-Powered Code Generation</p>
                    <p>You're receiving this because you enabled weekly reports in your settings.</p>
                    <p>&copy; 2025 CodeGalaxy. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        return send_email(user_email, subject, html_body)

    except Exception as e:
        print(f"Error sending weekly report: {e}")
        return False

# ============================================================
# REVIEW RESPONSE EMAIL
# ============================================================

def send_review_response_email(user_email, user_name, review_title, admin_response):
    """
    Sends admin response to user's review
    Args:
        user_email: User's email address
        user_name: User's name
        review_title: Title of the review
        admin_response: Admin's response text
    Returns: Boolean (success or failure)
    """
    try:
        subject = "Admin Response to Your Feedback - CodeGalaxy 🚀"

        app_url = os.getenv('APP_URL', 'http://localhost:8501')

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 40px auto;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 40px;
                    border-radius: 16px;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                }}
                .content {{
                    background: white;
                    padding: 30px;
                    border-radius: 12px;
                }}
                h1 {{
                    color: #333;
                    margin-top: 0;
                }}
                .review-box {{
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 12px;
                    border-left: 4px solid #667eea;
                    margin: 20px 0;
                }}
                .response-box {{
                    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                    padding: 20px;
                    border-radius: 12px;
                    margin: 20px 0;
                }}
                .button {{
                    display: inline-block;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 15px 30px;
                    text-decoration: none;
                    border-radius: 12px;
                    margin: 10px 0;
                    font-weight: bold;
                }}
                .footer {{
                    text-align: center;
                    color: white;
                    margin-top: 30px;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="content">
                    <h1>Hi {user_name}! 👋</h1>
                    <p>Thank you for your feedback! Our admin team has responded to your review.</p>

                    <div class="review-box">
                        <strong>Your Review:</strong>
                        <p>{review_title}</p>
                    </div>

                    <div class="response-box">
                        <strong>Admin Response:</strong>
                        <p>{admin_response}</p>
                    </div>

                    <p style="text-align: center; margin-top: 30px;">
                        <a href="{app_url}?page=reviews" class="button">View Your Reviews</a>
                    </p>
                </div>

                <div class="footer">
                    <p>CodeGalaxy 🚀 - AI-Powered Code Generation</p>
                    <p>&copy; 2025 CodeGalaxy. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        return send_email(user_email, subject, html_body)

    except Exception as e:
        print(f"Error sending review response email: {e}")
        return False

# ============================================================
# ADMIN ALERT EMAIL
# ============================================================

def send_admin_alert(alert_type, alert_message, details):
    """
    Sends alert email to admin
    Args:
        alert_type: Type of alert ("security", "error", "warning")
        alert_message: Alert message
        details: Dict with additional details
    Returns: Boolean (success or failure)
    """
    try:
        admin_email = os.getenv('ADMIN_EMAIL')

        if not admin_email:
            print("Admin email not found in environment variables")
            return False

        subject = f"CodeGalaxy Alert: {alert_type.upper()} - {alert_message}"

        details_html = ""
        for key, value in details.items():
            details_html += f"<p><strong>{key}:</strong> {value}</p>"

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 40px auto;
                    background: #e74c3c;
                    padding: 40px;
                    border-radius: 16px;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                }}
                .content {{
                    background: white;
                    padding: 30px;
                    border-radius: 12px;
                }}
                h1 {{
                    color: #e74c3c;
                    margin-top: 0;
                }}
                .alert-box {{
                    background: #fee;
                    padding: 20px;
                    border-radius: 12px;
                    border-left: 4px solid #e74c3c;
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    color: white;
                    margin-top: 30px;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="content">
                    <h1>⚠️ Alert: {alert_type.upper()}</h1>

                    <div class="alert-box">
                        <p><strong>Message:</strong> {alert_message}</p>
                        <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>

                    <h3>Details:</h3>
                    {details_html}
                </div>

                <div class="footer">
                    <p>CodeGalaxy Admin System</p>
                </div>
            </div>
        </body>
        </html>
        """

        return send_email(admin_email, subject, html_body)

    except Exception as e:
        print(f"Error sending admin alert: {e}")
        return False

# ============================================================
# PASSWORD RESET EMAIL
# ============================================================

def send_password_reset_success_email(user_email, user_name):
    """
    Sends confirmation email after successful password reset
    Args:
        user_email: User's email address
        user_name: User's name
    Returns: Boolean (success or failure)
    """
    try:
        subject = "Password Reset Successful - CodeGalaxy 🚀"

        app_url = os.getenv('APP_URL', 'http://localhost:8501')

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 40px auto;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 40px;
                    border-radius: 16px;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                }}
                .content {{
                    background: white;
                    padding: 30px;
                    border-radius: 12px;
                }}
                h1 {{
                    color: #333;
                    margin-top: 0;
                }}
                .success-icon {{
                    text-align: center;
                    font-size: 64px;
                    margin: 20px 0;
                }}
                .button {{
                    display: inline-block;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 15px 30px;
                    text-decoration: none;
                    border-radius: 12px;
                    margin: 10px 0;
                    font-weight: bold;
                }}
                .footer {{
                    text-align: center;
                    color: white;
                    margin-top: 30px;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="content">
                    <h1>Password Reset Successful</h1>
                    <div class="success-icon">✅</div>

                    <p>Hi {user_name},</p>

                    <p>Your password has been successfully reset. You can now log in with your new password.</p>

                    <p>If you didn't make this change, please contact us immediately.</p>

                    <p style="text-align: center; margin-top: 30px;">
                        <a href="{app_url}" class="button">Log In to CodeGalaxy</a>
                    </p>
                </div>

                <div class="footer">
                    <p>CodeGalaxy 🚀 - AI-Powered Code Generation</p>
                    <p>&copy; 2025 CodeGalaxy. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        return send_email(user_email, subject, html_body)

    except Exception as e:
        print(f"Error sending password reset success email: {e}")
        return False

# ============================================================
# WELCOME EMAIL
# ============================================================

def send_welcome_email(user_email, user_name):
    """
    Sends welcome email to new user after signup
    Args:
        user_email: User's email address
        user_name: User's name
    Returns: Boolean (success or failure)
    """
    try:
        subject = "Welcome to CodeGalaxy 🚀🌌"

        app_url = os.getenv('APP_URL', 'http://localhost:8501')

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 40px auto;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 40px;
                    border-radius: 16px;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                }}
                .content {{
                    background: white;
                    padding: 30px;
                    border-radius: 12px;
                }}
                h1 {{
                    color: #333;
                    margin-top: 0;
                }}
                .feature-list {{
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 12px;
                    margin: 20px 0;
                }}
                .feature-list li {{
                    margin: 10px 0;
                }}
                .button {{
                    display: inline-block;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 15px 30px;
                    text-decoration: none;
                    border-radius: 12px;
                    margin: 10px 0;
                    font-weight: bold;
                }}
                .footer {{
                    text-align: center;
                    color: white;
                    margin-top: 30px;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="content">
                    <h1>Welcome to CodeGalaxy! 🚀🌌</h1>

                    <p>Hi {user_name},</p>

                    <p>We're thrilled to have you join our community of developers! CodeGalaxy is your AI-powered code generation platform that makes coding faster and smarter.</p>

                    <div class="feature-list">
                        <strong>What you can do:</strong>
                        <ul>
                            <li>✨ Generate code with 3 AI models (Gemma-2B, Phi-2, CodeBERT)</li>
                            <li>📝 Explain and improve existing code</li>
                            <li>🕒 Save and manage your code history</li>
                            <li>🏆 Compete on the leaderboard</li>
                            <li>⚡ Complete daily coding challenges</li>
                            <li>💬 Share feedback and reviews</li>
                        </ul>
                    </div>

                    <p style="text-align: center; margin-top: 30px;">
                        <a href="{app_url}" class="button">Start Generating Code</a>
                    </p>
                </div>

                <div class="footer">
                    <p>CodeGalaxy 🚀 - AI-Powered Code Generation</p>
                    <p>Happy coding!</p>
                    <p>&copy; 2025 CodeGalaxy. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """

        return send_email(user_email, subject, html_body)

    except Exception as e:
        print(f"Error sending welcome email: {e}")
        return False
