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

   Lab 5. Changed to inventory manager. Create add_product(), update_stock(), search_product(), display_all().
   Change from text file to json file. Create save_inventory().
   Maintain menu system.

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
import json
import pathlib
import re


def get_database(database_filepath):
    try:
        with open(database_filepath, "r") as file:
            raw_database = file.read()

    except FileNotFoundError:
        with open(database_filepath, "w") as file:
            raw_database = repr({"inventory": 0, "rejected_entries": 0, "delivery_expenditure": 0.00, "tax_expenditure": 0.00, "delivery_history":[]})
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
        delivery_item_count = input("\n\nEnter the number of items in this delivery (type 'quit' to exit): ")
        
        if delivery_item_count.lower() == "quit":
            return "quit", rejected_entries_count

        try:
            delivery_item_count = int(delivery_item_count)

            if delivery_item_count < 0:
                raise ValueError
            
            return delivery_item_count, rejected_entries_count
        
        except ValueError:
            print("\nPlease enter a valid number. (Integer)")
            rejected_entries_count += 1
            continue


def get_delivery_cost():
    while True:
        delivery_cost = input("\nEnter the delivery cost: ")

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
    print(f"\nTotal Items Processed: {database['inventory']}")
    print(f"Rejected User Entries: {database['rejected_entries']}\n")
    print(f"Total Delivery Expenditure: ${database['delivery_expenditure']}")
    print(f"Total Delivery Tax Expenditure: ${database['tax_expenditure']}\n")

    print("Delivery History Records:")
    for rec in database["delivery_history"]:
        print(*rec)    


def check_overstock(database, delivery_item_count):
    if (database["inventory"] + delivery_item_count) > 500:
        print(f"\n[Alert!] Total inventory exceeded 500, this delivery will not be saved.")
        return False
    return True


def enter_new_delivery(database):
    item_number = 0
    delivery_record = []
    total_quantity = 0

    while True:
        print("Current Orders:\n")
        for rec in delivery_record:
            print(*rec)

        item_number += 1
        delivery_item_id = ((1+len(database["delivery_history"]))*1000)+(item_number)
        item_name = input("\n\nEnter Product Name: ")

        while True:
            item_quantity = input("Enter Quantity: ")
            try:
                item_quantity = int(item_quantity)

                if item_quantity < 0:
                    raise ValueError

                break

            except ValueError:
                print("\nPlease enter a valid number. (Positive Integer)\n")
                continue

        print("\nNew Delivery Item Recorded:")
        print(f"{delivery_item_id}, {item_name}, {item_quantity}")

        delivery_record.append((delivery_item_id, item_name, item_quantity))
        total_quantity += item_quantity

        while True:
            add_another_item = input("\n\nAdd another item? ('yes' / 'no'): ").lower()
            if add_another_item == "no":
                delivery_cost = get_delivery_cost()
                delivery_tax = calculate_delivery_tax(delivery_cost)

                if check_overstock(database, total_quantity):
                    update_local_database(database, total_quantity, 0, delivery_cost, delivery_tax, delivery_record)
                return

            elif add_another_item == "yes":
                break

            else:
                print("\nPlease enter either 'yes' or 'no'.")
                continue


def main():
    # database_filepath = os.getenv("DATABASE_FILE", "/app/database/inventory.json")
    database_filepath = "./inventory.json"
    database = get_database(database_filepath)
    
    while True:
        chosen_option = print_option_menu()

        if chosen_option == "4":
            save_to_database(database_filepath, database)
            print(f"\nDeliveries successfully saved to {os.path.basename(database_filepath)}")
            print_summary_report(database)
            return

        elif chosen_option == "3":
            print_summary_report(database)
        
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









# Lab 5 from here on

def print_system_banner():
    print("\n========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("========================================\n")


def get_inventory(inventory_filepath):
    try:
        with open(inventory_filepath, "r", encoding="utf-8") as file:
            inventory_data = json.load(file)

        print(f"{pathlib.Path(inventory_filepath).name} found.")

    except FileNotFoundError:
        inventory_data = {}

        with open(inventory_filepath, "w", encoding="utf-8") as file:
            json.dump(inventory_data, file, indent=4)

        print(f"{pathlib.Path(inventory_filepath).name} not found. Created new inventory file.")

    print("Inventory loaded successfully.")

    return inventory_data


def print_option_menu():
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------\n")


def get_option_menu_choice():
    while True:
        chosen_option = input("Enter Option: ")

        if chosen_option not in ["1", "2", "3", "4", "5", "6"]:
            print("\nPlease select an option from the menu.\n")
            continue
        else:
            return int(chosen_option)


def display_all(inventory):
    if not inventory:
        print("\nNo products found in the inventory.\n")
        return

    print("\nCurrent Inventory")
    print("------------------------------------------------")

    for product_id, product_info in inventory.items():
        print(f"ID: {product_id} | Name: {product_info['name']} | Price: ${product_info['price']:.2f} | Stock: {product_info['stock']}")

    print("------------------------------------------------\n")


def add_product(inventory):
    print("\nAdd New Product")

    while True:
        product_id = input("Product ID: ")

        if re.match(r'^P\d{3}$', product_id):
            if product_id in inventory:
                print("Product ID already exists.")
                continue
            break
        else:
            print("Invalid Product ID format. Please use 'P' followed by 3 digits (e.g., P001).")

    name = input("Product Name: ")

    while True:
        try:
            price = float(input("Price: "))
            if price < 0:
                raise ValueError
            break
        except ValueError:
            print("Invalid price. Please enter a positive number.")

    while True:
        try:
            stock = int(input("Stock Quantity: "))
            if stock < 0:
                raise ValueError
            break
        except ValueError:
            print("Invalid stock quantity. Please enter a positive whole number.")

    inventory[product_id] = {
        "product_id": product_id,
        "name": name,
        "price": price,
        "stock": stock
    }

    print("Product added successfully!\n")


def main():
    print_system_banner()

    inventory = get_inventory("./inventory.json")

    print_option_menu()

    while True:
        match get_option_menu_choice():
            case 1: # Display All Products
                display_all(inventory)
                continue

            case 2: # Add Product
                add_product(inventory)
                continue

            case 3: # Update Stock
                pass

            case 4: # Search Product
                pass

            case 5: # Save Inventory
                pass

            case 6: # Exit
                print("Exiting...")
                return















if __name__ == "__main__":
    main()
