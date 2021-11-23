import streamlit as st
import login_page, import_page, verify_page, explore_page, feature_page, automl_page


PAGES = {
    "Login": login_page,
    "Import data": import_page,
    "Verify data": verify_page,
    "Explore data": explore_page,
    "Feature Engineering": feature_page,
    "AutoML": automl_page
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()