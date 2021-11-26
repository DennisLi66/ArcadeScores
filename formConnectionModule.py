import os
from dotenv import load_dotenv #pip install python-dotenv
import mysql.connector #pip install mysql-connector-python

def formConnection():
    try:
        load_dotenv()
        conn = mysql.connector.connect(
            host=os.getenv('SQLHOST'),
            user=os.getenv('SQLUSER'),
            password=os.getenv('SQLPASSWORD'),
            database=os.getenv('SQLDATABASE')
            )
        return conn;        
    except:
        raise ValueError("There was no .env file or .env variables, or connection failed.")




if __name__ == '__main__':
    print('Testing MYSQL Connection...')
    connection = formConnection();
    connection.close();
    print('Connection Tested And Closed.');
