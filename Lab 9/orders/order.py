"""
    An order is made up of order line objects.
    Has an id, items list, and discount strategy if any.
"""

from products.product import Product
from orders.order_line import OrderLine
from discounts.discount_strategy import DiscountStrategy
from discounts.no_discount import NoDiscount


class Order:
    def __init__(self, order_id: str, discount_strategy: DiscountStrategy = None):
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []
        self._discount_strategy = discount_strategy if discount_strategy is not None else NoDiscount()

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def calculate_total(self) -> float:
        total = sum(line.calculate_subtotal() for line in self.order_lines)
        return self._discount_strategy.apply(total)

    def set_discount(self, discount_strategy: DiscountStrategy) -> None:
        self._discount_strategy = discount_strategy
