"""
    additional_info: Any
    This is like a placeholder since different product type takes different additional information.
    Not sure how to implement this otherwise. Maybe before each product creation, call something from 
    IOManager to get the specific additional info from the user, eg. input("Weight: ") / input("Download Size: ")
    But wouldn't work for load_products() method in DataManager.
"""

from typing import Any

from suppliers.supplier import Supplier
from products.product import Product
from products.physical_product import PhysicalProduct
from products.digital_product import DigitalProduct


class ProductFactory:
    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float, stock_quantity: int, supplier: Supplier, additional_info: Any) -> Product:
        if product_type == "physical":
            return PhysicalProduct(product_type, product_id, name, price, stock_quantity, supplier, additional_info)
        elif product_type == "digital":
            return DigitalProduct(product_type, product_id, name, price, stock_quantity, supplier, additional_info)
        else:
            raise ValueError(f"Unknown product type: {product_type}")
