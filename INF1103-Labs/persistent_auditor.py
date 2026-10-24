import json


class Product:

    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    def get_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def update_stock(self, quantity):
        self.__stock = quantity

    def display_information(self):
        print(
            f"ID: {self.__product_id} | "
            f"Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | "
            f"Stock: {self.__stock}"
        )

    def to_dict(self):
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }

class Inventory:

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        self.__products.append(product)

    def search_product(self, product_id):
        for product in self.__products:
            if product.get_id().lower() == product_id.lower():
                return product
        return None

    def display_all(self):
        print("Current Inventory")
        print("------------------------------------------------")
        if not self.__products:
            print("Inventory is empty.")
        else:
            for product in self.__products:
                product.display_information()
        print("------------------------------------------------")

    def get_products(self):
        return self.__products


def add_product(inventory):
    print("Add New Product")

    product_id = input("Product ID: ")
    product_name = input("Product Name: ")
    price = float(input("Price: "))
    stock = int(input("Stock Quantity: "))

    product = Product(product_id, product_name, price, stock)
    inventory.add_product(product)

    print("Product added successfully!")


def update_stock(inventory, transaction_history):
    print("Update Stock")

    product_id = input("Enter Product ID: ")
    product = inventory.search_product(product_id)

    if product:
        print("Product Found:")
        print("Name:", product.get_name())
        print("Current Stock:", product.get_stock())

        new_stock = int(input("New Stock Quantity: "))

        # Store the transaction amount
        transaction_amount = new_stock - product.get_stock()
        transaction_history.append(transaction_amount)

        product.update_stock(new_stock)

        print("Stock updated successfully!")
    else:
        print("Product not found.")


def load_inventory():
    inventory = Inventory()
    transaction_history = []

    try:
        with open("inventory.json", "r") as file:
            data = json.load(file)

            products_data = data.get("inventory", [])
            transaction_history = data.get("transaction_history", [])

            for p_data in products_data:
                product = Product(
                    p_data["id"],
                    p_data["name"],
                    p_data["price"],
                    p_data["stock"],
                )
                inventory.add_product(product)

            print("inventory.json found.")
            print("Inventory loaded successfully.")

            return inventory, transaction_history

    except FileNotFoundError:
        print("inventory.json not found.")
        print("Starting with empty inventory.")

        return inventory, []


def save_inventory(inventory, transaction_history):
    products_data = [product.to_dict() for product in inventory.get_products()]
    data = {
        "inventory": products_data,
        "transaction_history": transaction_history,
    }

    with open("inventory.json", "w") as file:
        json.dump(data, file, indent=4)

    print("Inventory saved successfully to inventory.json.")


def menu():
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")