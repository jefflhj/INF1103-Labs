from products.product import Product


class OrderLine:
    def __init__(self, product: Product, quantity: int):
        self._product = product
        self._quantity = quantity

    def calculate_subtotal(self) -> float:
        return self._product.price * self._quantity
