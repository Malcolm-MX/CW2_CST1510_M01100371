import pandas as pd 

def migrate_it_tickets(conn):
    #One off migration to read CSV into a dataframe and the pu it in SQL as a table
    data = pd.read_csv(r'DATA\it_tickets.csv')
    data.to_sql('it_tickets',conn, if_exists='replace', index = False)

def get_all_it_tickets(conn):
    #Query the full it_tickets table back out as a DataFrame
    sql = 'SELECT * FROM it_tickets'
    data = pd.read_sql(sql,conn) 
    return (data)
