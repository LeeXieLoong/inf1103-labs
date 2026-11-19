from discount_strategy import DiscountStrategy, NoDiscount
from order_line import OrderLine
from product import Product


class Order:
    def __init__(
        self, order_id: str, discount: DiscountStrategy | None = None
    ) -> None:
        if not order_id.strip():
            raise ValueError("Order ID cannot be empty.")
        self.__order_id: str = order_id.strip().upper()
        self.__order_lines: list[OrderLine] = []
        self.__discount: DiscountStrategy = NoDiscount() if discount is None else discount

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.__discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        self.__order_lines.append(OrderLine(product, quantity))

    def remove_order_line(self, line_number: int) -> bool:
        if 1 <= line_number <= len(self.__order_lines):
            del self.__order_lines[line_number - 1]
            return True
        return False

    def get_order_lines(self) -> tuple[OrderLine, ...]:
        return tuple(self.__order_lines)

    def calculate_total(self) -> float:
        total = sum((line.calculate_subtotal() for line in self.__order_lines), 0.0)
        return self.__discount.apply(total)

    def display_information(self) -> None:
        print(f"\nOrder {self.__order_id}")
        for line in self.__order_lines:
            line.display_information()
        print(f"Order total: ${self.calculate_total():.2f}")
