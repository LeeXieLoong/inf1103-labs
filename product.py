import math
from abc import ABC, abstractmethod

from supplier import Supplier


ProductRecord = dict[str, str | float | int | dict[str, str]]


class Product(ABC):
    def __init__(
        self, product_id: str, name: str, price: float, stock: int, supplier: Supplier
    ) -> None:
        if not product_id.strip() or not name.strip():
            raise ValueError("Product ID and name cannot be empty.")
        if not math.isfinite(price) or price < 0:
            raise ValueError("Price must be a valid non-negative number.")

        self.__product_id: str = product_id.strip().upper()
        self.__name: str = name.strip()
        self.__price: float = price
        self.__supplier: Supplier = supplier
        self.__stock: int
        self.update_stock(stock)

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def get_stock(self) -> int:
        return self.__stock

    def update_stock(self, quantity: int) -> None:
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Stock must be a non-negative whole number.")
        self.__stock = quantity

    def display_information(self) -> None:
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}"
        )
        self.__supplier.display_information()

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    def to_dict(self) -> ProductRecord:
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": self.__supplier.to_dict(),
        }
