def load_inventory():
    orders = []

    try:
        with open("orders.txt", "r") as file:
            for line in file:
                line = line.strip()

                if line:
                    parts = line.split(",")

                    order_id = int(parts[0])
                    product_name = parts[1]
                    quantity = int(parts[2])

                    orders.append([order_id, product_name, quantity])

    except FileNotFoundError:
        orders = []

    return orders


def save_inventory(orders):
    with open("orders.txt", "w") as file:
        for order in orders:
            file.write(f"{order[0]},{order[1]},{order[2]}\n")


# Main program
orders = load_inventory()

print("Current Orders:")

for order in orders:
    print(f"{order[0]}, {order[1]}, {order[2]}")

product_name = input("\nEnter Product Name: ")
quantity = int(input("Enter Quantity: "))

if orders:
    new_order_id = orders[-1][0] + 1
else:
    new_order_id = 1001

new_order = [new_order_id, product_name, quantity]
orders.append(new_order)

print("\nNew Order Added:")
print(f"{new_order_id},{product_name},{quantity}")

save_inventory(orders)

print("\nOrder successfully saved to orders.txt")