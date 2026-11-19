import os
import subprocess


class IOManager:
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
        print()
        print("5. Display All Suppliers")
        print("6. Add Supplier")
        print("7. Search Supplier")
        print()
        print("8. Save Inventory")
        print("9. Exit")
        print("----------------------------\n")

    @staticmethod
    def get_option_menu_choice() -> int:
        while True:
            chosen_option = input("Enter Option: ")

            if chosen_option not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                IOManager.clear_terminal()
                IOManager.show_option_menu()
                print("Please select an option from the menu.\n")
                continue
            else:
                return int(chosen_option)

    @staticmethod
    def show_exit_message() -> None:
        print("Thank you for using Inventory Management System.")
        print("Program terminated.\n")
