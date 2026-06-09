a = int(input("Введи первое число: "))
b = int(input("Введи второе число: "))
c = input("Выбери операцию: +, -, *, /, %: ")
if c == "+":
    print(a + b)
elif c == "-":
    print(a - b)
elif c == "*":
    print(a * b)
elif c == "/":
    if b == 0:
        print("На 0 нельзя делить")
    else:
        print(a / b)

