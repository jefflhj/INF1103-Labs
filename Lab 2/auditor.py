# Requirement 1: Initialize the inventory to zero in the start
inventory = 0
rejected_count = 0

# Requirement 2: Run in a continuous loop asking user to enter a stock quantity, until the user types "quit".
while True:
    stock_input = input("Enter a stock quantity (type 'quit' to exit): ")

    if stock_input.lower() == "quit":
        # Requirement 8: Reporting.
        print(f"\nTotal Units Processed: {inventory}")
        print(f"Failed / Rejected Entries: {rejected_count}\n")
        print("Exiting...")
        break

    # Requirement 4 & 5: Handle invalid inputs and reject negative numbers.
    if not stock_input.isdigit():
        print("\nPlease enter a valid number.\n")
        rejected_count += 1
        continue

    # Requirement 3: Accept stock values as integers.
    stock_input = int(stock_input)

    # Requirement 6: Manage state.
    inventory += stock_input
    print(f"\n[+] {stock_input}")
    print(f"Current Inventory: {inventory}\n")

    # Requirement 7: Trigger overstock alert.
    if inventory > 500:
        print(f"\n[Alert!] Total inventory exceeded 500 by {inventory - 500}. Exiting...")
        break
