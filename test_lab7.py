import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from can_be_shipped import CanBeShipped
from digital_product import DigitalProduct
from inventory import Inventory
from inventory_manager import load_inventory, main, save_inventory
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


PROJECT_DIR = Path(__file__).resolve().parent
TEST_SUPPLIER = Supplier("S001", "Lab Supplies", "sales@example.com")


class Lab7Tests(unittest.TestCase):
    def setUp(self):
        self.previous_directory = Path.cwd()
        self.temp_directory = tempfile.TemporaryDirectory(
            prefix="lab7-test-", dir=PROJECT_DIR
        )
        os.chdir(self.temp_directory.name)

    def tearDown(self):
        os.chdir(self.previous_directory)
        self.temp_directory.cleanup()

    def test_abstract_classes_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Product("P001", "Generic", 10, 2, TEST_SUPPLIER)
        with self.assertRaises(TypeError):
            CanBeShipped()

        class IncompleteProduct(Product):
            pass

        with self.assertRaises(TypeError):
            IncompleteProduct("P001", "Incomplete", 10, 2, TEST_SUPPLIER)

    def test_physical_product_displays_common_and_extra_information(self):
        product = PhysicalProduct("P001", "Laptop", 1200, 15, 2.5, TEST_SUPPLIER)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            product.display_information()
        for text in ["P001", "Laptop", "$1200.00", "Stock: 15", "2.5 kg", "$12.50"]:
            self.assertIn(text, output.getvalue())
        self.assertEqual(product.get_weight(), 2.5)
        self.assertIn("shipping", product.get_fulfilment_info())
        self.assertIsInstance(product, CanBeShipped)

    def test_digital_product_displays_information_without_shipping(self):
        product = DigitalProduct("D001", "Ebook", 12.5, 30, 100, TEST_SUPPLIER)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            product.display_information()
        for text in ["D001", "Ebook", "$12.50", "Stock: 30", "100 MB"]:
            self.assertIn(text, output.getvalue())
        self.assertEqual(product.get_download_size(), 100)
        self.assertIn("download", product.get_fulfilment_info())
        self.assertNotIsInstance(product, CanBeShipped)
        self.assertFalse(hasattr(product, "calculate_shipping_cost"))

    def test_shipping_cost_depends_on_weight(self):
        light = PhysicalProduct("P001", "Light", 10, 1, 1, TEST_SUPPLIER)
        heavy = PhysicalProduct("P002", "Heavy", 10, 1, 3.5, TEST_SUPPLIER)
        self.assertEqual(light.calculate_shipping_cost(), 5)
        self.assertEqual(heavy.calculate_shipping_cost(), 17.5)

    def test_measurements_reject_non_positive_and_non_finite_values(self):
        for product_class in [PhysicalProduct, DigitalProduct]:
            for value in [0, -1, float("nan"), float("inf")]:
                with self.subTest(product_class=product_class, value=value):
                    with self.assertRaises(ValueError):
                        product_class("P001", "Test", 10, 1, value, TEST_SUPPLIER)

    def test_inventory_operations_work_with_both_types(self):
        inventory = Inventory()
        physical = PhysicalProduct("P001", "Laptop", 1200, 15, 2.5, TEST_SUPPLIER)
        digital = DigitalProduct("D001", "Ebook", 12.5, 30, 100, TEST_SUPPLIER)
        self.assertTrue(inventory.add_product(physical))
        self.assertTrue(inventory.add_product(digital))
        self.assertFalse(inventory.add_product(physical))
        self.assertIs(inventory.search_product(" d001 "), digital)
        self.assertTrue(inventory.update_stock("p001", 0))
        self.assertEqual(physical.get_stock(), 0)
        self.assertFalse(inventory.update_stock("missing", 2))
        self.assertIsNone(inventory.search_product("missing"))
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            inventory.display_all()
        self.assertIn("2.5 kg", output.getvalue())
        self.assertIn("100 MB", output.getvalue())

    def test_save_and_reload_preserves_types_and_additional_attributes(self):
        inventory = Inventory()
        inventory.add_product(PhysicalProduct("P001", "Laptop", 1200, 15, 2.5, TEST_SUPPLIER))
        inventory.add_product(DigitalProduct("D001", "Ebook", 12.5, 30, 100, TEST_SUPPLIER))
        with contextlib.redirect_stdout(io.StringIO()):
            save_inventory(inventory)
            with patch("builtins.input", side_effect=AssertionError("Unexpected prompt")):
                restored = load_inventory()
        self.assertIsInstance(restored.search_product("P001"), PhysicalProduct)
        self.assertIsInstance(restored.search_product("D001"), DigitalProduct)
        self.assertEqual(
            [product.to_dict() for product in restored.get_products()],
            [product.to_dict() for product in inventory.get_products()],
        )

    def test_legacy_records_ask_for_their_types_before_saving(self):
        records = [
            {"id": "P001", "name": "Laptop", "price": 1200, "stock": 15},
            {"id": "D001", "name": "Ebook", "price": 12.5, "stock": 30},
        ]
        Path("inventory.json").write_text(json.dumps(records), encoding="utf-8")
        answers = ["x", "1", "nan", "0", "-2", "2.5", "2", "100"]
        with patch("builtins.input", side_effect=answers):
            with contextlib.redirect_stdout(io.StringIO()):
                inventory = load_inventory()
                self.assertEqual(json.loads(Path("inventory.json").read_text()), records)
                save_inventory(inventory)
        saved = json.loads(Path("inventory.json").read_text())
        self.assertEqual(saved[0]["type"], "physical")
        self.assertEqual(saved[0]["weight"], 2.5)
        self.assertEqual(saved[1]["type"], "digital")
        self.assertEqual(saved[1]["download_size"], 100)
        self.assertEqual(saved[0]["supplier"]["supplier_id"], "UNASSIGNED")

    def test_bad_inventory_data_is_not_overwritten(self):
        invalid_files = ["not JSON", "{}", '[{"type": "unknown"}]']
        for contents in invalid_files:
            with self.subTest(contents=contents):
                Path("inventory.json").write_text(contents, encoding="utf-8")
                with contextlib.redirect_stdout(io.StringIO()):
                    main()
                self.assertEqual(Path("inventory.json").read_text(), contents)

    def test_menu_and_restart_preserve_both_product_types(self):
        answers = [
            "1", "2", "P001", "Laptop", "-1", "1200", "-1", "15",
            "S001", "Lab Supplies", "sales@example.com", "1", "2.5",
            "2", "D001", "Ebook", "12.5", "30", "s001", "2", "100",
            "2", "P001", "3", "P001", "9", "4", "D001", "5", "6", "",
        ]
        command = [sys.executable, "-B", str(PROJECT_DIR / "inventory_manager.py")]
        first = subprocess.run(
            command, input="\n".join(answers), capture_output=True, text=True, timeout=15
        )
        self.assertEqual(first.returncode, 0, first.stderr)
        for text in ["Inventory is empty.", "Product ID already exists.",
                     "Stock updated successfully!", "100 MB", "Inventory saved successfully"]:
            self.assertIn(text, first.stdout)
        second = subprocess.run(
            command, input="1\n6\n", capture_output=True, text=True, timeout=15
        )
        self.assertEqual(second.returncode, 0, second.stderr)
        for text in ["2.5 kg", "100 MB", "Stock: 9", "Shipping cost: $12.50"]:
            self.assertIn(text, second.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
