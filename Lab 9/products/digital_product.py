
from products.product import Product


class DigitalProduct(Product):
    def __init__(self):
        pass

    def display_information(self):
        super().display_information()
        print(f"Size: {self._size} MB")

    def get_fulfilment_info():
        pass

    