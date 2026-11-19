from abc import ABC, abstractmethod

from suppliers.supplier import Supplier


class Product(ABC):
    def __init__(self, product_type: str, product_id: str, name: str, price: float, stock_quantity: int, supplier: Supplier):
        self._product_type = product_type
        self._product_id = product_id
        self._name = name
        self._price = price
        self._stock_quantity = stock_quantity
        self._supplier = supplier

    def update_stock():
        pass

    def display_product_information():
        pass

    def display_supplier_information():
        pass

    @abstractmethod
    def get_fulfilment_info():
        pass

    @property
    def product_type(self) -> str:
        return self._product_type

    @property
    def product_id(self) -> str:
        return self._product_id

    @property
    def name(self) -> str:
        return self.name

    @property
    def price(self) -> float:
        return self.price

    @property
    def stock_quantity(self) -> int:
        return self._stock_quantity

    @property
    def supplier_id(self) -> str:
        return self._supplier.supplier_id
