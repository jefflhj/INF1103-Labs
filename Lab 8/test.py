from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


def show_info_fulfilment(inventory: Inventory, product1: PhysicalProduct, product2: DigitalProduct) -> None:
    inventory.add_product(product1)
    inventory.add_product(product2)

    inventory.search_product(product1.product_id).display_information()
    print(inventory.search_product(product1.product_id).get_fulfilment_info())
    print()
    inventory.search_product(product2.product_id).display_information()
    print(inventory.search_product(product2.product_id).get_fulfilment_info())
