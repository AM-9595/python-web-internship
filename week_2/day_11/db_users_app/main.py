from users_repository import create_user, get_user_by_id, get_all_users, delete_user


def main():

    print("Создание пользователей.")
    id1 = create_user("Alice", "alice@example.com", 25)
    id2 = create_user("Bob", "bob@example.com", 30)
    id3 = create_user("Charlie", "charlie@example.com", 22)
    print(f"Созданы пользователи с ID: {id1}, {id2}, {id3}\n")

    print("Получение пользователя с ID=2:")
    user = get_user_by_id(2)
    print(user, "\n")

    print("Все пользователи:")
    all_users = get_all_users()
    for u in all_users:
        print(f"{u['id']}: {u['name']} ({u['email']}), возраст {u['age']}")
    print()

    print("Удаление пользователя с ID=1")
    deleted = delete_user(1)
    print(f"Удалён: {deleted}\n")

    print("Пользователи после удаления:")
    all_users = get_all_users()
    for u in all_users:
        print(f"{u['id']}: {u['name']} ({u['email']}), возраст {u['age']}")


if __name__ == "__main__":
    main()