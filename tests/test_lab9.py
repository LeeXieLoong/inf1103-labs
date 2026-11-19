import contextlib
import csv
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from digital_product import DigitalProduct
from discount_strategy import (
    BulkDiscount, DiscountStrategy, NoDiscount, PercentageDiscount, StudentDiscount,
)
from inventory import Inventory
from inventory_manager import get_positive_float, load_products
from order import Order
from order_line import OrderLine
from physical_product import PhysicalProduct
from product_factory import ProductFactory
from supplier import Supplier


PROJECT_DIR = Path(__file__).resolve().parents[1]


class Lab9Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S009", "Lab 9 Supplies", "sales@example.com")
        self.product = ProductFactory.create(
            "physical", "P009", "Test product", 25.0, 10, self.supplier, weight=0.5
        )

    def test_strategy_base_is_abstract(self) -> None:
        with self.assertRaises(TypeError):
            DiscountStrategy()

    def test_order_uses_no_discount_by_default(self) -> None:
        order = Order("O001")
        self.assertEqual(order.calculate_total(), 0.0)
        order.add_order_line(self.product, 10)
        self.assertEqual(order.calculate_total(), 250.0)
        self.assertEqual(NoDiscount().apply(250.0), 250.0)

    def test_existing_order_can_change_from_bulk_to_percentage(self) -> None:
        order = Order("O001", BulkDiscount(200, 20))
        order.add_order_line(self.product, 10)
        self.assertEqual(order.calculate_total(), 230.0)
        order.set_discount(PercentageDiscount(10))
        self.assertEqual(order.calculate_total(), 225.0)

    def test_student_discount_and_new_strategy_work_without_changing_order(self) -> None:
        class FixedDiscount(DiscountStrategy):
            def apply(self, total: float) -> float:
                return total - 5.0

        order = Order("O001", StudentDiscount())
        order.add_order_line(self.product, 10)
        self.assertEqual(order.calculate_total(), 237.5)
        order.set_discount(FixedDiscount())
        self.assertEqual(order.calculate_total(), 245.0)

    def test_two_orders_can_share_one_strategy(self) -> None:
        discount = PercentageDiscount(10)
        first = Order("O001", discount)
        second = Order("O002", discount)
        first.add_order_line(self.product, 10)
        second.add_order_line(self.product, 2)
        self.assertEqual(first.calculate_total(), 225.0)
        self.assertEqual(second.calculate_total(), 45.0)
        first.set_discount(NoDiscount())
        self.assertEqual(first.calculate_total(), 250.0)
        self.assertEqual(second.calculate_total(), 45.0)

    def test_bulk_threshold_and_discount_limits(self) -> None:
        discount = BulkDiscount(200, 20)
        self.assertEqual(discount.apply(199), 199)
        self.assertEqual(discount.apply(200), 180)
        self.assertEqual(BulkDiscount(0, 20).apply(10), 0.0)
        self.assertEqual(PercentageDiscount(0).apply(250), 250)
        self.assertEqual(PercentageDiscount(100).apply(250), 0)

    def test_invalid_discount_parameters_are_rejected(self) -> None:
        for percentage in [-1, 101, float("nan"), float("inf")]:
            with self.subTest(percentage=percentage), self.assertRaises(ValueError):
                PercentageDiscount(percentage)
        for threshold, amount in [(-1, 20), (200, -1), (float("nan"), 20), (200, float("inf"))]:
            with self.subTest(threshold=threshold, amount=amount):
                with self.assertRaises(ValueError):
                    BulkDiscount(threshold, amount)

    def test_factory_creates_both_product_types_with_supplier_and_measurement(self) -> None:
        digital = ProductFactory.create(
            "digital", "D009", "Ebook", 12.5, 4, self.supplier, download_size=150
        )
        self.assertIsInstance(self.product, PhysicalProduct)
        self.assertIsInstance(digital, DigitalProduct)
        self.assertEqual(self.product.get_weight(), 0.5)
        self.assertEqual(digital.get_download_size(), 150)
        self.assertIs(self.product.get_supplier(), self.supplier)
        self.assertIs(digital.get_supplier(), self.supplier)

    def test_factory_rejects_unknown_type_and_missing_measurements(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unknown product type: service"):
            ProductFactory.create("service", "S001", "Installation", 30, 5, self.supplier)
        for kind in ["physical", "digital"]:
            with self.subTest(kind=kind), self.assertRaisesRegex(ValueError, "require"):
                ProductFactory.create(kind, "P001", "Test", 10, 1, self.supplier)

    def test_both_product_types_reject_invalid_prices(self) -> None:
        for kind in ["physical", "digital"]:
            for price in [0, -1, float("nan"), float("inf")]:
                with self.subTest(kind=kind, price=price), self.assertRaises(ValueError):
                    ProductFactory.create(
                        kind, "P001", "Test", price, 1, self.supplier,
                        weight=1, download_size=100,
                    )

    def test_both_subclasses_preserve_stock_validation(self) -> None:
        for kind in ["physical", "digital"]:
            with self.subTest(kind=kind):
                with self.assertRaises(ValueError):
                    ProductFactory.create(
                        kind, "P001", "Test", 10, -1, self.supplier,
                        weight=1, download_size=100,
                    )
                product = ProductFactory.create(
                    kind, "P001", "Test", 10, 5, self.supplier,
                    weight=1, download_size=100,
                )
                with self.assertRaises(ValueError):
                    product.update_stock(-1)
                self.assertEqual(product.get_stock(), 5)
                product.update_stock(0)
                self.assertEqual(product.get_stock(), 0)

    def test_order_line_rejects_invalid_quantities_without_changing_order(self) -> None:
        order = Order("O001")
        for quantity in [0, -1, 1.5, True]:
            with self.subTest(quantity=quantity), self.assertRaises(ValueError):
                order.add_order_line(self.product, quantity)
        self.assertEqual(order.get_order_lines(), ())
        self.assertEqual(OrderLine(self.product, 2).calculate_subtotal(), 50)

    def test_price_input_retries_text_and_negative_value(self) -> None:
        output = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]) as prompt:
            with contextlib.redirect_stdout(output):
                price = get_positive_float("Price: ")
        self.assertEqual(price, 12.5)
        self.assertEqual(prompt.call_count, 3)
        self.assertEqual(output.getvalue().splitlines(), [
            "Please enter a valid number, e.g. 12.50",
            "Please enter a number greater than zero.",
        ])

    def test_price_input_rejects_zero_and_non_finite_values(self) -> None:
        with patch("builtins.input", side_effect=["0", "nan", "inf", "2.50"]):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(get_positive_float("Price: "), 2.5)

    def test_supplied_csv_loads_three_products_and_reports_bad_rows_in_order(self) -> None:
        inventory = Inventory()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            load_products(str(PROJECT_DIR / "products.csv"), inventory, self.supplier)
        self.assertEqual(
            [product.get_product_id() for product in inventory.get_products()],
            ["P001", "D001", "P003"],
        )
        self.assertEqual(output.getvalue().splitlines(), [
            "Row 4 skipped: Unknown product type: service",
            "Row 5 skipped: could not convert string to float: 'abc'",
            "3 products loaded.",
            "Load attempt finished.",
        ])
        self.assertEqual(inventory.find_product("P001").get_weight(), 0.5)
        self.assertEqual(inventory.find_product("D001").get_download_size(), 150)

    def test_missing_csv_runs_except_and_finally_without_loading(self) -> None:
        inventory = Inventory()
        with tempfile.TemporaryDirectory(prefix="lab9-test-", dir=PROJECT_DIR) as folder:
            original = Path(folder) / "products.csv"
            original.write_bytes((PROJECT_DIR / "products.csv").read_bytes())
            original.rename(Path(folder) / "products-renamed.csv")
            missing = str(original)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                load_products(missing, inventory, self.supplier)
        self.assertEqual(output.getvalue().splitlines(), [
            f"Products file not found: {missing}",
            "Load attempt finished.",
        ])
        self.assertEqual(inventory.get_products(), [])

    def test_bad_csv_rows_and_duplicate_ids_do_not_stop_later_valid_rows(self) -> None:
        inventory = Inventory()
        rows = [
            ["physical", "P001", "Bad price", "0", "1", "1", ""],
            ["digital", "D001", "Bad stock", "10", "-1", "", "100"],
            ["physical", "P002", "Missing weight", "10", "1", "", ""],
            ["too", "few", "columns"],
            ["digital", "D002", "Good ebook", "10", "2", "", "100"],
            ["digital", "D002", "Duplicate", "15", "3", "", "150"],
            ["physical", "P003", "Good book", "20", "4", "0.5", ""],
        ]
        with tempfile.TemporaryDirectory(prefix="lab9-test-", dir=PROJECT_DIR) as folder:
            path = Path(folder) / "products.csv"
            with path.open("w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["product_type", "product_id", "name", "price", "stock_quantity", "weight", "download_size"])
                writer.writerows(rows)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                load_products(str(path), inventory, self.supplier)
        self.assertEqual(len(inventory.get_products()), 2)
        self.assertIsNone(inventory.find_product("P001"))
        self.assertEqual(inventory.find_product("D002").get_name(), "Good ebook")
        self.assertEqual(inventory.find_product("P003").get_stock(), 4)
        self.assertIn("Duplicate product ID: D002", output.getvalue())
        self.assertTrue(output.getvalue().endswith("2 products loaded.\nLoad attempt finished.\n"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
