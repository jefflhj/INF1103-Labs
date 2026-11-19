from discounts.discount_strategy import DiscountStrategy


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: int):
        self._percentage = percentage

    def apply(self, total: float) -> float:
        return total - (total * (self._percentage/100))
