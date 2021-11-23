import streamlit as st
import pandas as pd
import altair as alt

def get_table(tbl, s):
  tbl = s.CASTable(tbl)
  return(tbl.to_frame())

def feature_engineering(s, tbl_name, target, a, b, c, d, e, f, g):
  s.loadActionSet("dataSciencePilot")
  features = s.dataSciencePilot.featureMachine(
    table                 = {"name":tbl_name, "caslib":"casuser"},
    target                = target,
    explorationPolicy     = {},
    screenPolicy          = {},
    copyVars = [target],
    transformationPolicy  = {"missing":a, "cardinality":b,
                             "entropy":c, "iqv":d,
                             "skewness":e, "kurtosis":f, "Outlier":g},
    transformationOut     = {"name":"TRANSFORMATION_OUT", "replace":True},
    featureOut            = {"name":"FEATURE_OUT", "replace":True},
    casOut                = {"name":tbl_name + "_TRANSFORMED", "replace":True},
    saveState             = {"name":"ASTORE_OUT", "replace":True}
  )
  return(get_table("FEATURE_OUT", s))

def app():
    st.title('Feature Engineering')
    if 'session' in st.session_state:
        with st.form("my_form1"):
            user_input_table = st.text_input("Table name")
            user_input_target = st.text_input("Target variable")
            a = st.checkbox('Analyze Missing')
            b = st.checkbox('Analyze Cardinality')
            c = st.checkbox('Analyze Entropy')
            d = st.checkbox('Analyze IQV')
            e = st.checkbox('Analyze Skewness')
            f = st.checkbox('Analyze Kurtosis')
            g = st.checkbox('Analyze Outlier')
            submitted = st.form_submit_button("Generate Features")
            if submitted:
                s = st.session_state.session
                out = feature_engineering(s, user_input_table, user_input_target, a, b, c, d, e, f, g)
                st.session_state.tbl_name = user_input_table
                st.dataframe(out)