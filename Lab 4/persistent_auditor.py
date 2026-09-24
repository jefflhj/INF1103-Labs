"""
   Smart Inventory Auditor

   A store manager orders items from vendors to fill their inventory stock to ensure they have sufficient items to sell.
   The system is used to enter the number of items in a delivery and the cost of the delivery. The system will then 
   calculate the tax on the delivery cost automatically. The system will also automatically keep track of the total 
   number of failed entries made by the user excluding delivery cost entries. These pieces of information will be saved and 
   stored in a text file.

   Variables:
        inventory:              The current total number of items in the store's physical inventory.
        rejected_entries:       The total number of rejected entries made by the user.
        delivery_expenditure:   The running total cost of all deliveries made to the store.
        tax_expenditure:        The running total tax cost of all deliveries made to the store.
        delivery_history:       A list of lists for every delivery made to the store and their details.
        inventory_filepath:     The file path to the inventory database text file .
"""

import os
import ast


def exit():
    pass


def get_inventory(inventory_filepath):
    try:
        with open(inventory_filepath, "r") as file:
            raw_inventory = file.read()

    except FileNotFoundError:
        with open(inventory_filepath, "w") as file:
            raw_inventory = repr({})
            file.write(raw_inventory)

    inventory = ast.literal_eval(raw_inventory)
    return inventory


def save_inventory(inventory_filepath, inventory):
    try:
        with open(inventory_filepath, "w") as file:
            file.write(repr(inventory))
    except Exception as e:
        print(f"Error saving inventory: {e}")


def update_delivery_history(inventory, delivery_item_count, rejected_entries_count, delivery_cost, delivery_tax):
    inventory["inventory"] = inventory.get("inventory", 0) + delivery_item_count
    inventory["rejected_entries"] = inventory.get("rejected_entries", 0) + rejected_entries_count
    inventory["delivery_expenditure"] = inventory.get("delivery_expenditure", 0) + delivery_cost
    inventory["tax_expenditure"] = inventory.get("tax_expenditure", 0) + delivery_tax


def get_delivery_item_count():
    rejected_entries_count = 0

    while True:
        delivery_item_count = input("Enter the number of items in this delivery (type 'quit' to exit): ")
        
        if delivery_item_count.lower() == "quit":
            return "quit", rejected_entries_count

        try:
            return int(delivery_item_count), rejected_entries_count
        
        except ValueError:
            print("\nPlease enter a valid number.\n")
            rejected_entries_count += 1
            continue


def get_delivery_cost():
    while True:
        delivery_cost = input("Enter the delivery cost: ")

        try:
            return float(delivery_cost)
        
        except ValueError:
            print("\nPlease enter a valid monetary value. (Will be rounded to 2 decimal places)\n")
            continue


def calculate_delivery_tax(delivery_cost):
    tax_rate = 0.1

    return round(delivery_cost * tax_rate, 2)


def main():
    inventory_filepath = os.getenv("INVENTORY_FILE", "/auditor/database/inventory.txt")

    inventory = get_inventory(inventory_filepath)

    delivery_item_count, rejected_entries_count = get_delivery_item_count()

    if delivery_item_count == "quit":
        update_delivery_history(inventory, 0, rejected_entries_count, 0, 0)
        save_inventory(inventory_filepath, inventory)
        exit()

    delivery_cost = get_delivery_cost()
    delivery_tax = calculate_delivery_tax(delivery_cost)
    
    update_delivery_history(inventory, delivery_item_count, rejected_entries_count, delivery_cost, delivery_tax)




