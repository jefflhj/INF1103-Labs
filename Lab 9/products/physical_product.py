from products.product import Product
from suppliers.supplier import Supplier
from products.can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_type: str, product_id: str, name: str, price: float, stock_quantity: int, supplier: Supplier, weight: float):
        super().__init__(product_type=product_type, product_id=product_id, name=name, price=price, stock_quantity=stock_quantity, supplier=supplier)
        self._weight = weight

    def display_information(self) -> None:
        super().display_information()
        print(f"Weight: {self._weight} kg")

    def get_fulfilment_info(self) -> str:
        return f"This product requires physical shipping. Shipping weight: {self._weight} kg"

    def calculate_shipping_cost(self) -> float:
        base_cost = 1.99
        if self._weight <= 2.00:
            return base_cost
        cost_per_kg = 1.00
        return base_cost + (cost_per_kg * self._weight)

    def to_csv_dict(self) -> dict:
        return {"product_type": self.product_type, "product_id": self.product_id, "name": self.name, "price": self.price, "stock_quantity": self.stock_quantity, "supplier_id": self.supplier_id, "weight": self.weight, "download_size": ""}
    
    @property
    def weight(self):
        return self._weight
