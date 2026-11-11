from product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, supplier, weight):
        super().__init__(product_id, name, price, stock, supplier, type="physical")
        self.__weight = weight

    def display_information(self):
        super().display_information()
        print(f"Weight: {self.__weight} kg")

    def to_dict(self):
        product_dict = super().to_dict()
        product_dict["weight"] = self.__weight
        return product_dict

    def get_fulfilment_info(self):
        return f"This product requires physical shipping. Shipping weight: {self.__weight} kg"

    def calculate_shipping_cost(self):
        base_cost = 1.99

        if self.__weight <= 2.00:
            return base_cost
        
        cost_per_kg = 1.00
        return base_cost + (cost_per_kg * self.__weight)

    @property
    def weight(self):
        return self.__weight
