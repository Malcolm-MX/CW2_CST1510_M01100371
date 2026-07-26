import streamlit as st
from app_model.it_tickets import get_all_it_tickets
from app_model.db import connect_database
import pandas as pd

st.set_page_config(page_title="IT Tickets",layout="wide")

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
data = get_all_it_tickets(conn)

st.title("Welcome to the IT Tickets Dashboard!")

#Sidebar filter which lets the user pick which ticket status to focus on
with st.sidebar:
    st.header("Navigation")
    status_ = st.selectbox("Status",data['status'].unique())

#Convert created_at from plain text into a real datetime type so
#operations for date module work correctly
data['created_at'] = pd.to_datetime(data['created_at'])

#Narrowing the data down to just the selected status
filtered_data = data[data['status'] == status_]

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    st.subheader(f"IT Tickets Status: {status_}")
    st.bar_chart(filtered_data['priority'].value_counts())


with col2:
    st.subheader("Tickets Created Over Time")
    #Strip time-of-day off each timestamp, then count how many tickets
    #were created on each date
    tickets_created = (filtered_data['created_at'].dt.date.value_counts())
    st.line_chart(tickets_created)

with col3:
    st.subheader("Tickets By Support Team")
    st.bar_chart(filtered_data['assigned_to'].value_counts())

with col4:
    st.subheader("All Tickets By Priority")
    #Uses the full unfiltered dataset, so the user can compare this
    #status's priorities against the overall picture
    st.bar_chart(data['priority'].value_counts())



st.subheader("Filtered Data")
st.dataframe(filtered_data)
st.divider()
st.subheader("All Tickets By Their Status")
st.bar_chart(data['status'].value_counts())
st.subheader("Raw Dataset")
st.dataframe(data)

with st.sidebar:
    st.divider()
    if st.button ("Log Out"):
        st.session_state["logged_in"] = False
        st.switch_page("Home.py")