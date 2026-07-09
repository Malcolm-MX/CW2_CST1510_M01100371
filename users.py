def add_user(conn, name, hash):
    cur = conn.cursor()
    sql = '''INSERT INTO users (username, password_hash) VALUES (?, ?)'''
    param = (name, hash)
    cur.execute(sql,param)
    conn.commit()

def migrate_users(conn):
    with open(r'DATA\users.txt', 'r') as f:
        users = f.readlines()
    for user in users:
        name, hash = user.strip().split(',')
        add_user(conn,name,hash)

def get_all_users(conn):
    cur = conn.cursor()
    sql = '''SELECT * FROM users'''
    cur.execute(sql)
    users = cur.fetchall()
    conn.close()
    return (users)

def get_user(conn,name):
    cur = conn.cursor()
    sql = '''SELECT * FROM users WHERE username = ?'''
    param = (name,)
    cur.execute(sql,param)
    user = cur.fetchone()
    conn.close()
    return (user)

def update_user(conn, old_name, new_name):
    cur = conn.cursor()
    sql = 'UPDATE users SET username = ? WHERE username = ?'
    param = (new_name, old_name) #Changed it up for readability
    cur.execute(sql,param)
    conn.commit()

def delete_user(conn,user_name):
    cur = conn.cursor()
    sql = 'DELETE FROM users WHERE username = ?'
    param = (user_name,) #Changed it up for readability
    cur.execute(sql,param)
    conn.commit()