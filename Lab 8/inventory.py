from product import Product


class Inventory:
    def __init__(self):
        self.__products: dict[str, Product] = {}

    def add_product(self, product: Product): # adds product to dict or prints exists message
        if product.product_id in self.__products:
            print(f"{product.product_id} - {product.name} already exists in the Inventory, it will not be added.") # create_product checks this already but just in case.

        else:
            self.__products[product.product_id] = product

    def remove_product(self, product: Product):
        if product.product_id in self.__products:
            del self.__products[product.product_id]

        else:
            print(f"{product.product_id} - {product.name} does not exists in the Inventory, nothing happened.")

    def search_product(self, product_id: str) -> Product | None: # Returns product object or None
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

    def to_dict(self) -> dict[str, dict]: # returns dict of dicts of products
        return {
            product_id: product.to_dict()
            for product_id, product in self.__products.items()
        }

