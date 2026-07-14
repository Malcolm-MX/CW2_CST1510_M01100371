import streamlit as st
from hashing import generateHash, validateHash
from app_model.users import add_user, get_user
from app_model.db import connect_database
from app_model.users import reset_failed_attempts
from app_model.users import failed_attempts_increment
from hashing import generateHash, validateHash, passwordValidation
conn = connect_database()

st.set_page_config(page_title="Home",page_icon="🏠",layout="wide")

st.title("Welcome to the main page 🏠")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'role' not in st.session_state:
    st.session_state['role'] = None

if st.session_state.get('logged_in'):
    st.info("You are already logged in. Log out by navigating to the dashboard, then sidebar in order to access Registration & Log In.")
    if st.button("Go to Dashboard"):
        st.switch_page("pages/1_Cyber Incidents.py")
    st.stop()



tab_login, tab_register, tab_admin = st.tabs(["Login","Register","Admin"])

adminUsername = "admin"
adminPasswordHash = generateHash("adminPassword123")

with tab_login:
    login_username = st.text_input("Username", key = "login_username")
    login_password = st.text_input("Password", type = "password", key = "login_password")
    
    
    if st.button("Log In"):
        user_row = get_user(conn, login_username)
        if user_row:
            id, userName, userHash = user_row[:3]

            cur = conn.cursor()
            cur.execute("SELECT locked FROM users WHERE username = ?", (login_username,))
            is_locked = cur.fetchone()[0]

            if is_locked:
                st.error("Account locked due to too many failed attempt. Re-register as a new user.")
            elif login_username == userName and validateHash(login_password,userHash):
                reset_failed_attempts(conn, login_username)
                st.session_state["logged_in"] = True
                st.session_state["role"] = "user"
                st.success("Logged in successfully")
                st.switch_page("pages/1_Cyber Incidents.py")
            else:
                failed_attempts_increment(conn, login_username)
                st.error("Invalid username or password. You have 5 attempts in total. If you are incorrect 5 times, your account will be locked.")
        else:
            st.error("Invalid username or password")            
        
        

with tab_register:
    register_username = st.text_input("New Username")
    register_password = st.text_input("New Password", type="password")
    
    if st.button("Register"):
        is_valid, message = passwordValidation(register_password)
        if not is_valid:
            st.error(message)
        else:
            hash_password = generateHash(register_password)
            st.session_state["logged_in"] = False 
            add_user(conn, register_username, hash_password)
            st.success("Registration successful! Please log in.")

with tab_admin:
    st.subheader("Admin Login")
    admin_username = st.text_input("Admin Username", key="admin_username")
    admin_password = st.text_input("Admin Password", type = "password", key="admin_password")

    if st.button("Admin Log In"):
        if admin_username == adminUsername and validateHash(admin_password, adminPasswordHash):
            st.session_state["logged_in"] = True
            st.session_state["role"] = "admin"
            st.success("Admin login successful")
            st.switch_page("pages/5_Admin Page.py")
        else:
            st.error("Maybe you are not an admin?")
        

