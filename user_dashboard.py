"""
CodeGalaxy - User Dashboard
All user-facing pages: Home, Generate Code, History, Profile, Reviews, Support
"""

import streamlit as st
import mock_database as database
import ai_models
import utils
import ui_components
from datetime import datetime

# ============================================================
# MAIN DASHBOARD ROUTER
# ============================================================

def show_user_dashboard():
    """
    Main user dashboard with sidebar navigation
    """
    # Check authentication
    if not st.session_state.get('authenticated'):
        st.error("Please log in to access the dashboard")
        st.stop()

    user = st.session_state['user']

    # Sidebar navigation
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align: center; padding: 20px;'>
            <div style='font-size: 48px;'>🚀</div>
            <h2 style='margin: 10px 0;'>CodeGalaxy</h2>
        </div>
        """, unsafe_allow_html=True)

        # Initialize current_page if not exists
        if 'current_page' not in st.session_state:
            st.session_state['current_page'] = 'home'

        # Navigation menu
        pages = {
            "home": "🏠 Home",
            "generate": "✨ Generate Code",
            "history": "🕒 History",
            "profile": "👤 Profile",
            "reviews": "💬 Reviews",
            "support": "❓ Support"
        }

        for page_key, page_label in pages.items():
            if st.button(page_label, key=f"nav_{page_key}", use_container_width=True,
                        type="primary" if st.session_state['current_page'] == page_key else "secondary"):
                st.session_state['current_page'] = page_key
                st.rerun()

        st.markdown("---")

        # User profile section
        st.markdown(f"""
        <div style='text-align: center; padding: 10px;'>
            <div style='font-size: 48px; margin-bottom: 10px;'>👤</div>
            <div style='font-weight: bold;'>{user.get('name', 'User')}</div>
            <div style='color: #999; font-size: 12px;'>{user.get('email', '')}</div>
        </div>
        """, unsafe_allow_html=True)

        # Theme toggle
        theme = st.session_state.get('theme', 'dark')
        if st.button(f"🌓 {'Dark' if theme == 'light' else 'Light'} Mode", use_container_width=True):
            st.session_state['theme'] = 'light' if theme == 'dark' else 'dark'
            st.rerun()

        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            from auth import logout
            logout()

    # Route to appropriate page
    current_page = st.session_state['current_page']

    if current_page == 'home':
        show_home_page()
    elif current_page == 'generate':
        show_generate_page()
    elif current_page == 'history':
        show_history_page()
    elif current_page == 'profile':
        show_profile_page()
    elif current_page == 'reviews':
        show_reviews_page()
    elif current_page == 'support':
        show_support_page()

# ============================================================
# PAGE 1: HOME
# ============================================================

def show_home_page():
    """
    Home page with user stats and recent activity
    """
    user = st.session_state['user']

    st.markdown(ui_components.page_header(
        f"Welcome back, {user.get('name', 'User')}! 👋",
        "Your AI-powered code generation dashboard",
        "🌌"
    ), unsafe_allow_html=True)

    # Get user stats
    stats = database.get_user_code_stats(user['_id'])

    # Stats cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(ui_components.stats_card(
            stats.get('total_codes', 0),
            "Codes Generated",
            "📝"
        ), unsafe_allow_html=True)

    with col2:
        st.markdown(ui_components.stats_card(
            stats.get('favorite_model', 'N/A'),
            "Favorite Model",
            "🤖"
        ), unsafe_allow_html=True)

    with col3:
        member_since = utils.format_timestamp(user.get('signup_date'), "short")
        st.markdown(ui_components.stats_card(
            member_since,
            "Member Since",
            "📅"
        ), unsafe_allow_html=True)

    st.markdown("---")

    # Recent activity
    st.markdown("### 📊 Recent Activity")

    recent_codes = database.get_user_codes(user['_id'], limit=5)

    if recent_codes:
        for code in recent_codes:
            with st.expander(f"{code.get('language', 'Code')} - {utils.truncate_text(code.get('prompt', 'No prompt'), 60)}"):
                st.code(code.get('code_output', ''), language=code.get('language', '').lower())
                st.caption(f"Generated with {code.get('model_name', 'Unknown')} - {utils.format_timestamp(code.get('created_at'))}")
    else:
        st.markdown(ui_components.empty_state(
            "📝",
            "No code generated yet",
            "Start by generating your first code!",
            "Generate Code"
        ), unsafe_allow_html=True)

    # Quick actions
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("✨ Generate Code", use_container_width=True, type="primary"):
            st.session_state['current_page'] = 'generate'
            st.rerun()

    with col2:
        if st.button("🕒 View History", use_container_width=True):
            st.session_state['current_page'] = 'history'
            st.rerun()

# ============================================================
# PAGE 2: GENERATE CODE
# ============================================================

def show_generate_page():
    """
    Code generation page with multiple tabs
    """
    st.markdown(ui_components.page_header(
        "Generate Code",
        "AI-powered code generation with multiple models",
        "✨"
    ), unsafe_allow_html=True)

    # Tabs for different tasks
    tab1, tab2, tab3 = st.tabs(["🎯 Generate", "📖 Explain", "⚡ Improve"])

    with tab1:
        show_generate_tab()

    with tab2:
        show_explain_tab()

    with tab3:
        show_improve_tab()

def show_generate_tab():
    """Generate code tab"""
    st.markdown("### Select AI Model")

    # Model selection
    col1, col2, col3 = st.columns(3)

    models = {
        "gemma-2b": {"name": "Gemma-2B", "desc": "General-purpose", "icon": "🔵"},
        "phi-2": {"name": "Phi-2", "desc": "Fast & efficient", "icon": "🟢"},
        "codebert": {"name": "CodeBERT", "desc": "Code analysis", "icon": "🟣"}
    }

    if 'selected_model' not in st.session_state:
        st.session_state['selected_model'] = 'gemma-2b'

    with col1:
        if st.button(f"{models['gemma-2b']['icon']} {models['gemma-2b']['name']}\n{models['gemma-2b']['desc']}",
                    use_container_width=True,
                    type="primary" if st.session_state['selected_model'] == 'gemma-2b' else "secondary"):
            st.session_state['selected_model'] = 'gemma-2b'

    with col2:
        if st.button(f"{models['phi-2']['icon']} {models['phi-2']['name']}\n{models['phi-2']['desc']}",
                    use_container_width=True,
                    type="primary" if st.session_state['selected_model'] == 'phi-2' else "secondary"):
            st.session_state['selected_model'] = 'phi-2'

    with col3:
        if st.button(f"{models['codebert']['icon']} {models['codebert']['name']}\n{models['codebert']['desc']}",
                    use_container_width=True,
                    type="primary" if st.session_state['selected_model'] == 'codebert' else "secondary"):
            st.session_state['selected_model'] = 'codebert'

    st.markdown("---")

    # Input section
    language = st.selectbox("Programming Language", ["Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "TypeScript"])
    prompt = st.text_area("Describe what you want to build", height=100, placeholder="E.g., Create a function that sorts a list of numbers")

    # Advanced options
    with st.expander("⚙️ Advanced Options"):
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7, help="Higher = more creative, Lower = more focused")
        max_tokens = st.number_input("Max Tokens", 100, 1000, 500)

    # Generate button
    if st.button("✨ Generate Code", type="primary", use_container_width=True):
        if not prompt:
            st.error("Please enter a description")
        else:
            with st.spinner(f"Generating {language} code with {models[st.session_state['selected_model']]['name']}..."):
                result = ai_models.generate_code(
                    st.session_state['selected_model'],
                    language,
                    prompt,
                    temperature=temperature,
                    max_tokens=max_tokens
                )

                if result['success']:
                    st.success("Code generated successfully!")

                    # Display code
                    st.code(result['code'], language=language.lower())

                    # Metadata
                    col_meta1, col_meta2, col_meta3 = st.columns(3)
                    with col_meta1:
                        st.caption(f"Model: {models[st.session_state['selected_model']]['name']}")
                    with col_meta2:
                        st.caption(f"Tokens: {result['tokens']}")
                    with col_meta3:
                        st.caption(f"Time: {result['time']:.2f}s")

                    # Action buttons
                    col_act1, col_act2, col_act3 = st.columns(3)

                    with col_act1:
                        if st.button("💾 Save to History"):
                            user = st.session_state['user']
                            saved = database.save_code(
                                user['_id'],
                                st.session_state['selected_model'],
                                "generate",
                                language,
                                prompt,
                                result['code'],
                                metadata={
                                    'tokens_used': result['tokens'],
                                    'response_time': result['time'],
                                    'success': True
                                }
                            )
                            if saved:
                                st.success("Saved to history!")
                            else:
                                st.error("Failed to save")

                    with col_act2:
                        st.download_button("📥 Download", result['code'], file_name=f"code.{language.lower()}")

                    with col_act3:
                        if st.button("🔄 Regenerate"):
                            st.rerun()

                else:
                    st.error(f"Generation failed: {result['error']}")

def show_explain_tab():
    """Explain code tab"""
    st.markdown("### Explain Code")

    code_input = st.text_area("Paste code to explain", height=200)
    language = st.selectbox("Language", ["Python", "JavaScript", "Java", "C++", "TypeScript"], key="explain_lang")

    if st.button("📖 Explain Code", type="primary"):
        if not code_input:
            st.error("Please enter code to explain")
        else:
            with st.spinner("Analyzing code..."):
                result = ai_models.explain_code(code_input, language)

                if result['success']:
                    st.success("Explanation generated!")
                    st.markdown(result['explanation'])
                else:
                    st.error(f"Failed: {result['error']}")

def show_improve_tab():
    """Improve code tab"""
    st.markdown("### Improve Code")

    code_input = st.text_area("Paste code to improve", height=200)
    language = st.selectbox("Language", ["Python", "JavaScript", "Java", "C++", "TypeScript"], key="improve_lang")
    focus = st.selectbox("Improvement Focus", ["General", "Performance", "Readability", "Security", "Best Practices"])

    if st.button("⚡ Improve Code", type="primary"):
        if not code_input:
            st.error("Please enter code to improve")
        else:
            with st.spinner("Improving code..."):
                result = ai_models.improve_code(code_input, language, focus)

                if result['success']:
                    st.success("Code improved!")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("**Original:**")
                        st.code(code_input, language=language.lower())

                    with col2:
                        st.markdown("**Improved:**")
                        st.code(result['improved_code'], language=language.lower())

                    st.markdown("**Improvements:**")
                    st.info(result['notes'])
                else:
                    st.error(f"Failed: {result['error']}")

# ============================================================
# PAGE 3: HISTORY
# ============================================================

def show_history_page():
    """
    Code history page with search and filter
    """
    user = st.session_state['user']

    st.markdown(ui_components.page_header(
        "Code History",
        "View and manage your generated code",
        "🕒"
    ), unsafe_allow_html=True)

    # Search and filter
    col1, col2 = st.columns([3, 1])

    with col1:
        search_query = st.text_input("🔍 Search", placeholder="Search in prompts or code...")

    with col2:
        if st.button("Export History", use_container_width=True):
            codes = database.get_user_codes(user['_id'], limit=1000)
            if codes:
                csv_data = utils.export_to_csv(
                    codes,
                    ['prompt', 'language', 'model_name', 'created_at']
                )
                st.download_button("Download CSV", csv_data, "code_history.csv", "text/csv")

    # Filters
    col_f1, col_f2, col_f3 = st.columns(3)

    with col_f1:
        model_filter = st.multiselect("Model", ["gemma-2b", "phi-2", "codebert"])

    with col_f2:
        lang_filter = st.multiselect("Language", ["Python", "JavaScript", "Java", "C++"])

    with col_f3:
        sort_by = st.selectbox("Sort By", ["Newest First", "Oldest First"])

    # Get codes
    if search_query or model_filter or lang_filter:
        codes = database.search_codes(
            user['_id'],
            search_query=search_query,
            filters={'models': model_filter, 'languages': lang_filter}
        )
    else:
        codes = database.get_user_codes(user['_id'], limit=50)

    st.markdown("---")

    # Display codes
    if codes:
        st.markdown(f"Found {len(codes)} code(s)")

        for code in codes:
            with st.container():
                col_code1, col_code2 = st.columns([4, 1])

                with col_code1:
                    st.markdown(f"**{code.get('language', 'Code')}** - {utils.truncate_text(code.get('prompt', ''), 80)}")
                    st.caption(f"{code.get('model_name', 'Unknown')} • {utils.format_timestamp(code.get('created_at'))}")

                with col_code2:
                    if st.button("👁️ View", key=f"view_{code['_id']}"):
                        st.session_state[f"show_{code['_id']}"] = not st.session_state.get(f"show_{code['_id']}", False)

                if st.session_state.get(f"show_{code['_id']}", False):
                    st.code(code.get('code_output', ''), language=code.get('language', '').lower())

                    col_act1, col_act2, col_act3 = st.columns(3)

                    with col_act1:
                        st.download_button("📥 Download", code.get('code_output', ''),
                                         file_name=f"code_{code['_id']}.txt", key=f"dl_{code['_id']}")

                    with col_act3:
                        if st.button("🗑️ Delete", key=f"del_{code['_id']}"):
                            if database.delete_code(code['_id'], user['_id']):
                                st.success("Deleted!")
                                st.rerun()

                st.markdown("---")
    else:
        st.markdown(ui_components.empty_state(
            "📭",
            "No code history",
            "Generate some code to see it here!",
            "Generate Code"
        ), unsafe_allow_html=True)

# ============================================================
# PAGE 4: PROFILE
# ============================================================

def show_profile_page():
    """
    User profile management page
    """
    user = st.session_state['user']

    st.markdown(ui_components.page_header(
        "Profile",
        "Manage your account settings",
        "👤"
    ), unsafe_allow_html=True)

    # Profile information
    st.markdown("### 📝 Profile Information")

    name = st.text_input("Full Name", value=user.get('name', ''))
    email = st.text_input("Email", value=user.get('email', ''), disabled=user.get('auth_provider') != 'email')
    bio = st.text_area("Bio", value=user.get('bio', ''), max_chars=500, placeholder="Tell us about yourself...")

    if st.button("💾 Save Changes", type="primary"):
        updated = database.update_user(user['_id'], {
            'name': name,
            'bio': bio
        })

        if updated:
            st.session_state['user'] = updated
            st.success("Profile updated!")
        else:
            st.error("Failed to update profile")

    st.markdown("---")

    # Account statistics
    st.markdown("### 📊 Account Statistics")

    stats = database.get_user_code_stats(user['_id'])

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Member Since", utils.format_timestamp(user.get('signup_date'), "short"))

    with col2:
        st.metric("Total Codes", stats.get('total_codes', 0))

    with col3:
        st.metric("Favorite Model", stats.get('favorite_model', 'N/A'))

    with col4:
        st.metric("Last Login", utils.format_timestamp(user.get('last_login')))

    st.markdown("---")

    # Settings
    st.markdown("### ⚙️ Settings")

    email_notifications = st.checkbox("Email notifications (weekly reports)",
                                     value=user.get('email_notifications', True))

    if st.button("Save Settings"):
        database.update_user(user['_id'], {'email_notifications': email_notifications})
        st.success("Settings saved!")

    st.markdown("---")

    # Danger zone
    with st.expander("🚨 Danger Zone"):
        st.warning("These actions cannot be undone!")

        if user.get('auth_provider') == 'email':
            if st.button("🔐 Change Password"):
                st.info("Password change would redirect to change password flow")

        if st.button("🗑️ Delete Account"):
            st.error("Account deletion would require confirmation")

# ============================================================
# PAGE 5: REVIEWS
# ============================================================

def show_reviews_page():
    """
    Reviews and feedback page
    """
    st.markdown(ui_components.page_header(
        "Reviews & Feedback",
        "Share your experience and see community reviews",
        "💬"
    ), unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["✍️ Submit Review", "👥 Community Reviews"])

    with tab1:
        show_submit_review_tab()

    with tab2:
        show_community_reviews_tab()

def show_submit_review_tab():
    """Submit review tab"""
    st.markdown("### Share Your Feedback")

    # Star rating
    rating = st.slider("Rating", 1, 5, 5, help="1 = Poor, 5 = Excellent")
    st.markdown(ui_components.star_rating(rating, "large"), unsafe_allow_html=True)

    title = st.text_input("Title", max_chars=100, placeholder="Summary of your feedback")
    comment = st.text_area("Comment", max_chars=500, placeholder="Tell us what you think...")
    category = st.selectbox("Category", ["General Feedback", "Feature Request", "Bug Report"])

    if st.button("✉️ Submit Feedback", type="primary"):
        if not title or not comment:
            st.error("Please fill in all fields")
        else:
            user = st.session_state['user']
            review = database.submit_review(user['_id'], rating, title, comment, category)

            if review:
                st.success("Thank you for your feedback! 🎉")
                st.balloons()
            else:
                st.error("Failed to submit feedback")

def show_community_reviews_tab():
    """Community reviews tab"""
    st.markdown("### What Others Are Saying")

    approved_reviews = database.get_reviews(status="approved", limit=20)

    if approved_reviews:
        for review in approved_reviews:
            # Get user info
            review_user = database.get_user_by_id(review['user_id'])
            user_name = review_user.get('name', 'Anonymous') if review_user else 'Anonymous'

            with st.container():
                col1, col2 = st.columns([4, 1])

                with col1:
                    st.markdown(ui_components.star_rating(review.get('rating', 0)), unsafe_allow_html=True)
                    st.markdown(f"**{review.get('title', '')}**")
                    st.write(review.get('comment', ''))
                    st.caption(f"By {user_name} • {utils.format_timestamp(review.get('created_at'))}")

                with col2:
                    helpful_count = review.get('helpful_count', 0)
                    if st.button(f"👍 Helpful ({helpful_count})", key=f"helpful_{review['_id']}"):
                        user = st.session_state['user']
                        if database.vote_helpful(review['_id'], user['_id']):
                            st.success("Thanks!")
                            st.rerun()

                st.markdown("---")
    else:
        st.info("No reviews yet. Be the first to share your feedback!")

# ============================================================
# PAGE 6: SUPPORT
# ============================================================

def show_support_page():
    """
    Support and help page
    """
    st.markdown(ui_components.page_header(
        "Support & Help",
        "Get help and find answers to common questions",
        "❓"
    ), unsafe_allow_html=True)

    # FAQ
    st.markdown("### 📚 Frequently Asked Questions")

    faqs = [
        ("How do I generate code?", "Navigate to the Generate Code page, select a model, choose your language, and describe what you want to build."),
        ("Which model should I use?", "Gemma-2B is great for general purposes, Phi-2 is fast for quick tasks, and CodeBERT excels at code analysis."),
        ("How do I save my code?", "After generating code, click the 'Save to History' button. You can view all saved code in the History page."),
        ("What languages are supported?", "We support Python, JavaScript, Java, C++, C#, Go, Rust, and TypeScript."),
        ("How do I export my history?", "Go to the History page and click 'Export History' to download your code as CSV.")
    ]

    for question, answer in faqs:
        with st.expander(question):
            st.write(answer)

    st.markdown("---")

    # Contact support
    st.markdown("### 💬 Contact Support")

    st.write("Need more help? Reach out to our support team:")

    col1, col2 = st.columns(2)

    with col1:
        st.info("📧 **Email:** support@codegalaxy.com")

    with col2:
        if st.button("Submit a Ticket", use_container_width=True):
            st.session_state['current_page'] = 'reviews'
            st.rerun()

    st.markdown("---")

    # Documentation links
    st.markdown("### 📖 Documentation")

    st.markdown("""
    - [Getting Started Guide](#)
    - [Model Comparison](#)
    - [API Rate Limits](#)
    - [Privacy Policy](#)
    """)
