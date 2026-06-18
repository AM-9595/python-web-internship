from fastapi import FastAPI
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    age: int

app = FastAPI()
users = []
user = {}
@app.get("/users")
def show_users():
    return {"Users List": users}

@app.get("/users/{user_id}")
def user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user


@app.post("/users")
def create_user(user: UserCreate):
    global new_id
    new_user = {
    "id": new_id,
    "name": user.name,
    "email": user.email,
    "age": user.age
}
    users.append(new_user)
    new_id = len(users) + 1
    return new_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for i, user in enumerate(users):
        if user["id"] == user_id:
            del users[i]
            return None
    raise HTTPException(status_code=404, detail="User not found")
