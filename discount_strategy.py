import math
from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float) -> None:
        if not math.isfinite(percentage) or not 0 <= percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.__percentage: float = percentage

    def apply(self, total: float) -> float:
        return round(total * (1 - self.__percentage / 100), 2)


class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float) -> None:
        if not math.isfinite(threshold) or threshold < 0:
            raise ValueError("Discount threshold must be non-negative.")
        if not math.isfinite(amount) or amount < 0:
            raise ValueError("Discount amount must be non-negative.")
        self.__threshold: float = threshold
        self.__amount: float = amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return max(0.0, total - self.__amount)
        return total


class StudentDiscount(PercentageDiscount):
    def __init__(self) -> None:
        super().__init__(5)
