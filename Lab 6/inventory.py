

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
                self.__products[product].display_information()
                print()

            print("\033[A\r------------------------------------------------\n")

    def to_dict(self):
        return {
            product_id: product.to_dict()
            for product_id, product in self.__products.items()
        }
