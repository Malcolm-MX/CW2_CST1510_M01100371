import streamlit as st
from app_model.db import connect_database
from app_model.users import get_all_users
import pandas as pd
from app_model.users import reset_failed_attempts

#If the user isn't logged in, they don't have access to this page, this is in pretty much all the pages
#Also, any user whose role isnt 'admin' cannot have access, so there are 2 checks
if not st.session_state.get("logged_in") or st.session_state.get("role") != 'admin':
    st.error("Access denied. Admins only.")
    st.stop()

st.title("Admin Dashboard")

st.header("Welcome, Admin.")

st.subheader("View your registered users here")

#Pulling every registered user from the users table, setting up a dataframe and showing the users
conn = connect_database()
users = get_all_users(conn)
usersDataFrame = pd.DataFrame(users, columns =["id","username","password_hash","failed_attempts","locked"])
#EXTRA SECURITY FEATURE - never display password hashes, even to the admin
usersAdminDisplay = usersDataFrame.drop(columns=["password_hash"])
st.dataframe(usersAdminDisplay)

st.divider()

#Famous quote from Spiderman movie
st.subheader("Unlock a Locked Account as Admin. With great power comes great responsibility")

#Essentially extracting all the users with locked = 1, so those with locked accounts and putting their usernames into a list
cur = conn.cursor()
cur.execute("SELECT username FROM users WHERE locked = 1")
lockedUsers = [row[0] for row in cur.fetchall()] #row[0] is specifically just to display the names, not any other columns

if lockedUsers:
    selectedUser = st.selectbox("Select a locked account", lockedUsers)
    if st.button("Unlock Account"):
        reset_failed_attempts(conn, selectedUser)
        #Unlocking is essentially resetting the lock to zero as well as the failed attempts counter to 0, that's why i'm reusing this function from users.py
        st.success(f"{selectedUser} has been unlocked.")
        st.rerun()#rerunning the streamlit page to update the user list and dataframe
else:
    st.info("No accounts are currently locked")

with st.sidebar:
    st.divider()
    if st.button ("Log Out"):
        st.session_state["logged_in"] = False
        st.switch_page("Home.py")