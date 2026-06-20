# users_repository.py
from database import get_connection

def create_user(name: str, email: str, age: int) -> int:
    """Создаёт пользователя и возвращает его ID."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (name, email, age) VALUES (%s, %s, %s) RETURNING id;",
                (name, email, age)
            )
            user_id = cur.fetchone()[0]
            conn.commit()
            return user_id

def get_user_by_id(user_id: int) -> dict | None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, email, age FROM users WHERE id = %s;", (user_id,))
            row = cur.fetchone()
            if row:
                return {"id": row[0], "name": row[1], "email": row[2], "age": row[3]}
            return None

def get_all_users() -> list[dict]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, email, age FROM users ORDER BY id;")
            rows = cur.fetchall()
            return [{"id": r[0], "name": r[1], "email": r[2], "age": r[3]} for r in rows]

def delete_user(user_id: int) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
            deleted = cur.rowcount > 0
            conn.commit()
            return deleted