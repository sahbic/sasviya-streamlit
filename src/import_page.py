import streamlit as st
import pandas as pd

def app():
    st.title('Import data')
    if 'session' in st.session_state:
        uploaded_file = st.file_uploader("Choose a CSV file", accept_multiple_files=False)
        if uploaded_file is not None:
            name = uploaded_file.name.split(".")[0]
            st.session_state.session.dropTable(name=name, caslib="casuser", quiet=True)
            st.session_state.session.read_csv(uploaded_file, casout={"name":name,"caslib":"casuser","promote":True})
            st.write('Data sample')
            df = st.session_state.session.CASTable(name).to_frame().head()
            st.dataframe(df)