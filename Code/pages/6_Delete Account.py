import streamlit as st
from app_model.db import connect_database
from app_model.users import get_user, delete_user
from hashing import validateHash

#If the user isn't logged in, they don't have access to this page, this is in pretty much all the pages
if not st.session_state.get("logged_in"):
    st.warning("Log in first, in order to delete your account")
    if st.button("Go to Login Page"):
        st.switch_page("Home.py")
    st.stop()

#Setting the page title and layout to wide
st.set_page_config(page_title="Delete Account", layout="wide")
st.title("Delete Your Account")
st.subheader("Sad to see you leave, remember, this action is permanent and cannot be undone.")

#Establishing a connection and passing it to the variable conn
conn = connect_database()

#Asking the user to enter their username and password again before deleting their,
#protects against an unattended logged-in session being used to delete the account without knowing the password
#Therefore it is an extremely strong security feature

confirmUsername = st.text_input("Confirm Username")
confirmPassword = st.text_input("Confirm Password", type = "password")

if st.button("Delete Account"):
    #First look up the account by the username that would have been entered
    user_row = get_user(conn, confirmUsername)
    if user_row:
        id, userName, userHash = user_row[:3]
        if confirmUsername == userName and validateHash(confirmPassword, userHash):
            #So the account will only be deleted if both the username and password entered are similar to the stored ones of the same account
            delete_user(conn, confirmUsername)
            st.session_state["logged_in"] = False
            st.session_state["role"] = None
            st.success("Account deleted. You have been logged out.")
            st.switch_page("Home.py")
        else:
            st.error("Incorrect password or username. Account not deleted. Try again.")