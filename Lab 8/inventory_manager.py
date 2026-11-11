"""
    Inventory Manager

    Lab 8. Object oriented.
    Created Supplier class.
    Added type hints.
    Added remove_product for Inventory.
    Created Orders, OrderLine.
    LSP.
    Product: get_product_mass(): pass   PhysicalProduct: get_product_mass(): return self._weight   DigitalProduct: get_product_mass(): return self._size ?
"""

import os
import json
import pathlib
import re

from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier
from order import Order
from suppliers import Suppliers


def print_system_banner():
    print("\n========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("========================================\n")


def print_option_menu():
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Supplier")
    print("3. Add Product")
    print("4. Update Stock")
    print("5. Search Product")
    print("6. Save Inventory")
    print("7. Exit")
    print("----------------------------\n")


def get_option_menu_choice(): # returns chosen menu option as integer
    while True:
        chosen_option = input("Enter Option: ")

        if chosen_option not in ["1", "2", "3", "4", "5", "6", "7"]:
            print("\nPlease select an option from the menu.\n")
            continue
        else:
            return int(chosen_option)


def create_supplier(inventory):
    while True:
        supplier_id = input("Supplier ID: ")

        if re.match(r'^S\d{3}$', supplier_id):
            if inventory.search_supplier(supplier_id):
                print("Supplier ID already exists.")
                return # just return straight to main menu instead of prompting for new id. Saves trouble of implementing a word to exit the search loop.
            break
        else:
            print("Invalid Supplier ID format. Please use 'S' followed by 3 digits (e.g., S001).")

    name = input("Supplier Name: ")
    email = input("Contact Email: ") # could regex for valid email

    return Supplier(supplier_id, name, email)


def get_product_type():
    while True:
        product_type = input("Enter Product Type (Physical/Digital): ").strip().lower()

        if product_type in ["physical", "digital"]:
            return product_type
        else:
            print("Invalid product type. Please enter 'Physical' or 'Digital'.")


def get_product_weight():
    while True:
        try:
            weight = float(input("Weight (kg): "))
            if weight < 0:
                raise ValueError
            return weight
        except ValueError:
            print("Invalid weight. Please enter a positive number.")


def get_product_download_size():
    while True:
        try:
            download_size = float(input("Download Size (MB): "))
            if download_size < 0:
                raise ValueError
            return download_size
        except ValueError:
            print("Invalid download size. Please enter a positive number.")


def add_product(product_type, inventory): # returns None or PhysicalProduct object or DigitalProduct object
    while True:
        product_id = input("Product ID: ")

        if re.match(r'^P\d{3}$', product_id):
            if inventory.search_product(product_id):
                print("Product ID already exists.")
                return # just return straight to main menu instead of prompting for new id. Saves trouble of implementing a word to exit the search loop.
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

    while True:
        supplier_id = input("Supplier ID: ")

        if re.match(r'^S\d{3}$', supplier_id):
            if inventory.search_product(supplier_id):
                supplier = #inventory.get_supplier()
            break
        else:
            print("Invalid Supplier ID format. Please use 'S' followed by 3 digits (e.g., S001).")

    if product_type == "physical":
        weight = get_product_weight()
        inventory.add_product(PhysicalProduct(product_id, name, round(price, 2), stock, weight))

    elif product_type == "digital":
        download_size = get_product_download_size()
        inventory.add_product(DigitalProduct(product_id, name, round(price, 2), stock, download_size))

    print("Product added successfully!\n")


def update_stock(inventory):
    print("\nUpdate Stock")

    while True:
        product_id = input("Enter Product ID: ")

        product = inventory.search_product(product_id)

        if product:
            break
        else:
            print("\nProduct ID not found\n")
            return # just return straight to main menu instead of prompting for new id. Saves trouble of implementing a word to exit the search loop.

    print("\nProduct Found:")
    print(f"Name: {product.name}")
    print(f"Current Stock: {product.stock}\n")

    while True:
        try:
            new_stock_quantity = int(input("New Stock Quantity: "))
            if new_stock_quantity < 0:
                raise ValueError
            break
        except ValueError:
            print("\nInvalid stock quantity. Please enter a positive whole number.\n")

    product.update_stock(new_stock_quantity) # will also update the product object in inventory's dict __products

    print("\nStock updated successfully!\n")


def search_product(inventory):
    print("\nSearch Product")

    while True:
        product_id = input("Enter Product ID: ")

        product = inventory.search_product(product_id)

        if product:
            break
        else:
            print("\nProduct not found.\n")
            return # just return straight to main menu instead of prompting for new id. Saves trouble of implementing a word to exit the search loop.

    print("\nProduct Found")
    print("------------------------------------------------")
    product.display_information()
    print("------------------------------------------------\n")


def load_inventory(inventory_filepath, inventory):
    try:
        with open(inventory_filepath, "r", encoding="utf-8") as file:
            inventory_data = json.load(file)

        print(f"{pathlib.Path(inventory_filepath).name} found.")

        for product in inventory_data.values():
            if product["type"] == "physical":
                inventory.add_product(PhysicalProduct(product["product_id"], product["name"], product["price"], product["stock"], product["weight"]))

            elif product["type"] == "digital":
                inventory.add_product(DigitalProduct(product["product_id"], product["name"], product["price"], product["stock"], product["download_size"]))

    except FileNotFoundError:
        inventory_data = {}

        with open(inventory_filepath, "w", encoding="utf-8") as file:
            json.dump(inventory_data, file, indent=4)

        print(f"{pathlib.Path(inventory_filepath).name} not found. Created new inventory file.")

    print("Inventory loaded successfully.\n")


def load_suppliers(suppliers_filepath, suppliers):
    try:
        with open(suppliers_filepath, "r", encoding="utf-8") as file:
            suppliers_data = json.load(file)

        print(f"{pathlib.Path(suppliers_filepath).name} found.")

        for supplier in suppliers_data.values():
            suppliers.add_supplier(Supplier(supplier["supplier_id"], supplier["name"], supplier["contact_email"]))

    except FileNotFoundError:
        suppliers_data = {}

        with open(suppliers_filepath, "w", encoding="utf-8") as file:
            json.dump(suppliers_data, file, indent=4)

        print(f"{pathlib.Path(suppliers_filepath).name} not found. Created new suppliers file.")

    print("Suppliers loaded successfully.\n")


def save_inventory(inventory, inventory_filepath, manual_save=False):
    if manual_save:
        print("\nSaving inventory...")
    else:
        print("\nSaving inventory before exit...")

    try:
        with open(inventory_filepath, "w", encoding="utf-8") as file:
            json.dump(inventory.to_dict(), file, indent=4)

        if manual_save:
            print(f"Inventory saved successfully to {pathlib.Path(inventory_filepath).name}.\n")
        else:
            print(f"Inventory saved successfully.\n")

    except Exception as e:
        print(f"Error saving inventory: {e}\n")


def exit_program(inventory, inventory_filepath):
    save_inventory(inventory, inventory_filepath)

    print("Thank you for using Inventory Management System.")
    print("Program terminated.\n")


def main():
    inventory_filepath = os.getenv("INVENTORY_FILE", "./inventory.json")
    suppliers_filepath = os.getenv("SUPPLIERS_FILE", "./suppliers.json")

    print_system_banner()

    inventory = Inventory()
    suppliers = Suppliers()

    load_inventory(inventory_filepath, inventory)
    load_suppliers(suppliers_filepath, suppliers)

    print_option_menu()

    while True:
        match get_option_menu_choice():
            case 1: # Display All Products
                inventory.display_all()
                continue

            case 2: # Add Supplier
                pass

            case 3: # Add Product
                add_product(get_product_type(), inventory)
                continue

            case 4: # Update Stock
                update_stock(inventory)
                continue

            case 5: # Search Product
                search_product(inventory)
                continue

            case 6: # Save Inventory
                save_inventory(inventory, inventory_filepath, True)
                continue

            case 7: # Exit
                exit_program(inventory, inventory_filepath)
                return


if __name__ == "__main__":
    main()
