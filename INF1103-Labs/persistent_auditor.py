import json


def add_product(inventory):
    print("Add New Product")

    product_id = input("Product ID: ")
    product_name = input("Product Name: ")
    price = float(input("Price: "))
    stock = int(input("Stock Quantity: "))

    product = {
        "id": product_id,
        "name": product_name,
        "price": price,
        "stock": stock
    }

    inventory.append(product)

    print("Product added successfully!")


def update_stock(inventory, transaction_history):
    print("Update Stock")

    product_id = input("Enter Product ID: ")

    product = search_product(inventory, product_id)

    if product:
        print("Product Found:")
        print("Name:", product["name"])
        print("Current Stock:", product["stock"])

        new_stock = int(input("New Stock Quantity: "))

        # Store the transaction amount
        transaction_amount = new_stock - product["stock"]
        transaction_history.append(transaction_amount)

        product["stock"] = new_stock

        print("Stock updated successfully!")
    else:
        print("Product not found.")


def search_product(inventory, product_id):
    for product in inventory:
        if product["id"].lower() == product_id.lower():
            return product

    return None


def display_all(inventory):
    print("Current Inventory")
    print("------------------------------------------------")

    for product in inventory:
        print(
            f"ID: {product['id']} | "
            f"Name: {product['name']} | "
            f"Price: ${product['price']:.2f} | "
            f"Stock: {product['stock']}"
        )

    print("------------------------------------------------")


def load_inventory():
    try:
        with open("inventory.json", "r") as file:
            data = json.load(file)

            inventory = data.get("inventory", [])
            transaction_history = data.get("transaction_history", [])

            print("inventory.json found.")
            print("Inventory loaded successfully.")

            return inventory, transaction_history

    except FileNotFoundError:
        print("inventory.json not found.")
        print("Starting with empty inventory.")

        return [], []


def save_inventory(inventory, transaction_history):
    data = {
        "inventory": inventory,
        "transaction_history": transaction_history
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


# Main program

inventory, transaction_history = load_inventory()

# Add three default products if inventory is empty
if not inventory:
    inventory = [
        {
            "id": "P001",
            "name": "Laptop",
            "price": 1200.00,
            "stock": 15
        },
        {
            "id": "P002",
            "name": "Mouse",
            "price": 25.50,
            "stock": 40
        },
        {
            "id": "P003",
            "name": "Keyboard",
            "price": 45.00,
            "stock": 25
        }
    ]


print("========================================")
print("INVENTORY MANAGEMENT SYSTEM")
print("========================================")

while True:
    menu()

    option = input("Enter option: ")

    if option == "1":
        display_all(inventory)

    elif option == "2":
        add_product(inventory)

    elif option == "3":
        update_stock(inventory, transaction_history)

    elif option == "4":
        print("Search Product")

        product_id = input("Enter Product ID: ")

        product = search_product(inventory, product_id)

        if product:
            print("Product Found")
            print("------------------------------------------------")
            print("ID:", product["id"])
            print("Name:", product["name"])
            print(f"Price: ${product['price']:.2f}")
            print("Stock:", product["stock"])
            print("------------------------------------------------")
        else:
            print("Product not found.")

    elif option == "5":
        print("Saving inventory...")
        save_inventory(inventory, transaction_history)

    elif option == "6":
        print("Saving inventory before exit...")

        data = {
            "inventory": inventory,
            "transaction_history": transaction_history
        }

        with open("inventory.json", "w") as file:
            json.dump(data, file, indent=4)

        print("Inventory saved successfully.")
        print("Thank you for using Inventory Management System.")
        print("Program terminated")

        break

    else:
        print("Invalid option. Please choose 1-6.")