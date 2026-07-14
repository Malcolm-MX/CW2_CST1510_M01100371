import streamlit as st
from app_model.db import connect_database
from app_model.users import get_user, delete_user
from hashing import validateHash

if not st.session_state.get("logged_in"):
    st.warning("Log in first, in order to delete your account")
    if st.button("Go to Login Page"):
        st.switch_page("Home.py")
    st.stop()

st.set_page_config(page_title="Delete Account", layout="wide")
st.title("Delete Your Account")
st.subheader("Sad to see you leave, remember, this action is permanent and cannot be undone.")

conn = connect_database()

confirmUsername = st.text_input("Confirm Username")
confirmPassword = st.text_input("Confirm Password", type = "password")

if st.button("Delete Account"):
    user_row = get_user(conn, confirmUsername)
    if user_row:
        id, userName, userHash = user_row[:3]
        if confirmUsername == userName and validateHash(confirmPassword, userHash):
            delete_user(conn, confirmUsername)
            st.session_state["logged_in"] = False
            st.session_state["role"] = None
            st.success("Account deleted. You have been logged out.")
            st.switch_page("Home.py")
        else:
            st.error("Incorrect password or username. Account not deleted. Try again.")