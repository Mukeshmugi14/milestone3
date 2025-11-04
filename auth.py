"""
CodeGalaxy - Authentication Module
Handles all authentication flows using Firebase: Email/Password, Google, GitHub.
"""

import streamlit as st
import os
import database
import utils
from firebase_config import initialize_firebase
from firebase_admin import auth as admin_auth

# Initialize Firebase
auth = initialize_firebase()

# ============================================================
# LOGIN PAGE
# ============================================================

def show_login_page():
    """
    Displays the main login page with Firebase authentication options.
    """
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                       -webkit-background-clip: text;
                       -webkit-text-fill-color: transparent;
                       font-size: 48px;'>
                CodeGalaxy 🚀
            </h1>
            <p style='color: #999; font-size: 18px;'>AI-Powered Code Generation Platform</p>
        </div>
        """, unsafe_allow_html=True)

        auth_mode = st.session_state.get('auth_mode', 'login')

        if auth_mode == 'signup':
            show_signup_page()
            return
        elif auth_mode == 'forgot_password':
            show_forgot_password()
            return

        st.markdown("### Sign In")
        email = st.text_input("Email", key="login_email", placeholder="your@email.com")
        password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")

        if st.button("Sign In", use_container_width=True, type="primary"):
            handle_email_password_login(email, password)

        if st.button("Forgot Password?", use_container_width=True):
            st.session_state['auth_mode'] = 'forgot_password'
            st.rerun()

        st.markdown("---")
        st.markdown("### Or continue with")

        col_oauth1, col_oauth2 = st.columns(2)
        with col_oauth1:
            if st.button("🔵 Continue with Google", use_container_width=True):
                st.info("Google OAuth is not yet implemented.")
        with col_oauth2:
            if st.button("⚫ Continue with GitHub", use_container_width=True):
                st.info("GitHub OAuth is not yet implemented.")

        st.markdown("---")
        if st.button("Don't have an account? Create one", use_container_width=True):
            st.session_state['auth_mode'] = 'signup'
            st.rerun()

# ============================================================
# SIGNUP PAGE
# ============================================================

def show_signup_page():
    """
    Displays the signup page for creating a new account with Firebase.
    """
    st.markdown("### Create Your Account")
    name = st.text_input("Full Name", placeholder="John Doe")
    email = st.text_input("Email", placeholder="your@email.com")
    password = st.text_input("Password", type="password", placeholder="At least 8 characters")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")

    if st.button("Sign Up", use_container_width=True, type="primary"):
        handle_email_password_signup(name, email, password, confirm_password)

    if st.button("Back to Login", use_container_width=True):
        st.session_state['auth_mode'] = 'login'
        st.rerun()

# ============================================================
# FORGOT PASSWORD
# ============================================================

def show_forgot_password():
    """
    Displays the forgot password page to send a reset link via Firebase.
    """
    st.markdown("### Reset Your Password")
    email = st.text_input("Email", placeholder="your@email.com")

    if st.button("Send Reset Link", use_container_width=True, type="primary"):
        handle_password_reset(email)

    if st.button("Back to Login", use_container_width=True):
        st.session_state['auth_mode'] = 'login'
        st.rerun()

# ============================================================
# AUTHENTICATION HANDLERS
# ============================================================

def handle_email_password_login(email, password):
    """
    Handles the email and password login using Firebase.
    """
    if not email or not password:
        st.error("Please enter both email and password.")
        return

    try:
        user_record = auth.sign_in_with_email_and_password(email, password)
        user_info = user_record['user']
        firebase_user = admin_auth.get_user(user_info.uid)

        mongo_user = database.get_user_by_firebase_uid(firebase_user.uid)
        if not mongo_user:
            mongo_user = database.create_user(
                name=firebase_user.display_name or "User",
                email=firebase_user.email,
                firebase_uid=firebase_user.uid,
                auth_provider='email'
            )

        set_session_state(mongo_user)
        st.rerun()

    except Exception as e:
        st.error(f"Login failed: {e}")

def handle_email_password_signup(name, email, password, confirm_password):
    """
    Handles the email and password signup using Firebase.
    """
    if not all([name, email, password, confirm_password]):
        st.error("All fields are required.")
        return
    if password != confirm_password:
        st.error("Passwords do not match.")
        return

    password_check = utils.validate_password_strength(password)
    if not password_check['valid']:
        for error in password_check['errors']:
            st.error(error)
        return

    try:
        firebase_user = admin_auth.create_user(
            email=email,
            password=password,
            display_name=name,
            email_verified=False
        )

        database.create_user(
            name=name,
            email=email,
            firebase_uid=firebase_user.uid,
            auth_provider='email'
        )

        st.success("Account created successfully! Please log in.")
        st.session_state['auth_mode'] = 'login'
        st.rerun()

    except Exception as e:
        st.error(f"Signup failed: {e}")

def handle_password_reset(email):
    """
    Handles sending a password reset email using Firebase.
    """
    if not email:
        st.error("Please enter your email address.")
        return

    try:
        auth.send_password_reset_email(email)
        st.success("A password reset link has been sent to your email.")
    except Exception as e:
        st.error(f"Failed to send reset link: {e}")

def set_session_state(user):
    """
    Sets the session state upon successful login.
    """
    st.session_state['authenticated'] = True
    st.session_state['user'] = user
    st.session_state['is_admin'] = (user.get('role') == 'admin')

# ============================================================
# ADMIN LOGIN
# ============================================================
def show_admin_login():
    """
    Displays admin login page (simple password-based)
    """
    st.markdown("### Admin Login")
    st.warning("🔒 This is the admin area. Authorized personnel only.")

    # Use st.form to manage the admin login fields
    with st.form(key='admin_login_form'):
        admin_username = st.text_input("Admin Username", value="codeAdmin")
        admin_password = st.text_input("Admin Password", type="password", value="Admin@14")
        submit_button = st.form_submit_button(label="Login as Admin", use_container_width=True)

    if submit_button:
        # Verify admin credentials
        correct_username = os.getenv('ADMIN_USERNAME', 'codeAdmin')
        correct_password = os.getenv('ADMIN_PASSWORD', 'Admin@14')

        if admin_username == correct_username and admin_password == correct_password:
            # Admin login successful
            st.session_state['authenticated'] = True
            st.session_state['is_admin'] = True
            st.session_state['user'] = {
                'name': 'Admin',
                'email': os.getenv('ADMIN_EMAIL', 'admin@codegalaxy.com'),
                'role': 'admin'
            }
            st.success("Admin login successful!")
            st.rerun()
        else:
            st.error("Invalid admin username or password")
# ============================================================
# LOGOUT
# ============================================================

def logout():
    """
    Logs out the current user and clears the session state.
    """
    if 'user' in st.session_state:
        st.session_state.clear()
    st.success("Logged out successfully!")
    st.rerun()
