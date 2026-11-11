from product import Product
from can_be_shipped import CanBeShipped
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, weight: float):
        super().__init__(product_id, name, price, stock, supplier, type="physical")
        self.__weight = weight

    def display_information(self) -> None:
        super().display_information()
        print(f"Weight: {self.__weight} kg")

    def to_dict(self) -> dict:
        product_dict = super().to_dict()
        product_dict["weight"] = self.__weight
        return product_dict

    def get_fulfilment_info(self) -> str:
        return f"This product requires physical shipping. Shipping weight: {self.__weight} kg"

    def calculate_shipping_cost(self) -> float:
        base_cost = 1.99

        if self.__weight <= 2.00:
            return base_cost
        
        cost_per_kg = 1.00
        return base_cost + (cost_per_kg * self.__weight)

    @property
    def weight(self):
        return self.__weight
