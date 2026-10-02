"""
    Inventory Manager

    Lab 5. Changed to inventory manager. Create add_product(), update_stock(), search_product(), display_all().
    Change from text file to json file. Create save_inventory().
    Maintain menu system.
"""

import json
import pathlib
import re


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
        print(f"ID: {product_id} | Name: {product_info['name']} | Price: ${product_info['price']} | Stock: {product_info['stock']}")

    print("------------------------------------------------\n")


def add_product(inventory):
    print("\nAdd New Product")

    while True:
        product_id = input("Product ID: ")

        if re.match(r'^P\d{3}$', product_id):
            if product_id in inventory:
                print("Product ID already exists.")
                return # just return straight to main menu instead of prompting for new id. Saves trouble of implementing a word to exit the input loop.
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
        "price": round(price, 2),
        "stock": stock
    }

    print("Product added successfully!\n")


def update_stock(inventory):
    print("\nUpdate Stock")

    while True:
        product_id = input("Enter Product ID: ")

        if product_id in inventory:
            break
        else:
            print("\nProduct ID not found\n")
            return # just return straight to main menu instead of prompting for new id. Saves trouble of implementing a word to exit the search loop.

    print("\nProduct Found:")
    print(f"Name: {inventory[product_id]['name']}")
    print(f"Current Stock: {inventory[product_id]['stock']}\n")

    while True:
        try:
            new_stock_quantity = int(input("New Stock Quantity: "))
            if new_stock_quantity < 0:
                raise ValueError
            break
        except ValueError:
            print("\nInvalid stock quantity. Please enter a positive whole number.\n")

    inventory[product_id]['stock'] = new_stock_quantity

    print("\nStock updated successfully!\n")


def search_product(inventory):
    print("\nSearch Product")

    while True:
        product_id = input("Enter Product ID: ")

        if product_id in inventory:
            break
        else:
            print("\nProduct not found.\n")
            return # just return straight to main menu instead of prompting for new id. Saves trouble of implementing a word to exit the search loop.

    print("\nProduct Found")
    print("------------------------------------------------")
    print(f"ID: {product_id}")
    print(f"Name: {inventory[product_id]['name']}")
    print(f"Price: ${inventory[product_id]['price']}")
    print(f"Stock: {inventory[product_id]['stock']}")
    print("------------------------------------------------\n")


def save_inventory(inventory, inventory_filepath, manual_save=False):
    if manual_save:
        print("\nSaving inventory...")
    else:
        print("\nSaving inventory before exit...")

    try:
        with open(inventory_filepath, "w", encoding="utf-8") as file:
            json.dump(inventory, file, indent=4)

        if manual_save:
            print(f"Inventory saved successfully to {pathlib.Path(inventory_filepath).name}.\n")
        else:
            print(f"Inventory saved successfully.\n")

    except Exception as e:
        print(f"Error saving inventory: {e}\n")


def exit_program(inventory, inventory_filepath):
    save_inventory(inventory, inventory_filepath)

    print("\nThank you for using Inventory Management System.")
    print("Program terminated.\n")


def main():
    inventory_filepath = "./inventory.json"

    print_system_banner()

    inventory = get_inventory(inventory_filepath)

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
                update_stock(inventory)
                continue

            case 4: # Search Product
                search_product(inventory)
                continue

            case 5: # Save Inventory
                save_inventory(inventory, inventory_filepath, True)
                continue

            case 6: # Exit
                exit_program(inventory, inventory_filepath)
                return


if __name__ == "__main__":
    main()
