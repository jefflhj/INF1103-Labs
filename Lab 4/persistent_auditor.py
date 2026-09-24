"""
   Smart Inventory Auditor

   A store manager orders items from vendors to fill their inventory stock to ensure they have sufficient items to sell.
   The system is used to enter the number of items in a delivery and the cost of the delivery. The system will then 
   calculate the tax on the delivery cost automatically. The system will also automatically keep track of the total 
   number of failed entries made by the user. These information will be saved and stored in a text file.

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


def exit(inventory):
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


def get_user_input():
    pass


def main():
    inventory_filepath = os.getenv("INVENTORY_FILE", "/auditor/database/inventory.txt")






