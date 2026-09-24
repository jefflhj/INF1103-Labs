"""
   Smart Inventory Auditor

   A store manager orders items from vendors to fill their inventory stock to ensure they have sufficient items to sell.
   The system is used to enter the number of items in a delivery and the cost of the delivery. The system will then 
   calculate the tax on the delivery cost automatically. The system will also automatically keep track of the total 
   number of failed entries made by the user excluding delivery cost entries. These pieces of information will be saved and 
   stored in a database text file.

   Lab 4 now allows the user to specify the items in the delivery. Delivery Item ID, Item Name, Quantity.
   The idea here is that the store orders items from a vendor and records these items for stock taking. This system is used 
   to keep track of incoming items, not to place an order for new items.
   This option will not track rejected entries. Possible with a database of valid item names. Only this option will store 
   a record of the delivery history.
   Note that Delivery = Order and Item = Product.

   Stored Variables:
        inventory:              The current total number of items in the store's physical inventory.
        rejected_entries:       The total number of rejected entries made by the user.
        delivery_expenditure:   The running total cost of all deliveries made to the store.
        tax_expenditure:        The running total tax cost of all deliveries made to the store.
        delivery_history:       A list of lists for every delivery made to the store and their details. #### not done yet
        delivery_item_id:       Unique ID for the item in the current delivery.
        item_name:              Item's name.
        item_quantity:          How many of that item.
"""

import os
import ast


def get_database(database_filepath):
    try:
        with open(database_filepath, "r") as file:
            raw_database = file.read()

    except FileNotFoundError:
        with open(database_filepath, "w") as file:
            raw_database = repr({})
            file.write(raw_database)

    database = ast.literal_eval(raw_database)
    return database


def save_to_database(database_filepath, database):
    try:
        with open(database_filepath, "w") as file:
            file.write(repr(database))
    except Exception as e:
        print(f"Error saving inventory: {e}")


def get_delivery_item_count():
    rejected_entries_count = 0

    while True:
        delivery_item_count = input("Enter the number of items in this delivery (type 'quit' to exit): ")
        
        if delivery_item_count.lower() == "quit":
            return "quit", rejected_entries_count

        try:
            delivery_item_count = int(delivery_item_count)

            if delivery_item_count < 0:
                raise ValueError
            
            return delivery_item_count, rejected_entries_count
        
        except ValueError:
            print("\nPlease enter a valid number. (Integer)\n")
            rejected_entries_count += 1
            continue


def get_delivery_cost():
    while True:
        delivery_cost = input("Enter the delivery cost: ")

        try:
            delivery_cost = float(delivery_cost)

            if delivery_cost < 0:
                raise ValueError
            
            return delivery_cost
        
        except ValueError:
            print("\nPlease enter a valid monetary value. (Will be rounded to 2 decimal places)\n")
            continue


def calculate_delivery_tax(delivery_cost):
    tax_rate = 0.1

    return round(delivery_cost * tax_rate, 2)


def update_local_database(database, delivery_item_count, rejected_entries_count, delivery_cost, delivery_tax, delivery_record):
    database["inventory"] = database.get("inventory", 0) + delivery_item_count
    database["rejected_entries"] = database.get("rejected_entries", 0) + rejected_entries_count
    database["delivery_expenditure"] = database.get("delivery_expenditure", 0) + delivery_cost
    database["tax_expenditure"] = database.get("tax_expenditure", 0) + delivery_tax
    if delivery_record is None:
        return
    database["delivery_history"].append(delivery_record)


def print_summary_report(database):
    print(f"\nTotal Items Processed: {database["inventory"]}")
    print(f"Rejected User Entries: {database["rejected_entries"]}\n")
    print(f"Total Delivery Expenditure: ${database["delivery_expenditure"]}")
    print(f"Total Delivery Tax Expenditure: ${database["tax_expenditure"]}\n")


def check_overstock(database, delivery_item_count):
    if (database["inventory"] + delivery_item_count) > 500:
        print(f"\n[Alert!] Total inventory exceeded 500, this delivery will not be saved.")
        return False
    return True


def print_option_menu():
    print("========= Choose An Option =========")
    print("1) Enter New Delivery Quantity Only")
    print("2) Enter New Delivery With Item Names")
    print("3) Save & Quit")

    while True:
        chosen_option = input(">>> ")

        if chosen_option != "1" or chosen_option != "2" or chosen_option != "3":
            print("Please select either '1', '2' or '3'.")
            continue
        else:
            return chosen_option


def enter_new_delivery(database):
    item_number = 0
    delivery_record = []
    total_quantity = 0

    while True:
        item_number += 1
        delivery_item_id = (len(database["delivery_history"])*1000)+(item_number)
        item_name = input("Enter Product Name: ")
        item_quantity = input("Enter Quantity: ")

        print("\nNew Delivery Item Recorded:")
        print(f"{delivery_item_id},{item_name},{item_quantity}")

        delivery_record.append((delivery_item_id, item_name, item_quantity))
        total_quantity += item_quantity

        if input("Add another item? ('yes' / 'no')").lower() == "no":
            delivery_cost = get_delivery_cost()
            delivery_tax = calculate_delivery_tax(delivery_cost)

            if check_overstock(database, total_quantity):
                update_local_database(database, total_quantity, 0, delivery_cost, delivery_tax, delivery_record)
                return


def main():
    database_filepath = os.getenv("DATABASE_FILE", "/auditor/database/database.txt")
    database = get_database(database_filepath)
    
    while True:
        chosen_option = print_option_menu()

        if chosen_option == "3":
            save_to_database(database_filepath, database)
            print_summary_report(database)
            return
        
        elif chosen_option == "2":
            enter_new_delivery(database)

        elif chosen_option == "1":
            delivery_item_count, rejected_entries_count = get_delivery_item_count()

            if delivery_item_count == "quit":
                update_local_database(database, 0, rejected_entries_count, 0, 0, None)
                continue

            delivery_cost = get_delivery_cost()
            delivery_tax = calculate_delivery_tax(delivery_cost)

            if check_overstock(database, delivery_item_count):
                update_local_database(database, delivery_item_count, rejected_entries_count, delivery_cost, delivery_tax, None)
                continue


if __name__ == "__main__":
    main()
