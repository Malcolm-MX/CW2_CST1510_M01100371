import streamlit as st
from app_model.db import connect_database
from app_model.users import get_all_users
import pandas as pd

if not st.session_state.get("logged_in") or st.session_state.get("role") != 'admin':
    st.error("Access denied. Admins only.")
    st.stop()

st.title("Admin Dashboard")

st.header("Welcome, Admin.")

st.subheader("View your registered users here")

conn = connect_database()
users = get_all_users(conn)
usersDataFrame = pd.DataFrame(users, columns =["id","username","password_hash","failed_attempts","locked"])
usersAdminDisplay = usersDataFrame.drop(columns=["password_hash"])
st.dataframe(usersAdminDisplay)

with st.sidebar:
    st.divider()
    if st.button ("Log Out"):
        st.session_state["logged_in"] = False
        st.switch_page("Home.py")