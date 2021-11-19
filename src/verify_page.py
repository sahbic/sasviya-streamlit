import streamlit as st
import pandas as pd

def app():
    st.title('Verify data')
    if 'session' in st.session_state:
        with st.form("my_form1"):
            user_input = st.text_input("Library name")
            submitted = st.form_submit_button("List tables")
            if submitted:
                s = st.session_state.session
                df = s.tableInfo(caslib=user_input).TableInfo
                st.table(df[["Name","Rows","Columns"]])

        with st.form("my_form2"):
            user_input = st.text_input("Table name")
            submitted = st.form_submit_button("Profile Data")
            if submitted:
                s = st.session_state.session
                df = s.simple.summary(table={"name":user_input}).Summary.iloc[:,:6]
                st.dataframe(df)