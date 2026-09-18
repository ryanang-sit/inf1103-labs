def get_valid_input():
    while True:
        stock = input("Enter stock quantity (or 'quit' to exit): ")

        if stock.lower() == "quit":
            return "quit"

        try:
            stock = int(stock)

            if stock < 0:
                print("Error: Stock quantity cannot be negative.")
                continue

            return stock

        except ValueError:
            print("Error: Invalid input. Please enter a whole number.")

def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total

#initialize the inventory to zero in the start
inventory = 0
failed_entries = 0

#run in a continuous loop asking user to enter a stock quantity, until the user types quit
while True:
    stock = input("Enter stock quantity (or 'quit' to exit): ")

    #reporting
    if stock.lower() == "quit":
        print("Total Units Processed:", inventory)
        print("Number of Failed/Rejected Entries:", failed_entries)
        break

    if stock.startswith("-"):
        try:
            #accept stock values as integers
            stock = int(stock)

            #enforce business rules
            if stock < 0:
                print("Error: Stock quantity cannot be negative.")
                failed_entries += 1
                continue

            #handle invalid input
        except ValueError:
            print("Error: Invalid input. Please enter a whole number.")
            failed_entries += 1
            continue

    if not stock.isdigit():
        print("Error: Invalid input. Please enter a whole number.")
        failed_entries += 1
        continue

    stock = int(stock)

    inventory += stock

    #trigger overstock alert
    if inventory > 500:
        print("ALERT: Overstock! Inventory exceeds 500 units.")
        break