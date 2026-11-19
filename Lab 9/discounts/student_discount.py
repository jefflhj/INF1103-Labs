"""
    All students get 10% off all orders.
"""

from discounts.discount_strategy import DiscountStrategy


class StudentDiscount(DiscountStrategy):
    def __init__(self):
        self._percentage = 10

    def apply(self, total: float) -> float:
        if self._percentage < 0 or self._percentage > 100:
            raise ValueError("Percentage discount must be between 0 to 100 percent.")
        else:
            return total - (total * (self._percentage/100))
