import streamlit as st
from hashing import generateHash, validateHash
from app_model.users import add_user, get_user
from app_model.db import connect_database
from app_model.users import reset_failed_attempts
from app_model.users import failed_attempts_increment
from hashing import generateHash, validateHash, passwordValidation

#Opening a database connection
conn = connect_database()

#Setting the tab name to "Home" with a page icon and making the layout wide so that diagrams are not squashed in a narrow layout
st.set_page_config(page_title="Home",page_icon="🏠",layout="wide")

#First main title to welcome the user to the page with it's own home icon
st.title("Welcome to the main page 🏠")

#Initialising session state keys
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'role' not in st.session_state:
    st.session_state['role'] = None

#If someone is logged in and 'logged in' is set to true, they don't have access to the login/register page unless they logout. It's an extra security feature
if st.session_state.get('logged_in'):
    st.info("You are already logged in. Log out by navigating to the dashboard, then sidebar in order to access Registration & Log In.")
    if st.button("Go to Dashboard"):
        st.switch_page("pages/1_Cyber Incidents.py")
    st.stop()
#This feature prevents multiple sessions of logging in without first ending your current session by logging out

#Assigning names to the different tabs
tab_login, tab_register, tab_admin = st.tabs(["Login","Register","Admin"])

#I hardcoded the admin username and password as a security feature, because I don't think any user should just be able to register as an admin,
# and login to see that private dashboard with other users information
adminUsername = "admin" #Admin username is admin
adminPasswordHash = generateHash("adminPassword123") #Admin password is adminPassword123

#Now working on the user login mechanism by having two tabs, login and register tab for them to fill out
with tab_login:
    login_username = st.text_input("Username", key = "login_username")
    login_password = st.text_input("Password", type = "password", key = "login_password")
    
    #Basically, if a user clicks log in, the cursor will establish a database connection to match their input details to an already registered user
    #If the details match, logged_in will be True, however if the details don't, logged in will be false and they'll get an error message as well as
    #5 more chances to get it right or their account will be locked
    if st.button("Log In"):
        user_row = get_user(conn, login_username)
        if user_row:
            id, userName, userHash = user_row[:3]

            cur = conn.cursor()
            cur.execute("SELECT locked FROM users WHERE username = ?", (login_username,))
            is_locked = cur.fetchone()[0] #the user profile can be locked after too many incorrect password attempts

            if is_locked:
                st.error("Account locked due to too many failed attempt. Re-register as a new user or contact admin to unlock your account, if you know the admin...")
            elif login_username == userName and validateHash(login_password,userHash):
                #correct credentials will log in the user though and it will reset any failed attempts they had before               #
                reset_failed_attempts(conn, login_username)
                st.session_state["logged_in"] = True
                st.session_state["role"] = "user"
                st.success("Logged in successfully")
                st.switch_page("pages/1_Cyber Incidents.py")
            else:
                #This is the else block for the increment failed attempts counter
                #It will lock the account after 5 failed attempts
                failed_attempts_increment(conn, login_username)
                st.error("Invalid username or password. You have 5 attempts remaining. If you are incorrect 5 times, your account will be locked.")
        else:
            st.error("Invalid username or password")            
        
        
#Defining some variables for the register tab now
with tab_register:
    register_username = st.text_input("New Username")
    register_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    
    if st.button("Register"):
        #Checking if the passwords match before validating or reistering the account
        if register_password != confirm_password:
            st.error("Passwords don't match. Try again please")
        else:
            #I took the passwordValidation function from my hashing.py file, basically to enforce
            #some password strength rules, also another additional security feature
            is_valid, message = passwordValidation(register_password)
            if not is_valid:
                st.error(message)
            else:
                #Never store passwords as plain text, so i'm hashing them before I store them using the generateHash function which i also imported from hashing.py
                hash_password = generateHash(register_password)
                st.session_state["logged_in"] = False 
                add_user(conn, register_username, hash_password)
                st.success("Registration successful! Please log in.")

#Last admin tab 
with tab_admin:
    st.subheader("Admin Login")
    admin_username = st.text_input("Admin Username", key="admin_username")
    admin_password = st.text_input("Admin Password", type = "password", key="admin_password")

    if st.button("Admin Log In"):
        #I'm making sure the credential check is separate from normal users, because remember admin is hardcoded login credentials and it's not stored
        #in user table because I don't want it to be accessible to just anyone since the admin dashboard allows one to unlock locked accounts and view list of users
        if admin_username == adminUsername and validateHash(admin_password, adminPasswordHash):
            st.session_state["logged_in"] = True
            st.session_state["role"] = "admin"
            st.success("Admin login successful")
            st.switch_page("pages/5_Admin Page.py")
        else:
            st.error("Maybe you are not an admin?")
            