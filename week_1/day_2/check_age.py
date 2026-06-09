a = int(input("Введи свой возвраст:"))
if a < 14:
    print("Ребёнок")
elif a > 13 and a < 18:
    print("Подросток")
elif a > 17 and a < 60:
    print("Взрослый")
elif a > 59:
    print("Пенсионер")