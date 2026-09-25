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

def calculate_tax(amount):
    tax = amount * 0.10
    return tax

def generate_report(total_units, failed_attempts):
    print("Total Deliveries Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)

# Main program
inventory = 0
failed_entries = 0

while True:
    stock = get_valid_input()

    if stock == "quit":
        generate_report(inventory, failed_entries)
        break

    tax = calculate_tax(stock)
    inventory = process_delivery(inventory, stock)

    print("Tax for this delivery:", tax)