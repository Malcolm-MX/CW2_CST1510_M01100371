import bcrypt#Hashing using bcrypt

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

def passwordValidation(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one number."
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter."
    return True, ""