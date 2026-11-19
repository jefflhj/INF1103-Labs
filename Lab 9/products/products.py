"""
    This is like inventory, it just stores all products.
    DataManager will read from and save to products.csv.
"""

from products.product import Product


class Products():
    def __init__(self):
        self._products = {}

    def add_product(product: Product) -> None:
        pass

    def remove_product():
        pass
    
    def search_product():
        pass

    def get_all_products(self) -> list[Product]:
        return list(self._products.values())
