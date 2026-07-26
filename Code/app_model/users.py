#Insert a new user row with the users username and hashed password
def add_user(conn, name, hash):
    cur = conn.cursor()
    sql = '''INSERT INTO users (username, password_hash) VALUES (?, ?)'''
    param = (name, hash)
    cur.execute(sql,param)
    conn.commit()

#It's a once off function to read the users txt and then insert each user into the users table
def migrate_users(conn):
    with open(r'DATA\users.txt', 'r') as f:
        users = f.readlines()
    for user in users:
        name, hash = user.strip().split(',')
        add_user(conn,name,hash)

#Returns every user as a list of tuples
def get_all_users(conn):
    cur = conn.cursor()
    sql = '''SELECT * FROM users'''
    cur.execute(sql)
    users = cur.fetchall()
    return (users)

def get_user(conn,name):
    #Look up a single user by username
    cur = conn.cursor()
    sql = '''SELECT * FROM users WHERE username = ?'''
    param = (name,)
    cur.execute(sql,param)
    user = cur.fetchone()
    return (user)

#Rename an existing user's username
def update_user(conn, old_name, new_name):
    cur = conn.cursor()
    sql = 'UPDATE users SET username = ? WHERE username = ?'
    param = (new_name, old_name) #Changed it up for readability
    cur.execute(sql,param)
    conn.commit()

#Permanently remove a user's account from the database
def delete_user(conn,user_name):
    cur = conn.cursor()
    sql = 'DELETE FROM users WHERE username = ?'
    param = (user_name,) #Changed it up for readability
    cur.execute(sql,param)
    conn.commit()

#Increment the failed login counter, then lock the account
#if it's reached 5 failed attempt
def failed_attempts_increment(conn, username):
    cur = conn.cursor()
    cur.execute("UPDATE users SET failed_attempts = failed_attempts + 1 WHERE username = ?", (username,))
    cur.execute("SELECT failed_attempts FROM users WHERE username = ?", (username,))
    attempts = cur.fetchone()[0]
    if attempts >= 5:
        cur.execute("UPDATE users SET locked = 1 WHERE username = ?", (username,))
    conn.commit()   

def reset_failed_attempts(conn, username):
#Reset the failed attempt counter and unlock the account
#used both after a successful login and by the admin's manual unlock
    cur = conn.cursor()
    cur.execute("UPDATE users SET failed_attempts = 0, locked = 0 WHERE username = ?", (username,))
    conn.commit()