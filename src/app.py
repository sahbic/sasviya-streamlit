import streamlit as st
import login_page
import import_page
import verify_page
import explore_page


PAGES = {
    "Login": login_page,
    "Import data": import_page,
    "Verify data": verify_page,
    "Explore data": explore_page
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()