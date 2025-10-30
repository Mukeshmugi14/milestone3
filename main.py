"""
CodeGalaxy - AI-Powered Code Generation Platform
Main entry point and routing logic
"""

import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="CodeGalaxy 🚀",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
def initialize_session_state():
    """Initialize all session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    if 'user' not in st.session_state:
        st.session_state['user'] = None
    if 'is_admin' not in st.session_state:
        st.session_state['is_admin'] = False
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'login'
    if 'theme' not in st.session_state:
        st.session_state['theme'] = 'dark'
    if 'last_activity' not in st.session_state:
        st.session_state['last_activity'] = None

# Load custom CSS
def load_custom_css():
    """Load custom CSS styles"""
    css_file_path = os.path.join(os.path.dirname(__file__), 'assets', 'styles.css')

    # Base CSS for glassmorphism (will be enhanced when assets/styles.css is created)
    base_css = """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Dark theme background */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }

    /* Glassmorphism card base */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }

    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
    }

    /* Gradient button */
    .gradient-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .gradient-button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 5px;
    }
    </style>
    """

    st.markdown(base_css, unsafe_allow_html=True)

    # Load additional CSS if file exists
    if os.path.exists(css_file_path):
        with open(css_file_path, 'r') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def check_session_timeout():
    """Check if session has timed out due to inactivity"""
    import datetime

    if st.session_state.get('last_activity'):
        timeout_minutes = int(os.getenv('SESSION_TIMEOUT', 60))
        now = datetime.datetime.now()
        last_activity = st.session_state['last_activity']

        time_diff = (now - last_activity).total_seconds() / 60

        if time_diff > timeout_minutes:
            # Session expired
            st.session_state['authenticated'] = False
            st.session_state['user'] = None
            st.session_state['is_admin'] = False
            st.warning("Session expired due to inactivity. Please log in again.")
            return True

    # Update last activity
    st.session_state['last_activity'] = datetime.datetime.now()
    return False

def main():
    """Main application routing logic"""
    # Initialize session state
    initialize_session_state()

    # Load custom CSS
    load_custom_css()

    # Check for admin route
    query_params = st.query_params
    is_admin_route = query_params.get('admin', False)

    # Check session timeout
    if st.session_state['authenticated']:
        if check_session_timeout():
            st.stop()

    # Routing logic
    if not st.session_state['authenticated']:
        # Not authenticated - show login page
        from auth import show_login_page
        show_login_page()

    elif st.session_state['is_admin'] and is_admin_route:
        # Admin authenticated and on admin route
        from admin_dashboard import show_admin_dashboard
        show_admin_dashboard()

    elif st.session_state['authenticated']:
        # Regular user authenticated or admin viewing user dashboard
        from user_dashboard import show_user_dashboard
        show_user_dashboard()

if __name__ == "__main__":
    main()
