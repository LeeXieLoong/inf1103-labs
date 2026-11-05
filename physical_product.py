import math

from can_be_shipped import CanBeShipped
from product import Product, ProductRecord
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    def __init__(
        self, product_id: str, name: str, price: float, stock: int,
        weight: float, supplier: Supplier,
    ) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if not math.isfinite(weight) or weight <= 0:
            raise ValueError("Weight must be a positive number in kilograms.")
        self.__weight: float = weight

    def get_weight(self) -> float:
        return self.__weight

    def display_information(self) -> None:
        super().display_information()
        print(f"Type: Physical | Weight: {self.__weight:g} kg")
        print(self.get_fulfilment_info())
        print(f"Shipping cost: ${self.calculate_shipping_cost():.2f}")

    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        # Shipping costs $5 per kilogram for one product.
        return round(self.__weight * 5.00, 2)

    def to_dict(self) -> ProductRecord:
        record = super().to_dict()
        record["type"] = "physical"
        record["weight"] = self.__weight
        return record
