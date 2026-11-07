from abc import ABC, abstractmethod
import json
from typing import List, Optional


# ---------------------------------------------------------
# 1. Interfaces (Abstract Base Classes)
# ---------------------------------------------------------
class CanBeShipped(ABC):

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Calculates shipping cost based on product characteristics."""
        pass


# ---------------------------------------------------------
# 2. Association: Supplier Class
# ---------------------------------------------------------
class Supplier:

    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self.__supplier_id: str = supplier_id
        self.__name: str = name
        self.__contact_email: str = contact_email

    def get_supplier_id(self) -> str:
        return self.__supplier_id

    def get_name(self) -> str:
        return self.__name

    def get_contact_email(self) -> str:
        return self.__contact_email

    def display_information(self) -> None:
        print(
            f"Supplier ID: {self.__supplier_id} | Name: {self.__name} | Email: {self.__contact_email}"
        )


# ---------------------------------------------------------
# 3. Abstract Base Class: Product (Associated with Supplier)
# ---------------------------------------------------------
class Product(ABC):

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
    ):
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.__supplier: Supplier = supplier

    def get_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def update_stock(self, quantity: int) -> None:
        self.__stock = quantity

    def display_information(self) -> None:
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock}",
            end="",
        )

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Abstract method to define how the product is fulfilled/delivered."""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Converts product attributes to a dictionary for JSON saving."""
        pass


# ---------------------------------------------------------
# 4. Subclass: PhysicalProduct (Inherits Product & CanBeShipped)
# ---------------------------------------------------------
class PhysicalProduct(Product, CanBeShipped):

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
        weight: float,
    ):
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight: float = weight

    def get_weight(self) -> float:
        return self.__weight

    def display_information(self) -> None:
        super().display_information()
        print(f" | Weight: {self.__weight}kg", end="")

    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping and handling."

    def calculate_shipping_cost(self) -> float:
        return 5.00 + (self.__weight * 2.00)

    def to_dict(self) -> dict:
        return {
            "type": "physical",
            "id": self.get_id(),
            "name": self.get_name(),
            "price": self.get_price(),
            "stock": self.get_stock(),
            "supplier_id": self.get_supplier().get_supplier_id(),
            "supplier_name": self.get_supplier().get_name(),
            "supplier_email": self.get_supplier().get_contact_email(),
            "weight": self.__weight,
        }


# ---------------------------------------------------------
# 5. Subclass: DigitalProduct (Inherits Product)
# ---------------------------------------------------------
class DigitalProduct(Product):

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
        download_size: float,
    ):
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size: float = download_size

    def get_download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        super().display_information()
        print(f" | Download Size: {self.__download_size}MB", end="")

    def get_fulfilment_info(self) -> str:
        return "Delivered digitally via instant download link."

    def to_dict(self) -> dict:
        return {
            "type": "digital",
            "id": self.get_id(),
            "name": self.get_name(),
            "price": self.get_price(),
            "stock": self.get_stock(),
            "supplier_id": self.get_supplier().get_supplier_id(),
            "supplier_name": self.get_supplier().get_name(),
            "supplier_email": self.get_supplier().get_contact_email(),
            "download_size": self.__download_size,
        }


# ---------------------------------------------------------
# 6. Aggregation: Inventory Class
# ---------------------------------------------------------
class Inventory:

    def __init__(self) -> None:
        self.products: List[Product] = []

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def remove_product(self, product_id: str) -> None:
        self.products = [
            p for p in self.products if p.get_id().lower() != product_id.lower()
        ]

    def search_product(self, product_id: str) -> Optional[Product]:
        for product in self.products:
            if product.get_id().lower() == product_id.lower():
                return product
        return None

    def display_all(self) -> None:
        print("Current Inventory")
        print("-----------------------------------------------------------------")
        if not self.products:
            print("Inventory is empty.")
        else:
            for product in self.products:
                product.display_information()
                print()  # Newline after each product info line
        print("-----------------------------------------------------------------")

    def get_products(self) -> List[Product]:
        return self.products


# ---------------------------------------------------------
# 7. Composition: OrderLine and Order Classes
# ---------------------------------------------------------
class OrderLine:

    def __init__(self, product: Product, quantity: int) -> None:
        self.product: Product = product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.product.get_price() * self.quantity


class Order:

    def __init__(self, order_id: str) -> None:
        self.order_id: str = order_id
        self.order_lines: List[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self.order_lines)


# ---------------------------------------------------------
# 8. System Operations & Functions
# ---------------------------------------------------------
def add_product(inventory: Inventory, suppliers: dict) -> None:
    print("Add New Product")
    print("Select Product Type:")
    print("1. Physical Product")
    print("2. Digital Product")
    choice = input("Enter choice (1/2): ").strip()

    product_id = input("Product ID: ")
    product_name = input("Product Name: ")

    price_input = input("Price: ").strip()
    if price_input.startswith("$"):
        price_input = price_input[1:]
    price = float(price_input)

    stock = int(input("Stock Quantity: "))

    # Simple association handling: select or create a default supplier
    supplier_id = input("Supplier ID (e.g., S001): ").strip()
    if supplier_id in suppliers:
        supplier = suppliers[supplier_id]
    else:
        supplier_name = input("Supplier Name: ").strip()
        supplier_email = input("Supplier Email: ").strip()
        supplier = Supplier(supplier_id, supplier_name, supplier_email)
        suppliers[supplier_id] = supplier

    if choice == "1":
        weight = float(input("Weight (kg): "))
        product = PhysicalProduct(
            product_id, product_name, price, stock, supplier, weight
        )
    elif choice == "2":
        download_size = float(input("Download Size (MB): "))
        product = DigitalProduct(
            product_id, product_name, price, stock, supplier, download_size
        )
    else:
        print("Invalid type selected. Defaulting to Physical Product.")
        weight = float(input("Weight (kg): "))
        product = PhysicalProduct(
            product_id, product_name, price, stock, supplier, weight
        )

    inventory.add_product(product)
    print("Product added successfully!")


def update_stock(inventory: Inventory, transaction_history: list) -> None:
    print("Update Stock")
    product_id = input("Enter Product ID: ")
    product = inventory.search_product(product_id)

    if product:
        print("Product Found:")
        print("Name:", product.get_name())
        print("Current Stock:", product.get_stock())

        new_stock = int(input("New Stock Quantity: "))

        transaction_amount = new_stock - product.get_stock()
        transaction_history.append(transaction_amount)

        product.update_stock(new_stock)
        print("Stock updated successfully!")
    else:
        print("Product not found.")


def load_inventory() -> tuple[Inventory, list, dict]:
    inventory = Inventory()
    transaction_history = []
    suppliers = {}

    try:
        with open("inventory.json", "r") as file:
            data = json.load(file)

            products_data = data.get("inventory", [])
            transaction_history = data.get("transaction_history", [])

            for p_data in products_data:
                sup_id = p_data.get("supplier_id", "S001")
                sup_name = p_data.get("supplier_name", "Default Supplier")
                sup_email = p_data.get("supplier_email", "supplier@shop.com")

                if sup_id not in suppliers:
                    suppliers[sup_id] = Supplier(sup_id, sup_name, sup_email)
                supplier = suppliers[sup_id]

                ptype = p_data.get("type", "physical")
                if ptype == "digital":
                    download_size = p_data.get("download_size", 100.0)
                    product = DigitalProduct(
                        p_data["id"],
                        p_data["name"],
                        p_data["price"],
                        p_data["stock"],
                        supplier,
                        download_size,
                    )
                else:
                    weight = p_data.get("weight", 1.0)
                    product = PhysicalProduct(
                        p_data["id"],
                        p_data["name"],
                        p_data["price"],
                        p_data["stock"],
                        supplier,
                        weight,
                    )
                inventory.add_product(product)

            print("inventory.json found.")
            print("Inventory loaded successfully.")

            return inventory, transaction_history, suppliers

    except FileNotFoundError:
        print("inventory.json not found.")
        print("Starting with empty inventory.")

        return inventory, [], suppliers


def save_inventory(inventory: Inventory, transaction_history: list) -> None:
    products_data = [product.to_dict() for product in inventory.get_products()]
    data = {
        "inventory": products_data,
        "transaction_history": transaction_history,
    }

    with open("inventory.json", "w") as file:
        json.dump(data, file, indent=4)

    print("Inventory saved successfully to inventory.json.")


def menu() -> None:
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


# ---------------------------------------------------------
# 9. Main Program Execution
# ---------------------------------------------------------
inventory, transaction_history, suppliers = load_inventory()

# Add default suppliers and products if inventory is empty
if not inventory.get_products():
    default_supplier = Supplier(
        "S001", "TechCorp Ltd", "contact@techcorp.com"
    )
    suppliers["S001"] = default_supplier

    inventory.add_product(
        PhysicalProduct(
            "P001", "Laptop", 1200.00, 15, default_supplier, 2.2
        )
    )
    inventory.add_product(
        PhysicalProduct("P002", "Mouse", 25.50, 40, default_supplier, 0.15)
    )
    inventory.add_product(
        DigitalProduct(
            "P003",
            "Operating System",
            145.00,
            100,
            default_supplier,
            4500.0,
        )
    )

print("========================================")
print("INVENTORY MANAGEMENT SYSTEM (LAB 8)")
print("========================================")

while True:
    menu()
    option = input("Enter option: ")

    if option == "1":
        inventory.display_all()

    elif option == "2":
        add_product(inventory, suppliers)

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
            print(
                f"Supplier: {product.get_supplier().get_name()} ({product.get_supplier().get_contact_email()})"
            )

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