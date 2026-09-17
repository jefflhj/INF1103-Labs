
# Additional: Ask for the delivery cost.
def get_delivery_cost():
    while True:
        cost_input = input("Enter the delivery cost: ")
        try:
            return float(cost_input)
        except ValueError:
            print("\nPlease enter a valid number.\n")
            continue

# Requirement 2: Run in a continuous loop asking user to enter a stock quantity, until the user types "quit".
def get_valid_input():
    rejects = 0
    while True:
        stock_input = input("Enter a stock quantity (type 'quit' to exit): ")
        
        if stock_input.lower() == "quit":
            return "quit", None

        try:
            return int(stock_input), rejects
        except ValueError:
            print("\nPlease enter a valid number.\n")
            rejects += 1
            continue

# Requirement 3: Update any counters and records you are tracking.
def process_delivery(current_total, new_value):
    current_total += new_value
    return current_total

# Requirement 3: Calculate the tax for that delivery.
def calculate_tax(amount):
    tax_rate = 0.1
    return amount * tax_rate

# Requirement 4: Reporting.
def generate_report(total_units, failed_attempts):
    print(f"\nTotal Units Processed: {total_units}")
    print(f"Failed / Rejected Entries: {failed_attempts}\n")
    # print(f"Total Delivery Cost: {total_delivery_cost}")
    # print(f"Total Delivery Tax: {total_delivery_tax}\n")

# Main function to run the program
def main():
    # Requirement 1: Initialize the inventory to zero in the start
    inventory = 0
    total_rejects = 0
    total_delivery_cost = 0
    total_delivery_tax = 0

    while True:
        # Requirement 4: Reporting.
        if (user_input:= get_valid_input())[0] == "quit":
            return generate_report(inventory, total_rejects)

        # get delivery cost from user input
        delivery_cost = get_delivery_cost()
        # calculate tax
        tax = calculate_tax(delivery_cost)
        print(f"\nDelivery Cost: {delivery_cost}")
        print(f"Tax: {tax}")

        # Requirement 3: Add the delivery amount to the running total.
        total_delivery_cost += delivery_cost
        total_delivery_tax += tax

        # add failed attempts to total
        total_rejects += user_input[1]
        # add new stock quantity delivered to inventory
        inventory = process_delivery(inventory, user_input[0])
        print(f"\n[+] {user_input[0]}")
        print(f"Current Inventory: {inventory}\n")

        if inventory > 500:
            print(f"\n[Alert!] Total inventory exceeded 500 by {inventory - 500}. Exiting...")
            break


if __name__ == "__main__":
    main()
