from abc import ABC, abstractmethod
import csv
import json
from typing import List, Optional


# ---------------------------------------------------------
# 1. Strategy Pattern: Discount Strategies
# ---------------------------------------------------------
class DiscountStrategy(ABC):

    @abstractmethod
    def apply(self, total: float) -> float:
        """Applies a discount calculation to the order total."""
        pass


class NoDiscount(DiscountStrategy):

    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):

    def __init__(self, percentage: float):
        if percentage < 0 or percentage > 100:
            raise ValueError("Discount percentage must be between 0 and 100.")
        self.__percentage: float = percentage

    def apply(self, total: float) -> float:
        return total * (1.0 - (self.__percentage / 100.0))


class BulkDiscount(DiscountStrategy):

    def __init__(self, threshold: float, amount: float):
        if threshold < 0 or amount < 0:
            raise ValueError("Threshold and discount amount cannot be negative.")
        self.__threshold: float = threshold
        self.__amount: float = amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return max(0.0, total - self.__amount)
        return total


class StudentDiscount(DiscountStrategy):
    """Fourth custom strategy extending the discount behaviors."""

    def __init__(self, flat_discount: float):
        if flat_discount < 0:
            raise ValueError("Student discount cannot be negative.")
        self.__flat_discount: float = flat_discount

    def apply(self, total: float) -> float:
        return max(0.0, total - self.__flat_discount)


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
# 3. Abstract Base Class: Product (with Validation)
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
        if price <= 0:
            raise ValueError("Product price must be greater than zero.")
        if stock < 0:
            raise ValueError("Product stock quantity cannot be negative.")

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
        if quantity < 0:
            raise ValueError("Stock update quantity cannot be negative.")
        self.__stock = quantity

    def display_information(self) -> None:
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock}",
            end="",
        )

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass


# ---------------------------------------------------------
# 4. Subclasses: PhysicalProduct & DigitalProduct
# ---------------------------------------------------------
class PhysicalProduct(Product):

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
        weight: float,
    ):
        if weight <= 0:
            raise ValueError("Physical product weight must be greater than zero.")
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight: float = weight

    def get_weight(self) -> float:
        return self.__weight

    def display_information(self) -> None:
        super().display_information()
        print(f" | Weight: {self.__weight}kg", end="")

    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping and handling."

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
        if download_size <= 0:
            raise ValueError("Download size must be greater than zero.")
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
# 5. Factory Pattern: ProductFactory
# ---------------------------------------------------------
class ProductFactory:

    @staticmethod
    def create(
        product_type: str,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
        extra_param: float,
    ) -> Product:
        ptype = product_type.strip().lower()
        if ptype == "physical":
            return PhysicalProduct(
                product_id, name, price, stock, supplier, extra_param
            )
        elif ptype == "digital":
            return DigitalProduct(
                product_id, name, price, stock, supplier, extra_param
            )
        else:
            raise ValueError(f"Unknown product type: {product_type}")


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
                print()
        print("-----------------------------------------------------------------")

    def get_products(self) -> List[Product]:
        return self.products


# ---------------------------------------------------------
# 7. Composition: OrderLine and Order Classes
# ---------------------------------------------------------
class OrderLine:

    def __init__(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("OrderLine quantity must be greater than zero.")
        self.product: Product = product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.product.get_price() * self.quantity


class Order:

    def __init__(
        self, order_id: str, discount: DiscountStrategy = NoDiscount()
    ) -> None:
        self.order_id: str = order_id
        self.order_lines: List[OrderLine] = []
        self.discount: DiscountStrategy = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.discount = discount

    def calculate_total(self) -> float:
        subtotal = sum(
            line.calculate_subtotal() for line in self.order_lines
        )
        return self.discount.apply(subtotal)


# ---------------------------------------------------------
# 8. Robust Input Helper & CSV File Loader
# ---------------------------------------------------------
def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def load_products(path: str, inventory: Inventory, suppliers: dict) -> None:
    loaded = 0
    try:
        file = open(path, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            header = next(reader, None)  # skip header
            for row in reader:
                if not row or len(row) < 6:
                    continue
                ptype, pid, name, price_str, stock_str, extra_str = [
                    r.strip() for r in row[:6]
                ]
                try:
                    price = float(price_str)
                    stock = int(stock_str)
                    extra = float(extra_str)

                    # Default supplier for CSV import
                    sup_id = "S_CSV"
                    if sup_id not in suppliers:
                        suppliers[sup_id] = Supplier(
                            sup_id, "CSV Supplier", "csv@supplier.com"
                        )
                    supplier = suppliers[sup_id]

                    product = ProductFactory.create(
                        ptype, pid, name, price, stock, supplier, extra
                    )
                    inventory.add_product(product)
                    loaded += 1
                except ValueError as e:
                    print(
                        f"Skipping invalid row {row} due to error: {e}"
                    )
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")

# ---------------------------------------------------------
# 9. Main Execution Entry Point
# ---------------------------------------------------------
if __name__ == "__main__":
    print("========================================")
    print("INVENTORY MANAGEMENT SYSTEM (LAB 9)")
    print("========================================")

    # Test Supplier and Factory creation
    supplier = Supplier("S001", "TechCorp Ltd", "contact@techcorp.com")
    inventory = Inventory()

    # Load products using factory
    p1 = ProductFactory.create(
        "physical", "P001", "Desk Lamp", 25.00, 10, supplier, 1.5
    )
    d1 = ProductFactory.create(
        "digital", "D001", "Photo Editor", 49.90, 100, supplier, 45.0
    )

    inventory.add_product(p1)
    inventory.add_product(d1)

    inventory.display_all()

    # Test Strategy Pattern with Order
    order = Order("ORD-001", PercentageDiscount(10))
    order.add_order_line(p1, 2)  # 2 * 25.00 = 50.00
    order.add_order_line(d1, 1)  # 1 * 49.90 = 49.90
    # Subtotal = 99.90, with 10% discount = 89.91

    print(f"Order Subtotal: ${99.90:.2f}")
    print(f"Order Total with 10% Discount: ${order.calculate_total():.2f}")

    # Switch strategy to BulkDiscount
    order.set_discount(BulkDiscount(50.0, 15.0))
    print(f"Order Total with Bulk Discount: ${order.calculate_total():.2f}")