"""
    Inventory Manager

    Lab 7. Object oriented.
    Inheritance, Method Overriding, Abstract Classes, Interfaces using abstract base classes.

    "For example, each saved product should include a type identifier such as “physical” or “digital”."
    This sounds like only when saved should it include a type identifier.

    For the type identifier, if only implemented during save and load from json, it would require 
    something like if "weight" in product_dict: to determine if it is a PhysicalProduct or DigitalProduct.
    This means that if some new product type is added with weight but is not a PhysicalProduct, it would be 
    misidentified. Instead, storing a type attribute to the product would probably be better.
"""

import os
import json
import pathlib
import re
from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        pass


class Product(ABC):
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock
        self.__type = None

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
            "stock": self.__stock,
            "type": self.__type
        }

    @abstractmethod
    def get_fulfilment_info(self):
        pass

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


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = weight
        self.__type = "physical"

    def display_information(self):
        super().display_information()
        print(f"Weight: {self.__weight} kg")

    def to_dict(self):
        product_dict = super().to_dict()
        product_dict["weight"] = self.__weight
        return product_dict

    def get_fulfilment_info(self):
        return f"This product requires physical shipping. Shipping weight: {self.__weight} kg"

    def calculate_shipping_cost(self):
        base_cost = 1.99

        if self.__weight <= 2.00:
            return base_cost
        
        cost_per_kg = 1.00
        return base_cost + (cost_per_kg * self.__weight)

    @property
    def weight(self):
        return self.__weight


class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.__download_size = download_size
        self.__type = "digital"

    def display_information(self):
        super().display_information()
        print(f"Download Size: {self.__download_size} MB")

    def to_dict(self):
        product_dict = super().to_dict()
        product_dict["download_size"] = self.__download_size
        return product_dict

    def get_fulfilment_info(self):
        return f"This product is delivered digitally. Download size: {self.__download_size} MB"

    @property
    def download_size(self):
        return self.__download_size


class Inventory:
    def __init__(self):
        self.__products = {}

    def add_product(self, product): # adds product to dict or prints exists message
        if product.product_id in self.__products:
            print(f"{product.product_id} - {product.name} already exists in the Inventory, it will not be added.") # create_product checks this already but just in case.

        else:
            self.__products[product.product_id] = product

    def search_product(self, product_id): # Returns product_id or None
        if product_id in self.__products:
            return self.__products[product_id]

        else:
            return None

    def display_all(self): # prints all products
        if not self.__products:
            print("The Inventory is empty.")

        else:
            print("\nCurrent Inventory")
            print("------------------------------------------------")

            for product in self.__products:
                self.__products[product].display_information()
                print()

            print("\033[A\r------------------------------------------------\n")

    def to_dict(self): # returns dict of dicts of products
        return {
            product_id: product.to_dict()
            for product_id, product in self.__products.items()
        }


def print_system_banner():
    print("\n========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("========================================\n")


def print_option_menu():
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------\n")


def get_option_menu_choice(): # returns chosen menu option as integer
    while True:
        chosen_option = input("Enter Option: ")

        if chosen_option not in ["1", "2", "3", "4", "5", "6"]:
            print("\nPlease select an option from the menu.\n")
            continue
        else:
            return int(chosen_option)


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
                add_product(get_product_type(), inventory)
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
