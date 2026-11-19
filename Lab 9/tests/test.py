import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.app_engine import AppEngine
from discounts.bulk_discount import BulkDiscount
from discounts.no_discount import NoDiscount
from discounts.percentage_discount import PercentageDiscount
from discounts.student_discount import StudentDiscount
from managers.data_manager import DataManager
from managers.io_manager import IOManager
from orders.order import Order
from products.product_factory import ProductFactory
from products.products import Products
from suppliers.supplier import Supplier
from suppliers.suppliers import Suppliers


class Tests(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S001", "Test Supplier", "test@example.com")
        self.physical = ProductFactory.create(
            "physical", "P001", "Desk Lamp", 25.0, 10,
            self.supplier, weight=1.5
        )

    def test_01_order_uses_no_discount_by_default(self):
        order = Order("O001")
        order.add_order_line(self.physical, 2)
        self.assertEqual(order.calculate_total(), 50.0)

    def test_02_order_calculates_total_using_discount_strategy(self):
        order = Order("O002", BulkDiscount(200, 20))
        order.add_order_line(self.physical, 10)
        self.assertEqual(order.calculate_total(), 230.0)
        order.set_discount(PercentageDiscount(10))
        self.assertEqual(order.calculate_total(), 225.0)

    def test_03_discount_strategy_can_be_changed(self):
        order = Order("O003", NoDiscount())
        order.add_order_line(self.physical, 4)
        order.set_discount(PercentageDiscount(25))
        self.assertEqual(order.calculate_total(), 75.0)

    def test_04_new_student_strategy_works_without_order_changes(self):
        order = Order("O004", StudentDiscount())
        order.add_order_line(self.physical, 4)
        self.assertEqual(order.calculate_total(), 90.0)

    def test_05_factory_creates_both_product_types(self):
        digital = ProductFactory.create(
            "digital", "D001", "Photo Editor", 49.9, 100,
            self.supplier, download_size=200.0
        )
        self.assertEqual(self.physical.product_type, "physical")
        self.assertEqual(digital.product_type, "digital")
        self.assertEqual(digital.download_size, 200.0)

    def test_06_unknown_product_type_raises_clear_value_error(self):
        with self.assertRaisesRegex(ValueError, "Unknown product type: service"):
            ProductFactory.create(
                "service", "S001", "Installation", 30, 5, self.supplier
            )

    def test_07_invalid_price_stock_and_order_quantity_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "price"):
            ProductFactory.create(
                "physical", "P002", "Bad Price", 0, 1,
                self.supplier, weight=1.0
            )
        with self.assertRaisesRegex(ValueError, "stock"):
            ProductFactory.create(
                "physical", "P003", "Bad Stock", 10, -1,
                self.supplier, weight=1.0
            )
        with self.assertRaisesRegex(ValueError, "quantity"):
            Order("O007").add_order_line(self.physical, 0)

    def test_08_invalid_user_input_retries_until_valid(self):
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]), \
             patch("builtins.print") as mocked_print:
            result = IOManager.get_positive_float("Price: ")
        self.assertEqual(result, 12.5)
        self.assertEqual(mocked_print.call_count, 2)

    def test_09_missing_products_file_is_handled(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = str(Path(directory) / "missing.csv")
            with patch.dict(os.environ, {"PRODUCTS": missing, "SUPPLIERS": missing}):
                manager = DataManager()
                inventory = manager.load_products(Suppliers())
            self.assertEqual(inventory.get_all_products(), [])
            self.assertTrue(Path(missing).exists())
        self.assertIn("Products file not found", " ".join(manager.load_warnings))

    def test_10_bad_csv_rows_are_skipped_and_valid_rows_load(self):
        csv_content = (
            "product_type,product_id,name,price,stock_quantity,supplier_id,weight,download_size\n"
            "physical,P101,Desk Lamp,25.00,10,S001,1.5,\n"
            "digital,D101,Photo Editor,49.90,100,S001,,200.0\n"
            "service,S101,Installation,30.00,5,S001,,\n"
            "physical,P102,Monitor Stand,abc,7,S001,2.0,\n"
            "physical,P103,Chair,39.50,7,S001,3.0,\n"
            "physical,P104,Shelf,15.00,2,S999,1.0,\n"
        )
        suppliers = Suppliers()
        suppliers.add_supplier(self.supplier)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "products.csv"
            path.write_text(csv_content, encoding="utf-8")
            with patch.dict(os.environ, {"PRODUCTS": str(path)}):
                manager = DataManager()
                inventory = manager.load_products(suppliers)
        self.assertEqual(len(inventory.get_all_products()), 3)
        self.assertIsNotNone(inventory.search_product("P101"))
        self.assertIsNotNone(inventory.search_product("D101"))
        self.assertIsNotNone(inventory.search_product("P103"))
        warnings = " ".join(manager.load_warnings)
        self.assertEqual(len(manager.load_warnings), 3)
        self.assertIn("Skipping invalid product row", warnings)
        self.assertIn("Unknown product type: service", warnings)
        self.assertIn("Unknown supplier ID: S999", warnings)

    def test_11_bulk_discount_only_applies_at_threshold(self):
        self.assertEqual(BulkDiscount(200, 20).apply(10), 10)
        self.assertEqual(BulkDiscount(200, 20).apply(199.99), 199.99)
        self.assertEqual(BulkDiscount(200, 20).apply(200), 180)
        self.assertEqual(BulkDiscount(10, 50).apply(20), 0)

    def test_12_saved_inventory_can_be_loaded_again(self):
        suppliers = Suppliers()
        suppliers.add_supplier(self.supplier)
        inventory = Products()
        inventory.add_product(self.physical)
        inventory.add_product(ProductFactory.create(
            "digital", "D001", "Photo Editor", 49.9, 100,
            self.supplier, download_size=200.0
        ))
        with tempfile.TemporaryDirectory() as directory:
            env = {"PRODUCTS": str(Path(directory) / "p.csv"), "SUPPLIERS": str(Path(directory) / "s.csv")}
            with patch.dict(os.environ, env):
                manager = DataManager()
                manager.save_suppliers(suppliers)
                manager.save_products(inventory)
                loaded_suppliers = manager.load_suppliers()
                loaded = manager.load_products(loaded_suppliers)
        self.assertEqual(manager.load_warnings, [])
        self.assertEqual(len(loaded.get_all_products()), 2)
        self.assertEqual(loaded.search_product("P001").stock_quantity, 10)
        self.assertEqual(loaded.search_product("D001").download_size, 200.0)

    def test_13_placing_an_order_adds_stock_and_applies_discount(self):
        with tempfile.TemporaryDirectory() as directory:
            env = {"PRODUCTS": str(Path(directory) / "p.csv"), "SUPPLIERS": str(Path(directory) / "s.csv")}
            with patch.dict(os.environ, env):
                engine = AppEngine()
        engine._suppliers.add_supplier(self.supplier)
        engine._products.add_product(self.physical)
        # product id, quantity, discount 2 = percentage, 10 percent, confirm
        answers = ["P001", "4", "2", "10", "y"]
        with patch("builtins.input", side_effect=answers), patch("builtins.print") as mocked_print:
            engine._place_supplier_order()
        self.assertEqual(self.physical.stock_quantity, 14)
        output = " ".join(str(call) for call in mocked_print.call_args_list)
        self.assertIn("Total after discount: 90.00", output)

    def test_14_cancelled_order_leaves_stock_unchanged(self):
        with tempfile.TemporaryDirectory() as directory:
            env = {"PRODUCTS": str(Path(directory) / "p.csv"), "SUPPLIERS": str(Path(directory) / "s.csv")}
            with patch.dict(os.environ, env):
                engine = AppEngine()
        engine._suppliers.add_supplier(self.supplier)
        engine._products.add_product(self.physical)
        with patch("builtins.input", side_effect=["P001", "4", "1", "n"]), patch("builtins.print"):
            engine._place_supplier_order()
        self.assertEqual(self.physical.stock_quantity, 10)


if __name__ == "__main__":
    unittest.main()
