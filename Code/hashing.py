import bcrypt#Hashing using bcrypt

#Starting with my generateHash function, I will pass pasw as a parameter
def generateHash(psw):
    byte_psw = psw.encode('utf-8') #I am encoding the parameter psw with utf-8 encoding to turn it into binary
    salt = bcrypt.gensalt()#Generating a salt
    hash = bcrypt.hashpw(byte_psw,salt) #Now hashing - salt+binary password
    return hash.decode('utf-8') 


#Validating Hash Vs Psw

def validateHash(psw, storedHash):
    byte_psw = psw.encode('utf-8')
    byte_hash = storedHash.encode('utf-8')
    is_valid = bcrypt.checkpw(byte_psw, byte_hash) #The validation is centred around comparing encoded hash to encoded password
    return is_valid

#All these password validations were utilised in my Home.py to make sure that the user doesn't enter a weak password when registering
#It's an extra security feature I added, the code below is super simple and self explanatory anyways, just validation checks on the password a user enters
def passwordValidation(password):
    if len(password) < 8: #length of password must be more than 8
        return False, "Password must be at least 8 characters long."
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one number."
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter."
    if not any(char.islower() for char in password):
        return False, "Password must contain at least one lowercase letter."
    if not any(char in "!@#$%^&*{}\|/`~,.-_><:;[]" for char in password):
        return False, "Password must contain at least one special character."
    return True, ""