from users_repository import (
    create_user as repo_create_user,
    get_user_by_id as repo_get_user,
    get_all_users as repo_get_all,
    delete_user as repo_delete_user
)

def create_user(name: str, email: str, age: int) -> dict:
    if age < 0:
        raise ValueError("Age cannot be negative")
    user_id = repo_create_user(name, email, age)
    return {"id": user_id, "name": name, "email": email, "age": age}

def get_user(user_id: int) -> dict | None:
    return repo_get_user(user_id)

def get_all_users() -> list[dict]:
    return repo_get_all()

def delete_user(user_id: int) -> bool:
    return repo_delete_user(user_id)