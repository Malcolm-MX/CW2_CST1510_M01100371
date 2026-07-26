import pandas as pd

def migrate_datasets_metadata(conn):
    #One off migration to read CSV into a dataframe and the pu it in SQL as a table
    data = pd.read_csv(r'DATA\datasets_metadata.csv')
    data.to_sql('datasets_metadata',conn, if_exists='replace', index = False)

#Query the full datasets_metadata table back out as a DataFrame
def get_all_datasets_metadata(conn):
    sql = 'SELECT * FROM datasets_metadata'
    data = pd.read_sql(sql,conn) 
    return (data)

