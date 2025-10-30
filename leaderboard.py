"""
CodeGalaxy - Leaderboard
Rankings and leaderboard calculation logic
"""

import streamlit as st
import database
import ui_components

def show_leaderboard_page():
    """
    Displays leaderboard page with multiple ranking tabs
    """
    st.markdown(ui_components.page_header(
        "Leaderboard",
        "Top CodeGalaxy developers",
        "🏆"
    ), unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🥇 Top Coders", "⭐ Top Contributors", "🎯 Model Masters"])

    with tab1:
        show_top_coders_tab()

    with tab2:
        show_top_contributors_tab()

    with tab3:
        show_model_masters_tab()

def show_top_coders_tab():
    """
    Shows top coders by code generation count
    """
    st.markdown("### Top Code Generators")

    top_coders = database.get_top_coders(limit=100)

    if top_coders:
        # Current user's rank
        current_user_id = st.session_state['user']['_id']
        user_rank = next((i+1 for i, coder in enumerate(top_coders) if coder['user_id'] == current_user_id), None)

        if user_rank:
            st.info(f"Your Rank: #{user_rank}")

        # Display leaderboard
        for i, coder in enumerate(top_coders[:20], 1):
            with st.container():
                col1, col2, col3 = st.columns([1, 4, 2])

                with col1:
                    medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"#{i}"
                    st.markdown(f"### {medal}")

                with col2:
                    st.markdown(f"**{coder.get('name', 'Unknown')}**")
                    st.caption(coder.get('email', ''))

                with col3:
                    st.metric("Codes Generated", coder.get('code_count', 0))

                st.markdown("---")
    else:
        st.info("No data available yet. Start generating code!")

def show_top_contributors_tab():
    """
    Shows top contributors by review score
    """
    st.markdown("### Top Contributors")

    top_contributors = database.get_top_contributors(limit=100)

    if top_contributors:
        for i, contributor in enumerate(top_contributors[:20], 1):
            with st.container():
                col1, col2, col3, col4 = st.columns([1, 3, 2, 2])

                with col1:
                    medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"#{i}"
                    st.markdown(f"### {medal}")

                with col2:
                    st.markdown(f"**{contributor.get('name', 'Unknown')}**")

                with col3:
                    st.metric("Reviews", contributor.get('review_count', 0))

                with col4:
                    st.metric("Score", contributor.get('score', 0))

                st.markdown("---")
    else:
        st.info("No contributors yet. Share your feedback to appear here!")

def show_model_masters_tab():
    """
    Shows users with diverse model usage
    """
    st.markdown("### Model Masters")
    st.caption("Users who use all models evenly")

    model_masters = database.get_model_masters(limit=100)

    if model_masters:
        for i, master in enumerate(model_masters[:20], 1):
            with st.container():
                col1, col2, col3 = st.columns([1, 4, 2])

                with col1:
                    st.markdown(f"### #{i}")

                with col2:
                    st.markdown(f"**{master.get('name', 'Unknown')}**")

                with col3:
                    diversity = master.get('diversity_score', 0)
                    st.metric("Diversity", f"{diversity:.1f}%")

                st.markdown("---")
    else:
        st.info("Start using different models to appear here!")

def calculate_leaderboard_data():
    """
    Calculates and caches leaderboard data
    """
    return {
        "top_coders": database.get_top_coders(100),
        "top_contributors": database.get_top_contributors(100),
        "model_masters": database.get_model_masters(100)
    }
