from db import get_connection

def create_user(name, email, age):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                   CREATE TABLE IF NOT EXISTS users (
                       id SERIAL PRIMARY KEY,
                       name VARCHAR(255) NOT NULL,
                       email VARCHAR(255) UNIQUE NOT NULL,
                       age INTEGER NOT NULL
                   );
               """)
            conn.commit()
            print("Таблица users проверена/создана.")
            
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (name, email, age) VALUES (%s, %s, %s) RETURNING id;",
                (name, email, age)
            )
            user_id = cur.fetchone()[0]
            conn.commit()
            return user_id

def get_user_by_id(user_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, email, age FROM users WHERE id = %s;", (user_id,))
            row = cur.fetchone()
            if row:
                return {
                    "id": row[0],
                    "name": row[1],
                    "email": row[2],
                    "age": row[3]
                }
            return None

def get_all_users():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, email, age FROM users ORDER BY id;")
            rows = cur.fetchall()
            return [
                {
                    "id": row[0],
                    "name": row[1],
                    "email": row[2],
                    "age": row[3]
                }
                for row in rows
            ]

def delete_user(user_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
            deleted = cur.rowcount > 0
            conn.commit()
            return deleted