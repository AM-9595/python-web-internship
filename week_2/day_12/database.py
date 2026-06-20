import psycopg2

def get_connection():
    conn = psycopg2.connect(
        dbname="11",
        user="postgres",
        password="123",
        host="localhost",
        port=5432
    )
    return conn