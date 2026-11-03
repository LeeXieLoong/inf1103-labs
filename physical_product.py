import math

from can_be_shipped import CanBeShipped
from product import Product


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        if not math.isfinite(weight) or weight <= 0:
            raise ValueError("Weight must be a positive number in kilograms.")
        self.__weight = weight

    def get_weight(self):
        return self.__weight

    def display_information(self):
        super().display_information()
        print(f"Type: Physical | Weight: {self.__weight:g} kg")
        print(self.get_fulfilment_info())
        print(f"Shipping cost: ${self.calculate_shipping_cost():.2f}")

    def get_fulfilment_info(self):
        return "Requires physical shipping."

    def calculate_shipping_cost(self):
        # Shipping costs $5 per kilogram for one product.
        return round(self.__weight * 5.00, 2)

    def to_dict(self):
        record = super().to_dict()
        record["type"] = "physical"
        record["weight"] = self.__weight
        return record
