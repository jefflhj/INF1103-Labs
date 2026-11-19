"""
    All user input and output (console) occurs here.
    AppEngine decides WHAT to ask and show, IOManager decides HOW.
"""

import math
import os
import subprocess

MENU_OPTION_COUNT = 10


class IOManager:
    # ===== Display =====
    @staticmethod
    def print_system_banner() -> None:
        print("\n========================================")
        print("INVENTORY MANAGEMENT SYSTEM")
        print("========================================\n")

    @staticmethod
    def clear_terminal() -> None:
        command = "cls" if os.name == "nt" else "clear"
        subprocess.run(command, shell=True)

    @staticmethod
    def show_option_menu() -> None:
        print("----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Search Product")
        print("4. Update Product Stock")
        print("5. Place Supplier Order")
        print()
        print("6. Display All Suppliers")
        print("7. Add Supplier")
        print("8. Search Supplier")
        print()
        print("9. Save Inventory")
        print("10. Exit")
        print("----------------------------\n")

    @staticmethod
    def show_message(message: str = "") -> None:
        print(message)

    @staticmethod
    def show_messages(messages: list[str]) -> None:
        for message in messages:
            print(message)

    @staticmethod
    def show_heading(title: str) -> None:
        print(f"\n{title}")
        print("-" * len(title))

    @staticmethod
    def show_separator() -> None:
        print("\n========================================\n")

    @staticmethod
    def show_exit_message() -> None:
        print("Thank you for using Inventory Management System.")
        print("Program terminated.\n")

    @staticmethod
    def pause() -> None:
        input("\nPress Enter to return to the menu...")

    # ===== Input =====
    @staticmethod
    def get_option_menu_choice() -> int:
        valid_options = [str(number) for number in range(1, MENU_OPTION_COUNT + 1)]
        while True:
            chosen_option = input("Enter Option: ").strip()

            if chosen_option not in valid_options:
                IOManager.clear_terminal()
                IOManager.show_option_menu()
                print("Please select an option from the menu.\n")
                continue
            else:
                return int(chosen_option)

    @staticmethod
    def get_choice(title: str, options: list[str]) -> int:
        """Shows a numbered list and returns the chosen position (1-based)."""
        print(f"\n{title}")
        for number, option in enumerate(options, start=1):
            print(f"{number}. {option}")
        while True:
            chosen = input("Enter choice: ").strip()
            if chosen.isdigit() and 1 <= int(chosen) <= len(options):
                return int(chosen)
            print(f"Please enter a number between 1 and {len(options)}.")

    @staticmethod
    def get_non_empty_string(prompt: str) -> str:
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("This field cannot be empty.")

    @staticmethod
    def get_email(prompt: str) -> str:
        while True:
            value = input(prompt).strip()
            local, _, domain = value.partition("@")
            if local and "." in domain and " " not in value:
                return value
            print("Please enter a valid email address, e.g. name@example.com")

    @staticmethod
    def get_positive_float(prompt: str, maximum: float = None) -> float:
        while True:
            try:
                value = float(input(prompt))
                if not math.isfinite(value) or value <= 0:
                    print("Please enter a number greater than zero.")
                    continue
                if maximum is not None and value > maximum:
                    print(f"Please enter a number no greater than {maximum}.")
                    continue
                return value
            except ValueError:
                print("Please enter a valid number, e.g. 12.5")

    @staticmethod
    def get_positive_int(prompt: str) -> int:
        while True:
            try:
                value = int(input(prompt))
                if value <= 0:
                    print("Please enter a whole number greater than zero.")
                    continue
                return value
            except ValueError:
                print("Please enter a valid whole number, e.g. 5")

    @staticmethod
    def get_non_negative_int(prompt: str) -> int:
        while True:
            try:
                value = int(input(prompt))
                if value < 0:
                    print("Please enter a whole number of zero or more.")
                    continue
                return value
            except ValueError:
                print("Please enter a valid whole number, e.g. 5")

    @staticmethod
    def get_yes_no(prompt: str) -> bool:
        while True:
            answer = input(prompt).strip().lower()
            if answer in ("y", "yes"):
                return True
            if answer in ("n", "no"):
                return False
            print("Please enter y or n.")
