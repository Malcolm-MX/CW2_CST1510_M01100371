import pandas as pd

def migrate_cyber_incidents(conn): 
    data = pd.read_csv(r'DATA\cyber_incidents.csv')
    data.to_sql('cyber_incidents',conn,if_exists ='replace', index = False)

def get_all_cyber_incidents(conn):
    sql = 'SELECT * FROM cyber_incidents'
    data = pd.read_sql(sql,conn)
    return (data)