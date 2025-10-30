"""
CodeGalaxy - Daily Challenges
Daily coding challenges generation and tracking
"""

import streamlit as st
import database
import ai_models
import ui_components
import utils
from datetime import datetime
import random

def show_challenges_page():
    """
    Displays daily challenges page
    """
    st.markdown(ui_components.page_header(
        "Daily Challenge",
        "Test your skills with daily coding challenges",
        "⚡"
    ), unsafe_allow_html=True)

    # Get today's challenge
    today = datetime.now()
    challenge = database.get_daily_challenge(today)

    if not challenge:
        # Generate new challenge
        with st.spinner("Generating today's challenge..."):
            challenge = generate_and_save_challenge(today)

    if challenge:
        display_challenge(challenge)
    else:
        st.error("Failed to load challenge. Please try again later.")

def generate_and_save_challenge(date):
    """
    Generates a new daily challenge using AI
    """
    # Random parameters
    difficulties = ["Easy", "Medium", "Hard"]
    languages = ["Python", "JavaScript", "Java"]
    topics = ["Arrays", "Strings", "Functions", "Algorithms", "Data Structures"]

    difficulty = random.choice(difficulties)
    language = random.choice(languages)
    topic = random.choice(topics)

    # Generate challenge using AI
    result = ai_models.generate_challenge(language, topic, difficulty)

    if result['success']:
        # Save to database
        challenge = database.create_daily_challenge(
            date=date,
            difficulty=difficulty,
            description=result['description'],
            language=language,
            hint=result['hint'],
            solution=result['solution']
        )

        return challenge

    return None

def display_challenge(challenge):
    """
    Displays the challenge with interactive elements
    """
    # Challenge header
    difficulty_color = utils.get_difficulty_color(challenge.get('difficulty', 'Medium'))
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
                padding: 30px; border-radius: 16px; margin-bottom: 20px;'>
        <h2>🗓️ Challenge of the Day - {challenge.get('date', datetime.now()).strftime('%B %d, %Y')}</h2>
        <div style='margin-top: 10px;'>
            {ui_components.badge(challenge.get('difficulty', 'Medium'), difficulty_color)}
            {ui_components.badge(challenge.get('language', 'Python'), 'info')}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Challenge description
    st.markdown("### 📋 Challenge")
    st.markdown(challenge.get('description', 'No description available'))

    st.markdown("---")

    # Actions
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💡 Get Hint", use_container_width=True):
            st.session_state['show_hint'] = True

    with col2:
        if st.button("✨ Generate Solution", use_container_width=True):
            st.session_state['show_solution'] = True

    with col3:
        if st.button("✅ Mark Complete", use_container_width=True, type="primary"):
            user = st.session_state['user']
            if database.mark_challenge_complete(user['_id'], challenge['date']):
                st.success("Challenge completed! 🎉")
                st.balloons()

    # Show hint
    if st.session_state.get('show_hint', False):
        st.markdown("### 💡 Hint")
        st.info(challenge.get('hint', 'Think about the problem step by step.'))

    # Show solution
    if st.session_state.get('show_solution', False):
        st.markdown("### ✨ Solution")
        st.code(challenge.get('solution', '# Solution not available'), language=challenge.get('language', 'python').lower())

    st.markdown("---")

    # User stats
    user = st.session_state['user']
    challenge_stats = database.get_user_challenge_stats(user['_id'])

    col_stats1, col_stats2 = st.columns(2)

    with col_stats1:
        st.metric("Challenges Completed", challenge_stats.get('completed_count', 0))

    with col_stats2:
        streak = challenge_stats.get('current_streak', 0)
        st.metric("Current Streak", f"🔥 {streak} days" if streak > 0 else "0 days")

def check_and_generate_challenge():
    """
    Checks if today's challenge exists, generates if not
    Called on app startup
    """
    today = datetime.now()
    challenge = database.get_daily_challenge(today)

    if not challenge:
        generate_and_save_challenge(today)
