import streamlit as st
import pandas as pd
import altair as alt

def app():
    st.title('Explore data')
    if 'session' in st.session_state:
        with st.form("my_form1"):
            user_input = st.text_input("Table name")
            submitted = st.form_submit_button("Explore Data")
            if submitted:
                s = st.session_state.session
                df_miss = s.simple.distinct(table={"name":user_input}).Distinct[["Column","NMiss"]]
                df_miss["PctMiss"] = df_miss["NMiss"]/df_miss.shape[0]
                c= alt.Chart(df_miss).mark_bar().encode(
                    x='Column',
                    y='PctMiss',
                    tooltip=["Column","NMiss","PctMiss"]
                )
                st.altair_chart(c, use_container_width=True)

                s.loadActionSet("cardinality")
                s.cardinality.summarize(table={"name":"HMEQ_ID"},cardinality={"caslib":"casuser", "name":"cardinality", "replace":True})
                df_card = s.CASTable("cardinality",caslib="casuser").to_frame()[["_VARNAME_","_CARDINALITY_"]]
                c2 = alt.Chart(df_card).mark_bar().encode(
                    x='_VARNAME_',
                    y='_CARDINALITY_',
                    tooltip=["_VARNAME_","_CARDINALITY_"]
                )
                st.altair_chart(c2, use_container_width=True)