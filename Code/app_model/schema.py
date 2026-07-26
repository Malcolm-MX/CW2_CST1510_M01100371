def create_user_table(conn):
    #Create the users table if it doesn't already exist yet
    cur = conn.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL);
    '''
    cur.execute(sql)
    conn.commit()