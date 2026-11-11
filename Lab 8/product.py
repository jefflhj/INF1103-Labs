from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, type: str):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock
        self._supplier: Supplier = supplier
        self.__type = type

    def update_stock(self, quantity: int) -> bool:
        if quantity >= 0 and isinstance(quantity, int): # not really needed here since input validation alr done in the update_stock function
            self.__stock = quantity
            return True

        else:
            return False

    def display_information(self) -> None:
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.price:.2f}")
        print(f"Stock: {self.stock}")

    def display_supplier_information(self) -> None:
        self._supplier.display_information()

    def to_dict(self) -> dict:
        return {
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "type": self.__type
        }

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    @property
    def product_id(self):
        return self.__product_id # These are immutable so they cant be edited outide the class even if exposed like this. Example if return a dict, then they would be editable outside.

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def stock(self):
        return self.__stock


