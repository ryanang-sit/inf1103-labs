from abc import ABC, abstractmethod
import json


# ---------------------------------------------------------
# 1. Interfaces (Abstract Base Classes)
# ---------------------------------------------------------
class CanBeShipped(ABC):

    @abstractmethod
    def calculate_shipping_cost(self):
        """Calculates shipping cost based on product characteristics."""
        pass


# ---------------------------------------------------------
# 2. Abstract Base Class: Product
# ---------------------------------------------------------
class Product(ABC):

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
            f"Stock: {self.__stock}",
            end="",
        )

    @abstractmethod
    def get_fulfilment_info(self):
        """Abstract method to define how the product is fulfilled/delivered."""
        pass

    @abstractmethod
    def to_dict(self):
        """Converts product attributes to a dictionary for JSON saving."""
        pass


# ---------------------------------------------------------
# 3. Subclass: PhysicalProduct (Inherits Product & CanBeShipped)
# ---------------------------------------------------------
class PhysicalProduct(Product, CanBeShipped):

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight

    def get_weight(self):
        return self.__weight

    def display_information(self):
        super().display_information()
        print(f" | Weight: {self.__weight}kg")

    def get_fulfilment_info(self):
        return "Requires physical shipping and handling."

    def calculate_shipping_cost(self):
        # Simple rule: base fee $5.00 + $2.00 per kg
        return 5.00 + (self.__weight * 2.00)

    def to_dict(self):
        return {
            "type": "physical",
            "id": self.get_id(),
            "name": self.get_name(),
            "price": self.get_price(),
            "stock": self.get_stock(),
            "weight": self.__weight,
        }


# ---------------------------------------------------------
# 4. Subclass: DigitalProduct (Inherits Product)
# ---------------------------------------------------------
class DigitalProduct(Product):

    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.__download_size = download_size

    def get_download_size(self):
        return self.__download_size

    def display_information(self):
        super().display_information()
        print(f" | Download Size: {self.__download_size}MB")

    def get_fulfilment_info(self):
        return "Delivered digitally via instant download link."

    def to_dict(self):
        return {
            "type": "digital",
            "id": self.get_id(),
            "name": self.get_name(),
            "price": self.get_price(),
            "stock": self.get_stock(),
            "download_size": self.__download_size,
        }


# ---------------------------------------------------------
# 5. Inventory Class (Manages a collection of Products)
# ---------------------------------------------------------
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
        print("-----------------------------------------------------------------")
        if not self.__products:
            print("Inventory is empty.")
        else:
            for product in self.__products:
                product.display_information()
        print("-----------------------------------------------------------------")

    def get_products(self):
        return self.__products


# ---------------------------------------------------------
# 6. System Operations & Functions
# ---------------------------------------------------------
def add_product(inventory):
    print("Add New Product")
    print("Select Product Type:")
    print("1. Physical Product")
    print("2. Digital Product")
    choice = input("Enter choice (1/2): ").strip()

    product_id = input("Product ID: ")
    product_name = input("Product Name: ")

    # Clean up price input in case the user types '$'
    price_input = input("Price: ").strip()
    if price_input.startswith("$"):
        price_input = price_input[1:]
    price = float(price_input)

    stock = int(input("Stock Quantity: "))

    if choice == "1":
        weight = float(input("Weight (kg): "))
        product = PhysicalProduct(product_id, product_name, price, stock, weight)
    elif choice == "2":
        download_size = float(input("Download Size (MB): "))
        product = DigitalProduct(
            product_id, product_name, price, stock, download_size
        )
    else:
        print("Invalid type selected. Defaulting to Physical Product.")
        weight = float(input("Weight (kg): "))
        product = PhysicalProduct(product_id, product_name, price, stock, weight)

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
                ptype = p_data.get("type", "physical")
                if ptype == "digital":
                    download_size = p_data.get("download_size", 100.0)
                    product = DigitalProduct(
                        p_data["id"],
                        p_data["name"],
                        p_data["price"],
                        p_data["stock"],
                        download_size,
                    )
                else:
                    weight = p_data.get("weight", 1.0)
                    product = PhysicalProduct(
                        p_data["id"],
                        p_data["name"],
                        p_data["price"],
                        p_data["stock"],
                        weight,
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


# ---------------------------------------------------------
# 7. Main Program Execution
# ---------------------------------------------------------
inventory, transaction_history = load_inventory()

# Add default products if inventory is empty
if not inventory.get_products():
    inventory.add_product(
        PhysicalProduct("P001", "Laptop", 1200.00, 15, 2.2)
    )
    inventory.add_product(PhysicalProduct("P002", "Mouse", 25.50, 40, 0.15))
    inventory.add_product(
        DigitalProduct("P003", "Operating System", 145.00, 100, 4500.0)
    )

print("========================================")
print("INVENTORY MANAGEMENT SYSTEM (LAB 7)")
print("========================================")

while True:
    menu()
    option = input("Enter option: ")

    if option == "1":
        inventory.display_all()

    elif option == "2":
        add_product(inventory)

    elif option == "3":
        update_stock(inventory, transaction_history)

    elif option == "4":
        print("Search Product")
        product_id = input("Enter Product ID: ")
        product = inventory.search_product(product_id)

        if product:
            print("Product Found")
            print("-----------------------------------------------------------------")
            print("ID:", product.get_id())
            print("Name:", product.get_name())
            print(f"Price: ${product.get_price():.2f}")
            print("Stock:", product.get_stock())
            print("Fulfilment:", product.get_fulfilment_info())

            # Check if the product implements CanBeShipped interface
            if isinstance(product, CanBeShipped):
                shipping_cost = product.calculate_shipping_cost()
                print(f"Shipping Cost: ${shipping_cost:.2f}")

            print("-----------------------------------------------------------------")
        else:
            print("Product not found.")

    elif option == "5":
        print("Saving inventory...")
        save_inventory(inventory, transaction_history)

    elif option == "6":
        print("Saving inventory before exit...")
        save_inventory(inventory, transaction_history)

        print("Inventory saved successfully.")
        print("Thank you for using Inventory Management System.")
        print("Program terminated")
        break

    else:
        print("Invalid option. Please choose 1-6.")