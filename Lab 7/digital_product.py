
from product import Product


class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock, type="digital")
        self.__download_size = download_size

    def display_information(self):
        super().display_information()
        print(f"Download Size: {self.__download_size} MB")

    def to_dict(self):
        product_dict = super().to_dict()
        product_dict["download_size"] = self.__download_size
        return product_dict

    def get_fulfilment_info(self):
        return f"This product is delivered digitally. Download size: {self.__download_size} MB"

    @property
    def download_size(self):
        return self.__download_size

