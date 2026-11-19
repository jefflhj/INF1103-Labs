"""
    This is like inventory, it just stores all products.
    DataManager will read from and save to products.csv.
"""

from products.product import Product


class Products():
    def __init__(self):
        self._products = {}

    def add_product(self, product: Product) -> str:
        if product.product_id in self._products:
            return "Product already exists."
        else:
            self._products[product.product_id] = product
            return "Product added successfully."

    def remove_product(self, product: Product) -> str:
        if product.product_id not in self._products:
            return "Product does not exist."
        else:
            del self._products[product.product_id]
            return "Product removed successfully."
    
    def search_product(self, product_id: str) -> Product | None:
        if product_id not in self._products:
            return None
        else:
            return self._products[product_id]

    def get_all_products(self) -> list[Product]:
        return list(self._products.values())
