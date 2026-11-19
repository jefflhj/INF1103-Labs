"""
    All students get 10% off all orders.
"""

from discounts.discount_strategy import DiscountStrategy


class StudentDiscount(DiscountStrategy):
    def __init__(self):
        self._percentage = 10

    def apply(self, total: float) -> float:
        return total - (total * (self._percentage/100))
