# Requirement 1: Initialize the inventory to zero in the start
inventory = 0

# Requirement 2: Run in a continuous loop asking user to enter a stock quantity, until the user types "quit".
while True:
    stock_input = input("Enter a stock quantity (type 'quit' to exit): ")

    if stock_input.lower() == "quit":
        print("Exiting...")
        break

    # Requirement 4 & 5: Handle invalid inputs and reject negative numbers.
    if not stock_input.isdigit():
        print("\nPlease enter a valid number.\n")
        continue

    # Requirement 3: Accept stock values as integers.
    stock_input = int(stock_input)