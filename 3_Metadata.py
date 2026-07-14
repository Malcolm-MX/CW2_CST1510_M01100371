import streamlit as st
from app_model.metadatas import get_all_datasets_metadata
from app_model.db import connect_database
import pandas as pd

st.set_page_config(page_title="Metadatas",layout="wide")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.warning("Please log in to access the dashboard.")
    if st.button("Go to Login Page"):
        st.session_state['logged_in'] = False
        st.switch_page("Home.py")
    st.stop()
else:
    st.success("You are logged in!")

conn = connect_database()
data = get_all_datasets_metadata(conn)

st.title("Welcome to the Metadata Dashboard!")

with st.sidebar:
    st.header("Navigation")
    name_ = st.selectbox("Name Of Dataset",data['name'].unique())

data['upload_date'] = pd.to_datetime(data['upload_date'])

filtered_data = data[data['name'] == name_]

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    st.subheader("Datasets by Uploader")
    st.bar_chart(data['uploaded_by'].value_counts())
    
with col2:
    st.subheader(f"Selected Dataset: {name_}")
    st.dataframe(filtered_data)

with col3:
    st.subheader("Rows Per Dataset")
    st.bar_chart(data.set_index('name')['rows'])

with col4:
    st.subheader("Columns per Dataset")
    st.bar_chart(data.set_index('name')['columns'])

st.divider()
st.subheader("Raw Dataset")
st.dataframe(data)

with st.sidebar:
    st.divider()
    if st.button ("Log Out"):
        st.session_state["logged_in"] = False
        st.switch_page("Home.py")