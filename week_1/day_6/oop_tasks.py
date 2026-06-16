class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

class Product:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

class Order:
    def __init__(self, id, user, products, status):
        self.id = id
        self.user = user
        self.products = products  # теперь обязательно передать список
        self.status = status      # обязательно передать строку

    def total_price(self):
        total = 0
        for p in self.products:
            total += p.price
        return total

    def add_product(self, product):
        self.products.append(product)

    def change_status(self, new_status):
        self.status = new_status


user = User(1, "Ivan", "ivan@example.com")
apple = Product(1, "Apple", 50)
banana = Product(2, "Banana", 30)

order = Order(100, user, [], "new")

order.add_product(apple)
order.add_product(banana)

# Выводим сумму
print(order.total_price())

# Меняем статус
order.change_status("поменяли")
print(order.status)

