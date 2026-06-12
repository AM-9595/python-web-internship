numbers = [3, 7, 2, 9, 4, 6, 1, 8, 5]
print("Сумма:", sum(numbers))
print("Среднее:", sum(numbers)/len(numbers))
print("Максимум:", max(numbers))
print("Минимум:", min(numbers))
print("Четные:", [n for n in numbers if n%2==0])
print("Нечетные:", [n for n in numbers if n%2!=0])

print("---")

strings = ["cat", "dog", "snake", "butterfly", "python", "mansur"]
print("Длиннее 5:", [s for s in strings if len(s)>5])
print("Верхний регистр:", [s.upper() for s in strings])
print("По длине:", sorted(strings, key=len))

print("---")

user = {"id": 1, "name": "Ivan", "age": 22, "email": "ivan@example.com"}
print(f"Пользователь {user['name']}, возраст {user['age']}, email {user['email']}")

print("---")

users = [
    {"id": 1, "name": "Ivan", "age": 22, "email": "ivan@example.com"},
    {"id": 2, "name": "Max", "age": 17, "email": "max@example.com"},
    {"id": 3, "name": "Petr", "age": 30, "email": "petr@example.com"},
]
print("Старше 18:")
for u in users:
    if u["age"] > 18:
        print(f"  {u['name']}, {u['age']}, {u['email']}")
email = input("Введите email: ")
found = None
for u in users:
    if u["email"] == email:
        found = u
        break
print(found)
total = 0
for u in users:
    total += u["age"]
print("Средний возраст:", total / len(users))