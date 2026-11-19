from abc import ABC, abstractmethod

from suppliers.supplier import Supplier


class Product(ABC):
    def __init__(self, product_type: str, product_id: str, name: str, price: float, stock_quantity: int, supplier: Supplier):
        if price <= 0:
            raise ValueError("Product price must be greater than zero.")
        if stock_quantity < 0:
            raise ValueError("Product stock quantity cannot be negative.")
        self._product_type = product_type
        self._product_id = product_id
        self._name = name
        self._price = float(price)
        self._stock_quantity = int(stock_quantity)
        self._supplier = supplier

    def update_stock(self, new_quantity: int) -> None:
        if new_quantity < 0:
            raise ValueError("Product stock quantity cannot be negative.")
        self._stock_quantity = new_quantity

    def display_information(self) -> None:
        print(f"Supplier Information")
        print("--------------------")
        self._supplier.display_information()
        print(f"\nProduct Information")
        print("--------------------")
        print(f"ID: {self._product_id}")
        print(f"Name: {self._name}")
        print(f"Price: {self._price}")
        print(f"Stock: {self._stock_quantity}")
        
    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    @abstractmethod
    def to_csv_dict(self) -> dict:
        pass

    @property
    def product_type(self) -> str:
        return self._product_type

    @property
    def product_id(self) -> str:
        return self._product_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self._price

    @property
    def stock_quantity(self) -> int:
        return self._stock_quantity

    @property
    def supplier_id(self) -> str:
        return self._supplier.supplier_id
