import pandas as pd

import streamlit as st

email = st.text_input("enter email")
password = st.text_input("Enter password")
gender = st.selectbox("select gender",["male","female","other"])
btn = st.button("login")

if btn:
    if email =="rk0213688@gmail.com" and password =="Rk110086":
        st.success("login successful")
        st.balloons()
    else:
        st.error("login failed")


# file uploader

file = st.file_uploader("upload csv file")

if file is not None:
    df = pd.read_csv(file)
    st.dataframe(df.describe())