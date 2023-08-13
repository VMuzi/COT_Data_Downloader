import pyodbc


def connectToDb(server,database,username,password):  
    connString = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password
    
    cnxn = pyodbc.connect(connString)
    cursor = cnxn.cursor()
    return cursor,cnxn

def execute_Create_SQL(sqlStatment,values,cursor):
    
    cursor.execute(sqlStatment,values)
