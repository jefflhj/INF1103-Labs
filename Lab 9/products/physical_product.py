
from products.product import Product
from products.can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self):
        pass

    def display_information(self):
        super().display_information()
        print(f"Weight: {self._weight} kg")

    def get_fulfilment_info():
        pass

    def calculate_shipping_cost():
        pass
