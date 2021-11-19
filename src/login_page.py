import streamlit as st
import pandas as pd
import swat

def flatten_data(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def app():
    st.title('Login')

    with st.form("my_form"):
        st.write('Enter your credentials')
        user_input = st.text_input("Enter username")
        password = st.text_input("Enter your password", type="password")
        submitted = st.form_submit_button("Submit")
        if submitted:
            s = swat.CAS("http://dach-viya4-k8s/cas-shared-default-http", username=user_input, password=password)
            st.session_state.session = s
            server_status = flatten_data(s.serverStatus().About)
            df = pd.DataFrame.from_records([server_status],index=["values"]).astype(str)
            st.table(df.T)
