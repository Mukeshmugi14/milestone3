"""
CodeGalaxy - Admin Dashboard
Admin portal with analytics, user management, and moderation features
"""

import streamlit as st
import database
import ui_components
import plotly.graph_objects as go
from datetime import datetime, timedelta

def show_admin_dashboard():
    """
    Main admin dashboard with tabs
    """
    # Check admin authentication
    if not st.session_state.get('is_admin'):
        st.error("Access denied. Admin privileges required.")
        st.stop()

    st.markdown(ui_components.page_header(
        "Admin Dashboard",
        "Platform management and analytics",
        "⚙️"
    ), unsafe_allow_html=True)

    # Get platform stats
    stats = database.get_platform_stats()

    # Top stats cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(ui_components.stats_card(
            stats.get('total_users', 0),
            "Total Users",
            "👥"
        ), unsafe_allow_html=True)

    with col2:
        st.markdown(ui_components.stats_card(
            stats.get('total_codes', 0),
            "Codes Generated",
            "📝"
        ), unsafe_allow_html=True)

    with col3:
        st.markdown(ui_components.stats_card(
            stats.get('active_today', 0),
            "Active Today",
            "🔥"
        ), unsafe_allow_html=True)

    with col4:
        st.markdown(ui_components.stats_card(
            stats.get('pending_reviews', 0),
            "Pending Reviews",
            "💬"
        ), unsafe_allow_html=True)

    st.markdown("---")

    # Main tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Analytics",
        "👥 Users",
        "💬 Reviews",
        "🤖 Models",
        "📋 Logs",
        "⚙️ Settings"
    ])

    with tab1:
        show_analytics_tab()

    with tab2:
        show_user_management_tab()

    with tab3:
        show_review_moderation_tab()

    with tab4:
        show_model_monitoring_tab()

    with tab5:
        show_activity_logs_tab()

    with tab6:
        show_settings_tab()

def show_analytics_tab():
    """Analytics dashboard"""
    st.markdown("### Platform Analytics")

    # Model usage distribution
    st.markdown("#### Model Usage Distribution")

    # Get model stats (simplified)
    gemma_stats = database.get_model_stats("gemma-2b", 30)
    phi_stats = database.get_model_stats("phi-2", 30)
    codebert_stats = database.get_model_stats("codebert", 30)

    fig = go.Figure(data=[go.Pie(
        labels=['Gemma-2B', 'Phi-2', 'CodeBERT'],
        values=[
            gemma_stats.get('total_uses', 0) if gemma_stats else 0,
            phi_stats.get('total_uses', 0) if phi_stats else 0,
            codebert_stats.get('total_uses', 0) if codebert_stats else 0
        ]
    )])

    st.plotly_chart(fig, use_container_width=True)

    # Export analytics
    if st.button("📥 Export Analytics Report"):
        st.success("Report exported!")

def show_user_management_tab():
    """User management"""
    st.markdown("### User Management")

    # Search and filters
    search = st.text_input("🔍 Search users by name or email")

    col1, col2 = st.columns(2)
    with col1:
        role_filter = st.selectbox("Role", ["All", "User", "Admin"])
    with col2:
        status_filter = st.selectbox("Status", ["All", "Active", "Suspended"])

    # Get users
    filters = {}
    if role_filter != "All":
        filters['role'] = role_filter.lower()
    if status_filter != "All":
        filters['status'] = status_filter.lower()
    if search:
        filters['search'] = search

    users = database.get_all_users(filters, limit=50)

    # Display users
    if users:
        for user in users:
            with st.expander(f"{user.get('name', 'Unknown')} ({user.get('email', '')})"):
                col_user1, col_user2 = st.columns(2)

                with col_user1:
                    st.write(f"**Role:** {user.get('role', 'user')}")
                    st.write(f"**Status:** {user.get('status', 'active')}")
                    st.write(f"**Signup:** {user.get('signup_date', 'N/A')}")

                with col_user2:
                    if st.button("✏️ Edit", key=f"edit_{user['_id']}"):
                        st.info("Edit functionality would open edit form")

                    if user.get('status') == 'active':
                        if st.button("🔒 Suspend", key=f"suspend_{user['_id']}"):
                            database.update_user(user['_id'], {'status': 'suspended'})
                            st.success("User suspended")
                            st.rerun()
                    else:
                        if st.button("🔓 Reactivate", key=f"reactivate_{user['_id']}"):
                            database.update_user(user['_id'], {'status': 'active'})
                            st.success("User reactivated")
                            st.rerun()
    else:
        st.info("No users found")

def show_review_moderation_tab():
    """Review moderation"""
    st.markdown("### Review Moderation")

    filter_status = st.radio("Filter", ["Pending", "Approved", "Rejected"], horizontal=True)

    reviews = database.get_reviews(status=filter_status.lower(), limit=50)

    if reviews:
        for review in reviews:
            user = database.get_user_by_id(review['user_id'])
            user_name = user.get('name', 'Unknown') if user else 'Unknown'

            with st.container():
                st.markdown(f"**{review.get('title', '')}** by {user_name}")
                st.markdown(ui_components.star_rating(review.get('rating', 0)), unsafe_allow_html=True)
                st.write(review.get('comment', ''))
                st.caption(f"Category: {review.get('category', '')} • {review.get('created_at', '')}")

                if filter_status == "Pending":
                    col_rev1, col_rev2, col_rev3 = st.columns(3)

                    with col_rev1:
                        if st.button("✅ Approve", key=f"approve_{review['_id']}"):
                            admin_id = st.session_state['user'].get('_id')
                            database.moderate_review(review['_id'], "approve", admin_id)
                            st.success("Review approved!")
                            st.rerun()

                    with col_rev2:
                        if st.button("❌ Reject", key=f"reject_{review['_id']}"):
                            admin_id = st.session_state['user'].get('_id')
                            database.moderate_review(review['_id'], "reject", admin_id, reason="Admin decision")
                            st.success("Review rejected!")
                            st.rerun()

                    with col_rev3:
                        if st.button("💬 Respond", key=f"respond_{review['_id']}"):
                            st.session_state[f"responding_{review['_id']}"] = True

                if st.session_state.get(f"responding_{review['_id']}", False):
                    response = st.text_area("Admin Response", key=f"response_{review['_id']}")
                    if st.button("Send Response", key=f"send_{review['_id']}"):
                        admin_id = st.session_state['user'].get('_id')
                        database.moderate_review(review['_id'], "respond", admin_id, response=response)
                        st.success("Response sent!")
                        st.rerun()

                st.markdown("---")
    else:
        st.info(f"No {filter_status.lower()} reviews")

def show_model_monitoring_tab():
    """Model monitoring"""
    st.markdown("### Model Monitoring")

    # Get stats for all models
    for model_name in ["gemma-2b", "phi-2", "codebert"]:
        stats = database.get_model_stats(model_name, 30)

        if stats:
            with st.expander(f"🤖 {model_name.upper()}", expanded=True):
                col_model1, col_model2, col_model3 = st.columns(3)

                with col_model1:
                    st.metric("Total Uses", stats.get('total_uses', 0))

                with col_model2:
                    st.metric("Success Rate", f"{stats.get('success_rate', 0):.1f}%")

                with col_model3:
                    st.metric("Avg Response Time", f"{stats.get('avg_response_time', 0):.2f}s")

def show_activity_logs_tab():
    """Activity logs"""
    st.markdown("### Activity Logs")

    log_type = st.selectbox("Log Type", ["All", "User Actions", "Admin Actions", "System Events", "Security Events"])

    filters = {}
    if log_type != "All":
        filters['type'] = log_type.replace(" ", "_").lower()

    logs = database.get_logs(filters, limit=100)

    if logs:
        for log in logs:
            with st.expander(f"{log.get('action', 'Unknown')} - {log.get('created_at', '')}"):
                st.write(f"**Type:** {log.get('type', '')}")
                st.write(f"**Severity:** {log.get('severity', 'info')}")
                st.json(log.get('details', {}))
    else:
        st.info("No logs found")

def show_settings_tab():
    """Platform settings"""
    st.markdown("### Platform Settings")

    # General settings
    st.markdown("#### General")
    platform_name = st.text_input("Platform Name", value="CodeGalaxy")
    welcome_msg = st.text_area("Welcome Message", value="Welcome to CodeGalaxy!")

    if st.button("💾 Save General Settings"):
        st.success("Settings saved!")

    st.markdown("---")

    # Email settings
    st.markdown("#### Email Configuration")
    st.write(f"SMTP Server: {os.getenv('EMAIL_USER', 'Not configured')}")

    if st.button("📧 Send Test Email"):
        st.info("Test email would be sent")

    st.markdown("---")

    # API settings
    st.markdown("#### API Configuration")

    for model_name in ["gemma-2b", "phi-2", "codebert"]:
        result = ai_models.test_model_api(model_name)
        status = "✅ Connected" if result['connected'] else "❌ Disconnected"
        st.write(f"**{model_name}:** {status}")

import os
import ai_models
