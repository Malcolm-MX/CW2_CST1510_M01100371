import streamlit as st
from app_model.db import connect_database
from app_model.users import get_user, update_user
from hashing import generateHash, validateHash, passwordValidation

#If the user isn't logged in, they don't have access to this page, this is in pretty much all the pages
if not st.session_state.get('logged_in'):
    st.warning("Please log in to access this page.")
    if st.button("Go to Login Page"):
        st.switch_page("Home.py")
    st.stop()

# Admins don't have a real profile in the users table (hardcoded credentials),
#so I block them from this page entirely
if st.session_state.get('role') == 'admin':
        st.info("Admins don't have any business changing password or username, admin's a hardcoded role.")
        st.stop()

st.set_page_config(page_title="User Profile", layout = "wide")
st.title("User Profile")

#Get the currently logged-in users username from session_state,
#and use it to fetch their row from the database
conn = connect_database()
currentUsername = st.session_state.get("username")
user_row = get_user(conn, currentUsername)

if user_row:
    id, username, password_hash = user_row[:3]
    st.write(f"Username: {username}")
else:
    st.error("Could not find your account.")
    st.stop()

st.divider()

st.subheader("Change Username")

newUsername = st.text_input("New Username")
currentPasswordForUsername = st.text_input("Confirm Current Password", type="password", key="pw_for_username")

if st.button("Update Username"):
    #Verify the current password before allowing a username change
    if validateHash(currentPasswordForUsername, password_hash):
        update_user(conn, currentUsername, newUsername)
        st.session_state["username"] = newUsername
        st.success("Username updated successfully. Don't forget it again.")
    else:
        st.error("Incorrect password. You might have to create a new account if you don't remember it.")

st.divider()

st.subheader("Change Password")

newPassword = st.text_input("New Password", type="password", key="new_password")
currentPasswordForPw = st.text_input("Confirm Current Password", type="password", key="pw_for_password")

if st.button("Update Password"):
    #Verify the current password before allowing a password change
    if validateHash(currentPasswordForPw, password_hash):
        #Enforcing the same password strength rules as when a user registers a new password
        is_valid, message = passwordValidation(newPassword)
        if not is_valid:
            st.error(message)
        else:
            #Hashing this new password aand storing it in the database
            new_hash = generateHash(newPassword)
            cur = conn.cursor()
            cur.execute("UPDATE users SET password_hash = ? WHERE username = ?", (new_hash, currentUsername))
            conn.commit()
            st.success("Password updated successfully.")
    else:
        st.error("Incorrect current password. Password not changed unfortunately.")

