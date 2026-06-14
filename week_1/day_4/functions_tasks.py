def is_even(number):
    pass

def calculate_discount(price, discount_percent):
    pass

def find_user_by_id(users, user_id):
    for user in users:
        if user["id"] == user_id:
            return user
    return None
users = [
    {"id": 1, "name": "Ivan"},
    {"id": 2, "name": "Max"}
]

result = find_user_by_id(users, 1)
print(result)

result2 = find_user_by_id(users, 99)
print(result2)

# Проверка
if result2 is None:
    print("Пользователь не найден")

def validate_email(email):
    if "@" in email and "." in email:
        return "Все хорошо"
    else:
        return "Добавьте знак @ или Точку"
print(validate_email("max@example.com"))
print(validate_email("ivan@example"))
print(validate_email("petr.example.com"))


def divide(a, b):
    if b == 0:
        print("На ноль делить нельзя")
    return a / b

