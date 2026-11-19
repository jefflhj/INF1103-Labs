from products.product import Product
from suppliers.supplier import Supplier


class DigitalProduct(Product):
    def __init__(self, product_type: str, product_id: str, name: str, price: float, stock: int, supplier: Supplier, download_size: float):
        super().__init__(product_type=product_type, product_id=product_id, name=name, price=price, stock=stock, supplier=supplier)
        self._download_size = download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"Download Size: {self._download_size} MB")

    def get_fulfilment_info(self) -> str:
        return f"This product is delivered digitally. Download size: {self._download_size} MB"

    @property
    def download_size(self):
        return self._download_size
