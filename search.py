"""
CodeGalaxy - Search Functionality
Global search across codes, reviews, and documentation
"""

import database
import utils

def perform_search(query, collections=['codes', 'reviews'], user_id=None):
    """
    Performs fuzzy search across specified collections
    Args:
        query: Search query string
        collections: List of collections to search
        user_id: User ID for scoped search (optional)
    Returns: Dict with results from each collection
    """
    results = {
        "codes": [],
        "reviews": [],
        "docs": []
    }

    if not query:
        return results

    # Search in codes
    if 'codes' in collections and user_id:
        codes = database.search_codes(user_id, search_query=query)
        results['codes'] = codes[:10]  # Limit to top 10

    # Search in reviews
    if 'reviews' in collections:
        all_reviews = database.get_reviews(status="approved", limit=100)
        matching_reviews = []

        for review in all_reviews:
            if utils.fuzzy_search(query, review.get('title', '')) or \
               utils.fuzzy_search(query, review.get('comment', '')):
                matching_reviews.append(review)

        results['reviews'] = matching_reviews[:10]

    # Search in docs (placeholder)
    if 'docs' in collections:
        # In production, this would search through documentation
        results['docs'] = []

    return results

def show_search_results(query):
    """
    Displays search results in tabbed interface
    """
    import streamlit as st

    st.markdown(f"### Search Results for '{query}'")

    tab1, tab2, tab3 = st.tabs(["📝 Codes", "💬 Reviews", "📚 Documentation"])

    with tab1:
        display_code_results(query)

    with tab2:
        display_review_results(query)

    with tab3:
        display_doc_results(query)

def display_code_results(query):
    """
    Displays code search results
    """
    import streamlit as st

    user = st.session_state.get('user')
    if not user:
        st.warning("Please log in to search your code history")
        return

    codes = database.search_codes(user['_id'], search_query=query)

    if codes:
        st.write(f"Found {len(codes)} code(s)")

        for code in codes:
            with st.expander(f"{code.get('language', 'Code')} - {utils.truncate_text(code.get('prompt', ''), 80)}"):
                st.code(code.get('code_output', ''), language=code.get('language', '').lower())
                st.caption(f"{code.get('model_name', 'Unknown')} • {utils.format_timestamp(code.get('created_at'))}")
    else:
        st.info("No matching codes found")

def display_review_results(query):
    """
    Displays review search results
    """
    import streamlit as st

    all_reviews = database.get_reviews(status="approved", limit=100)
    matching_reviews = []

    for review in all_reviews:
        if utils.fuzzy_search(query, review.get('title', '')) or \
           utils.fuzzy_search(query, review.get('comment', '')):
            matching_reviews.append(review)

    if matching_reviews:
        st.write(f"Found {len(matching_reviews)} review(s)")

        for review in matching_reviews:
            user = database.get_user_by_id(review['user_id'])
            user_name = user.get('name', 'Anonymous') if user else 'Anonymous'

            with st.container():
                st.markdown(f"**{review.get('title', '')}**")
                st.write(review.get('comment', ''))
                st.caption(f"By {user_name} • {utils.format_timestamp(review.get('created_at'))}")
                st.markdown("---")
    else:
        st.info("No matching reviews found")

def display_doc_results(query):
    """
    Displays documentation search results
    """
    import streamlit as st

    st.info("Documentation search coming soon!")
