import streamlit as st
from app_model.cyber_incidents import get_all_cyber_incidents
from app_model.db import connect_database
import pandas as pd

st.set_page_config(page_title="Cyber Incidents",page_icon="🏠",layout="wide")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

#If the user isn't logged in, they don't have access to this page, this is in pretty much all the pages
if not st.session_state['logged_in']:
    st.warning("Please log in to access the dashboard.")
    if st.button("Go to Login Page"):
        st.session_state['logged_in'] = False
        st.switch_page("Home.py")
    st.stop()
else:
    st.success("You are logged in!")

conn = connect_database()
data = get_all_cyber_incidents(conn)

st.title("Welcome to the Cyber Incidents Dashboard!")

#Sidebar filter which lets the user pick which severity level to focus on
with st.sidebar:
    st.header("Navigation")
    severity_ = st.selectbox("Severity Level",data['severity'].unique())

#Convert timestamp from plain text into a real datetime type so charts
#order points better
data['timestamp'] = pd.to_datetime(data['timestamp'])

#Narrow the data down to just the selected severity level
filtered_data = data[data['severity'] == severity_]

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Cyber Incidents with Severity: {severity_}")
    st.bar_chart(filtered_data['category'].value_counts())

with col2:
    st.subheader("Category Trend Over Time")
    st.line_chart(filtered_data, x='timestamp',y='category')

st.subheader("Filtered Data")
st.dataframe(filtered_data)
st.subheader("Filtered Data As A Bar Chart")
st.bar_chart(data['category'].value_counts())
st.divider()
st.subheader("Raw Dataset")
st.dataframe(data)

with st.sidebar:
    st.divider()
    if st.button ("Log Out"):
        st.session_state["logged_in"] = False
        st.switch_page("Home.py")