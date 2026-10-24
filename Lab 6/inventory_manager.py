"""
    Inventory Manager

    Lab 6. Object oriented.
    Inventory items as objects.
"""

import os
import json
import pathlib
import re


class Product:
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    def update_stock(self, quantity):
        if quantity >= 0 and isinstance(quantity, int): # not really needed here since input validation alr done in the update_stock function
            self.__stock = quantity
            return True

        else:
            return False

    def display_information(self):
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.price:.2f}")
        print(f"Stock: {self.stock}")

    def to_dict(self):
        return {
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock
        }

    @property
    def product_id(self):
        return self.__product_id # These are immutable so they cant be edited outide the class even if exposed like this. Example if return a dict, then they would be editable outside.

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def stock(self):
        return self.__stock


class Inventory:
    def __init__(self):
        self.__products = {}

    def add_product(self, product):
        if product.product_id in self.__products:
            print(f"{product.product_id} - {product.name} already exists in the Inventory, it will not be added.")

        else:
            self.__products[product.product_id] = product

    def search_product(self, product_id):
        if product_id in self.__products:
            return self.__products[product_id]
            # self.__products[product_id].display_information()

        else:
            return None
            # print(f"The product id '{product_id}' was not found in the Inventory.")

    def display_all(self):
        if not self.__products:
            print("The Inventory is empty.")

        else:
            print("\nCurrent Inventory")
            print("------------------------------------------------")

            for product in self.__products:
                product.display_information()
                print()

            print("\044[A/r------------------------------------------------\n")

    def to_dict(self):
        return {
            product_id: product.to_dict()
            for product_id, product in self.__products.items()
        }


def print_system_banner():
    print("\n========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("========================================\n")


def load_inventory(inventory_filepath, inventory):
    try:
        with open(inventory_filepath, "r", encoding="utf-8") as file:
            inventory_data = json.load(file)

        print(f"{pathlib.Path(inventory_filepath).name} found.")

        for product in inventory_data.values():
            inventory.add_product(Product(product["product_id"], product["name"], product["price"], product["stock"]))

    except FileNotFoundError:
        inventory_data = {}

        with open(inventory_filepath, "w", encoding="utf-8") as file:
            json.dump(inventory_data, file, indent=4)

        print(f"{pathlib.Path(inventory_filepath).name} not found. Created new inventory file.")

    print("Inventory loaded successfully.\n")


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

    inventory.add_product(Product(product_id, name, round(price, 2), stock))

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

    print_system_banner()

    inventory = Inventory()

    load_inventory(inventory_filepath, inventory)

    print_option_menu()

    while True:
        match get_option_menu_choice():
            case 1: # Display All Products
                inventory.display_all()
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


