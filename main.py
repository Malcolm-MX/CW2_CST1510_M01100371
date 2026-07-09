import bcrypt
import pandas as pd

from app_model.db import conn
from app_model.users import add_user, get_user

#Hashing using bcrypt

def generateHash(psw):
    byte_psw = psw.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(byte_psw,salt)
    return hash.decode('utf-8')


#Validating Hash Vs Psw

def validateHash(psw, storedHash):
    byte_psw = psw.encode('utf-8')
    byte_hash = storedHash.encode('utf-8')
    is_valid = bcrypt.checkpw(byte_psw, byte_hash)
    return is_valid

#User Registration

def registerUser(conn):
    name = input("Enter your name: ")
    password = input("Enter your password: ")
    hash_password = generateHash(password)
    add_user(conn, name, hash_password)



#User Login

def logInUser(conn):
    name = input("Enter your name: ")
    password = input("Enter your password: ")
    id, userName, userHash = get_user(conn, name)
    print (f'Welcome {userName} !!')
    if name == userName and validateHash(password,userHash):
            return True
    return False
        

def main():
    while True:
        print("""Welcome to the system!
        Choose from the following options:
            1. To Register
            2. To Log In
            3. To Exit""")
        
        choice = input(': > ')

        if choice == '1':
            registerUser(conn)
        elif choice == '2':
            if logInUser(conn):
                print ("Login Successful")
            else:
                print("Incorrect log in. Try again!")
        elif choice == '3':
            print ("Goodbye!")
            break

if __name__ == '__main__':
    main()