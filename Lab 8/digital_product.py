from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, download_size: float):
        super().__init__(product_id, name, price, stock, supplier, type="digital")
        self.__download_size = download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"Download Size: {self.__download_size} MB")

    def to_dict(self) -> dict:
        product_dict = super().to_dict()
        product_dict["download_size"] = self.__download_size
        return product_dict

    def get_fulfilment_info(self) -> str:
        return f"This product is delivered digitally. Download size: {self.__download_size} MB"

    @property
    def download_size(self):
        return self.__download_size
