import pandas as pd

def migrate_cyber_incidents(conn): 
    #One off migration to read CSV into a dataframe and the pu it in SQL as a table
    data = pd.read_csv(r'DATA\cyber_incidents.csv')
    data.to_sql('cyber_incidents',conn,if_exists ='replace', index = False)

def get_all_cyber_incidents(conn):
    ## Query the full cyber_incidents table back out as a DataFrame
    sql = 'SELECT * FROM cyber_incidents'
    data = pd.read_sql(sql,conn)
    return (data)