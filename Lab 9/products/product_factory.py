"""
    additional_info: Any
    This is like a placeholder since different product type takes different additional information.
    Not sure how to implement this otherwise. Maybe before each product creation, call something from 
    IOManager to get the specific additional info from the user, eg. input("Weight: ") / input("Download Size: ")
    But wouldn't work for load_products() method in DataManager.
    
    Now that we have to use CSV instead of JSON, I have to add additional_info to the csv as well. Instead of each
    product having their custom attributes.

    Instead of additional_info, just put each specific attribute, and leave it empty in CSV.
"""

from suppliers.supplier import Supplier
from products.product import Product
from products.physical_product import PhysicalProduct
from products.digital_product import DigitalProduct


class ProductFactory:
    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float, stock_quantity: int, supplier: Supplier, weight: float = None, download_size: float = None) -> Product:
        if product_type == "physical":
            if weight is None:
                raise ValueError("Physical products require a weight.")
            return PhysicalProduct(product_type, product_id, name, price, stock_quantity, supplier, weight)
        elif product_type == "digital":
            if download_size is None:
                raise ValueError("Digital products require a download size.")
            return DigitalProduct(product_type, product_id, name, price, stock_quantity, supplier, download_size)
        else:
            raise ValueError(f"Unknown product type: {product_type}")
