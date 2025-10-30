"""
CodeGalaxy - Authentication Module
Handles all authentication flows: Email/OTP, Google OAuth, GitHub OAuth, Admin login
"""

import streamlit as st
import os
from datetime import datetime
import database
import utils
import email_service

# ============================================================
# LOGIN PAGE
# ============================================================

import mock_database

def show_login_page():
    """
    Bypasses the login page and automatically authenticates a mock user
    based on the 'view' query parameter. Defaults to 'admin'.
    """
    query_params = st.query_params
    view = query_params.get('view', 'admin')

    if view == "admin":
        st.session_state['user'] = mock_database.MOCK_USERS["admin_1"]
        st.session_state['is_admin'] = True
    else:
        st.session_state['user'] = mock_database.MOCK_USERS["user_1"]
        st.session_state['is_admin'] = False

    st.session_state['authenticated'] = True
    st.rerun()

# ============================================================
# SIGNUP PAGE
# ============================================================

def show_signup_page():
    """
    Displays the signup page with OTP verification
    """
    st.markdown("### Create Your Account")

    if 'signup_step' not in st.session_state:
        st.session_state['signup_step'] = 'form'
    if 'signup_email' not in st.session_state:
        st.session_state['signup_email'] = ''

    if st.session_state['signup_step'] == 'form':
        # Signup form
        name = st.text_input("Full Name", placeholder="John Doe")
        email = st.text_input("Email", placeholder="your@email.com")
        password = st.text_input("Password", type="password", placeholder="At least 8 characters")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Sign Up", use_container_width=True, type="primary"):
                # Validation
                if not name or not email or not password or not confirm_password:
                    st.error("All fields are required")
                elif not utils.validate_email(email):
                    st.error("Please enter a valid email address")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    # Validate password strength
                    password_check = utils.validate_password_strength(password)
                    if not password_check['valid']:
                        for error in password_check['errors']:
                            st.error(error)
                    else:
                        # Check if email already exists
                        existing_user = database.get_user_by_email(email)
                        if existing_user:
                            st.error("Email already registered. Please login instead.")
                        else:
                            # Generate and send OTP
                            otp_code = database.create_otp(email, "signup")
                            if otp_code:
                                # Send OTP email
                                email_sent = email_service.send_otp_email(email, otp_code, "signup")

                                if email_sent:
                                    # Store signup data temporarily
                                    st.session_state['signup_data'] = {
                                        'name': name,
                                        'email': email,
                                        'password': password
                                    }
                                    st.session_state['signup_email'] = email
                                    st.session_state['signup_step'] = 'verify'
                                    st.success(f"OTP sent to {email}! Please check your inbox.")
                                    st.rerun()
                                else:
                                    st.warning("⚠️ Email service not configured. Creating account without OTP verification (development mode).")
                                    # Fallback: Create account directly without OTP
                                    user = database.create_user(
                                        name=name,
                                        email=email,
                                        password=password,
                                        auth_provider="email"
                                    )
                                    if user:
                                        st.session_state['authenticated'] = True
                                        st.session_state['user'] = user
                                        st.session_state['is_admin'] = False
                                        st.success("✅ Account created successfully! Welcome to CodeGalaxy! 🚀")
                                        st.rerun()
                                    else:
                                        st.error("Failed to create account. Please check database connection.")
                            else:
                                # Fallback: Database not connected, create account directly
                                st.warning("⚠️ Database OTP service unavailable. Creating account without OTP verification (development mode).")
                                user = database.create_user(
                                    name=name,
                                    email=email,
                                    password=password,
                                    auth_provider="email"
                                )
                                if user:
                                    st.session_state['authenticated'] = True
                                    st.session_state['user'] = user
                                    st.session_state['is_admin'] = False

                                    # Log signup action if possible
                                    try:
                                        database.create_log(
                                            "user_action",
                                            "signup",
                                            {"email": user['email'], "method": "email_no_otp"},
                                            user_id=user['_id']
                                        )
                                    except:
                                        pass  # Database logging might fail too

                                    st.success("✅ Account created successfully! Welcome to CodeGalaxy! 🚀")
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to create account. Please check database connection and try again.")

        with col2:
            if st.button("Back to Login", use_container_width=True):
                st.session_state['auth_mode'] = 'login'
                st.rerun()

    elif st.session_state['signup_step'] == 'verify':
        # OTP verification
        st.info(f"We've sent a 6-digit code to {st.session_state['signup_email']}")

        otp_input = st.text_input("Enter OTP Code", max_chars=6, placeholder="123456")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Verify & Sign Up", use_container_width=True, type="primary"):
                if not otp_input or len(otp_input) != 6:
                    st.error("Please enter a valid 6-digit code")
                else:
                    # Verify OTP
                    is_valid = database.verify_otp(
                        st.session_state['signup_email'],
                        otp_input,
                        "signup"
                    )

                    if is_valid:
                        # Create user account
                        signup_data = st.session_state['signup_data']
                        user = database.create_user(
                            name=signup_data['name'],
                            email=signup_data['email'],
                            password=signup_data['password'],
                            auth_provider="email"
                        )

                        if user:
                            # Log the user in
                            st.session_state['authenticated'] = True
                            st.session_state['user'] = user
                            st.session_state['is_admin'] = False

                            # Send welcome email
                            email_service.send_welcome_email(user['email'], user['name'])

                            # Log signup action
                            database.create_log(
                                "user_action",
                                "signup",
                                {"email": user['email'], "method": "email"},
                                user_id=user['_id']
                            )

                            # Clean up session
                            del st.session_state['signup_data']
                            del st.session_state['signup_step']
                            st.session_state['auth_mode'] = 'login'

                            st.success("Account created successfully! Welcome to CodeGalaxy! 🚀")
                            st.rerun()
                        else:
                            st.error("Failed to create account. Please try again.")
                    else:
                        st.error("Invalid or expired OTP. Please try again.")

        with col2:
            if st.button("Resend OTP", use_container_width=True):
                # Generate new OTP
                otp_code = database.create_otp(st.session_state['signup_email'], "signup")
                if otp_code:
                    email_sent = email_service.send_otp_email(
                        st.session_state['signup_email'],
                        otp_code,
                        "signup"
                    )
                    if email_sent:
                        st.success("New OTP sent!")
                    else:
                        st.error("Failed to send OTP.")

        if st.button("← Back to Signup Form"):
            st.session_state['signup_step'] = 'form'
            st.rerun()

# ============================================================
# FORGOT PASSWORD
# ============================================================

def show_forgot_password():
    """
    Displays forgot password flow with OTP
    """
    st.markdown("### Reset Your Password")

    if 'reset_step' not in st.session_state:
        st.session_state['reset_step'] = 'email'

    if st.session_state['reset_step'] == 'email':
        # Request OTP
        st.write("Enter your email address and we'll send you a code to reset your password.")

        email = st.text_input("Email", placeholder="your@email.com")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Send Reset Code", use_container_width=True, type="primary"):
                if not email:
                    st.error("Please enter your email address")
                elif not utils.validate_email(email):
                    st.error("Please enter a valid email address")
                else:
                    # Check if user exists (but don't reveal if not for security)
                    user = database.get_user_by_email(email)

                    # Generate OTP regardless (security: don't reveal if email exists)
                    otp_code = database.create_otp(email, "password_reset")

                    if otp_code and user:
                        email_sent = email_service.send_otp_email(email, otp_code, "password_reset")

                        if email_sent:
                            st.session_state['reset_email'] = email
                            st.session_state['reset_step'] = 'verify'
                            st.success("If this email exists, an OTP has been sent.")
                            st.rerun()

                    # Always show this message for security
                    st.success("If this email exists, an OTP has been sent.")

        with col2:
            if st.button("Back to Login", use_container_width=True):
                st.session_state['auth_mode'] = 'login'
                st.rerun()

    elif st.session_state['reset_step'] == 'verify':
        # Verify OTP and reset password
        st.info(f"Enter the code sent to {st.session_state.get('reset_email', 'your email')}")

        otp_input = st.text_input("OTP Code", max_chars=6, placeholder="123456")
        new_password = st.text_input("New Password", type="password", placeholder="Enter new password")
        confirm_new = st.text_input("Confirm New Password", type="password", placeholder="Re-enter new password")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Reset Password", use_container_width=True, type="primary"):
                if not otp_input or not new_password or not confirm_new:
                    st.error("All fields are required")
                elif new_password != confirm_new:
                    st.error("Passwords do not match")
                else:
                    # Validate new password
                    password_check = utils.validate_password_strength(new_password)
                    if not password_check['valid']:
                        for error in password_check['errors']:
                            st.error(error)
                    else:
                        # Verify OTP
                        is_valid = database.verify_otp(
                            st.session_state['reset_email'],
                            otp_input,
                            "password_reset"
                        )

                        if is_valid:
                            # Get user and update password
                            user = database.get_user_by_email(st.session_state['reset_email'])

                            if user:
                                # Update password
                                hashed_password = utils.hash_password(new_password)
                                updated_user = database.update_user(
                                    user['_id'],
                                    {'password': hashed_password}
                                )

                                if updated_user:
                                    # Send confirmation email
                                    email_service.send_password_reset_success_email(
                                        user['email'],
                                        user['name']
                                    )

                                    # Log password reset
                                    database.create_log(
                                        "user_action",
                                        "password_reset",
                                        {"email": user['email']},
                                        user_id=user['_id']
                                    )

                                    # Clean up session
                                    del st.session_state['reset_step']
                                    del st.session_state['reset_email']
                                    st.session_state['auth_mode'] = 'login'

                                    st.success("Password reset successful! You can now log in with your new password.")
                                    st.rerun()
                                else:
                                    st.error("Failed to update password. Please try again.")
                            else:
                                st.error("User not found.")
                        else:
                            st.error("Invalid or expired OTP.")

        with col2:
            if st.button("Resend OTP", use_container_width=True):
                otp_code = database.create_otp(st.session_state['reset_email'], "password_reset")
                if otp_code:
                    email_sent = email_service.send_otp_email(
                        st.session_state['reset_email'],
                        otp_code,
                        "password_reset"
                    )
                    if email_sent:
                        st.success("New OTP sent!")

        if st.button("← Back"):
            st.session_state['reset_step'] = 'email'
            st.rerun()

# ============================================================
# ADMIN LOGIN
# ============================================================

def show_admin_login():
    """
    Displays admin login page (simple password-based)
    """
    st.markdown("### Admin Login")

    st.warning("🔒 This is the admin area. Authorized personnel only.")

    admin_password = st.text_input("Admin Password", type="password", placeholder="Enter admin password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login as Admin", use_container_width=True, type="primary"):
            if not admin_password:
                st.error("Please enter admin password")
            else:
                # Verify admin password
                correct_password = os.getenv('ADMIN_PASSWORD', 'Infosys')

                if admin_password == correct_password:
                    # Admin login successful
                    st.session_state['authenticated'] = True
                    st.session_state['is_admin'] = True
                    st.session_state['user'] = {
                        'name': 'Admin',
                        'email': os.getenv('ADMIN_EMAIL', 'admin@codegalaxy.com'),
                        'role': 'admin'
                    }

                    # Log admin login
                    database.create_log(
                        "admin_action",
                        "admin_login",
                        {"source": "admin_portal"},
                        severity="info"
                    )

                    st.success("Admin login successful!")
                    st.rerun()
                else:
                    st.error("Invalid admin password")

                    # Log failed admin login
                    database.create_log(
                        "security_event",
                        "failed_admin_login",
                        {"attempt": "admin_portal"},
                        severity="warning"
                    )

    with col2:
        if st.button("Back to User Login", use_container_width=True):
            st.query_params.clear()
            st.rerun()

# ============================================================
# GOOGLE OAUTH (Placeholder)
# ============================================================

def handle_google_oauth():
    """
    Handles Google OAuth flow
    Note: This is a simplified placeholder. Full OAuth implementation requires
    proper redirect URIs, state management, and token exchange.
    """
    try:
        from google_auth_oauthlib.flow import Flow
        from google.auth.transport.requests import Request

        google_client_id = os.getenv('GOOGLE_CLIENT_ID')
        google_client_secret = os.getenv('GOOGLE_CLIENT_SECRET')

        if not google_client_id or not google_client_secret:
            st.error("Google OAuth credentials not configured")
            return

        # In a real implementation:
        # 1. Create OAuth flow with redirect URI
        # 2. Generate authorization URL
        # 3. Redirect user to Google
        # 4. Handle callback with authorization code
        # 5. Exchange code for tokens
        # 6. Fetch user profile
        # 7. Create or login user

        st.info("Google OAuth requires proper configuration with redirect URIs and Google Cloud Console setup.")

    except Exception as e:
        st.error(f"OAuth error: {e}")

# ============================================================
# GITHUB OAUTH (Placeholder)
# ============================================================

def handle_github_oauth():
    """
    Handles GitHub OAuth flow
    Note: This is a simplified placeholder. Full OAuth implementation requires
    proper redirect URIs, state management, and token exchange.
    """
    try:
        github_client_id = os.getenv('GITHUB_CLIENT_ID')
        github_client_secret = os.getenv('GITHUB_CLIENT_SECRET')

        if not github_client_id or not github_client_secret:
            st.error("GitHub OAuth credentials not configured")
            return

        # In a real implementation:
        # 1. Create GitHub OAuth authorization URL
        # 2. Redirect user to GitHub
        # 3. Handle callback with authorization code
        # 4. Exchange code for access token
        # 5. Fetch user profile from GitHub API
        # 6. Create or login user

        st.info("GitHub OAuth requires proper configuration with OAuth App setup in GitHub Developer Settings.")

    except Exception as e:
        st.error(f"OAuth error: {e}")

# ============================================================
# LOGOUT
# ============================================================

def logout():
    """
    Logs out the current user and clears session
    """
    try:
        # Log logout action
        if st.session_state.get('user'):
            database.create_log(
                "user_action",
                "logout",
                {"email": st.session_state['user'].get('email')},
                user_id=st.session_state['user'].get('_id')
            )

        # Clear all session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]

        st.success("Logged out successfully!")
        st.rerun()

    except Exception as e:
        st.error(f"Logout error: {e}")
