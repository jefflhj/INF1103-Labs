from products.product import Product
from suppliers.supplier import Supplier


class DigitalProduct(Product):
    def __init__(self, product_type: str, product_id: str, name: str, price: float, stock_quantity: int, supplier: Supplier, download_size: float):
        super().__init__(product_type=product_type, product_id=product_id, name=name, price=price, stock_quantity=stock_quantity, supplier=supplier)
        self._download_size = download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"Download Size: {self._download_size} MB")

    def get_fulfilment_info(self) -> str:
        return f"This product is delivered digitally. Download size: {self._download_size} MB"

    def to_csv_dict(self) -> dict:
        return {"product_type": self.product_type, "product_id": self.product_id, "name": self.name, "price": self.price, "stock_quantity": self.stock_quantity, "supplier_id": self.supplier_id, "weight": "", "download_size": self.download_size}
    
    @property
    def download_size(self):
        return self._download_size
