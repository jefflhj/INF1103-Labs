from discounts.bulk_discount import BulkDiscount
from discounts.discount_strategy import DiscountStrategy
from discounts.no_discount import NoDiscount
from discounts.percentage_discount import PercentageDiscount
from discounts.student_discount import StudentDiscount
from managers.data_manager import DataManager
from managers.io_manager import IOManager
from orders.order import Order
from products.product import Product
from products.product_factory import ProductFactory
from products.products import Products
from suppliers.supplier import Supplier
from suppliers.suppliers import Suppliers


class AppEngine:
    def __init__(self):
        self._data_manager = DataManager()
        self._suppliers = Suppliers()
        self._products = Products()
        self._orders: list[Order] = []
        self._has_unsaved_changes = False
        self._running = False
        self._actions = {
            1: self._display_products,
            2: self._add_product,
            3: self._search_product,
            4: self._update_product_stock,
            5: self._place_supplier_order,
            6: self._display_suppliers,
            7: self._add_supplier,
            8: self._search_supplier,
            9: self._save_inventory,
            10: self._exit,
        }

    # ===== Workflow =====
    def run(self) -> None:
        self._load_inventory()
        self._running = True
        while self._running:
            IOManager.clear_terminal()
            IOManager.print_system_banner()
            IOManager.show_option_menu()
            choice = IOManager.get_option_menu_choice()
            IOManager.clear_terminal()

            try:
                self._actions[choice]()
            except (ValueError, PermissionError, RuntimeError, OSError) as error:
                IOManager.show_message(f"Error: {error}")

            if self._running:
                IOManager.pause()

    def _load_inventory(self) -> None:
        self._suppliers = self._data_manager.load_suppliers()
        warnings = self._data_manager.load_warnings
        self._products = self._data_manager.load_products(self._suppliers)
        warnings += self._data_manager.load_warnings

        IOManager.print_system_banner()
        IOManager.show_messages(warnings)
        IOManager.show_message(f"{len(self._suppliers.get_all_suppliers())} suppliers loaded.")
        IOManager.show_message(f"{len(self._products.get_all_products())} products loaded.")
        if warnings:
            IOManager.pause()

    # ===== Products =====
    def _display_products(self) -> None:
        products = self._products.get_all_products()
        if not products:
            IOManager.show_message("No products in the inventory.")
            return

        IOManager.show_heading(f"All Products ({len(products)})")
        for product in products:
            product.display_information()
            IOManager.show_separator()

    def _add_product(self) -> None:
        if not self._suppliers.get_all_suppliers():
            IOManager.show_message("There are no suppliers yet. Please add a supplier before adding a product.")
            return

        product_type = ("physical", "digital")[IOManager.get_choice("Product type", ["Physical", "Digital"]) - 1]
        product_id = self._ask_new_product_id()
        name = IOManager.get_non_empty_string("Name: ")
        price = IOManager.get_positive_float("Price: ")
        stock_quantity = IOManager.get_non_negative_int("Stock quantity: ")
        supplier = self._ask_existing_supplier()

        weight = download_size = None
        if product_type == "physical":
            weight = IOManager.get_positive_float("Weight (kg): ")
        else:
            download_size = IOManager.get_positive_float("Download size (MB): ")

        product = ProductFactory.create(product_type, product_id, name, price, stock_quantity, supplier, weight=weight, download_size=download_size)
        IOManager.show_message(self._products.add_product(product))
        self._has_unsaved_changes = True

    def _search_product(self) -> None:
        product = self._products.search_product(IOManager.get_non_empty_string("Product ID: "))
        if product is None:
            IOManager.show_message("Product not found.")
            return
        IOManager.show_separator()
        product.display_information()

    def _update_product_stock(self) -> None:
        product = self._ask_existing_product_or_none()
        if product is None:
            return
        IOManager.show_message(f"{product.name} currently has {product.stock_quantity} in stock.")
        product.update_stock(IOManager.get_non_negative_int("New stock quantity: "))
        IOManager.show_message(f"Stock for {product.name} updated to {product.stock_quantity}.")
        self._has_unsaved_changes = True

    # ===== Orders =====
    def _place_supplier_order(self) -> None:
        product = self._ask_existing_product_or_none()
        if product is None:
            return

        supplier = self._suppliers.search_supplier(product.supplier_id)
        quantity = IOManager.get_positive_int("Quantity to order: ")
        order = Order(f"O{len(self._orders) + 1:03d}", self._ask_discount_strategy())
        order.add_order_line(product, quantity)

        IOManager.show_heading("Order Summary")
        IOManager.show_message(f"Order ID: {order.order_id}")
        IOManager.show_message(f"Supplier: {supplier.name} ({supplier.email})")
        IOManager.show_message(f"Product: {product.name} ({product.product_id})")
        IOManager.show_message(f"Quantity: {quantity}")
        IOManager.show_message(f"Subtotal: {product.price * quantity:.2f}")
        IOManager.show_message(f"Total after discount: {order.calculate_total():.2f}")

        if not IOManager.get_yes_no("\nPlace this order? (y/n): "):
            IOManager.show_message("Order cancelled.")
            return

        # The ordered stock is added to the inventory straight away.
        product.update_stock(product.stock_quantity + quantity)
        self._orders.append(order)
        self._has_unsaved_changes = True
        IOManager.show_message(f"Order {order.order_id} placed with {supplier.name}. {product.name} stock is now {product.stock_quantity}.")

    def _ask_discount_strategy(self) -> DiscountStrategy:
        choice = IOManager.get_choice("Discount", ["None", "Percentage", "Bulk (amount off when total reaches a threshold)", "Student (10% off)"])
        if choice == 2:
            return PercentageDiscount(IOManager.get_positive_float("Percentage off (1-100): ", maximum=100))
        if choice == 3:
            threshold = IOManager.get_positive_float("Total needed to qualify: ")
            amount = IOManager.get_positive_float("Amount off: ")
            return BulkDiscount(threshold, amount)
        if choice == 4:
            return StudentDiscount()
        return NoDiscount()

    # ===== Suppliers =====
    def _display_suppliers(self) -> None:
        suppliers = self._suppliers.get_all_suppliers()
        if not suppliers:
            IOManager.show_message("No suppliers in the system.")
            return

        IOManager.show_heading(f"All Suppliers ({len(suppliers)})")
        for supplier in suppliers:
            supplier.display_information()
            IOManager.show_separator()

    def _add_supplier(self) -> None:
        while True:
            supplier_id = IOManager.get_non_empty_string("Supplier ID: ")
            if self._suppliers.search_supplier(supplier_id) is None:
                break
            IOManager.show_message("A supplier with that ID already exists.")

        name = IOManager.get_non_empty_string("Name: ")
        email = IOManager.get_email("Email: ")
        IOManager.show_message(self._suppliers.add_supplier(Supplier(supplier_id, name, email)))
        self._has_unsaved_changes = True

    def _search_supplier(self) -> None:
        supplier = self._suppliers.search_supplier(IOManager.get_non_empty_string("Supplier ID: "))
        if supplier is None:
            IOManager.show_message("Supplier not found.")
            return
        IOManager.show_separator()
        supplier.display_information()

    # ===== Saving and exiting =====
    def _save_inventory(self) -> None:
        self._data_manager.save_suppliers(self._suppliers)
        self._data_manager.save_products(self._products)
        self._has_unsaved_changes = False
        IOManager.show_message("Inventory saved.")

    def _exit(self) -> None:
        if self._has_unsaved_changes and IOManager.get_yes_no("You have unsaved changes. Save before exiting? (y/n): "):
            self._save_inventory()
        self._running = False
        IOManager.show_exit_message()

    # ===== Shared prompts =====
    def _ask_new_product_id(self) -> str:
        while True:
            product_id = IOManager.get_non_empty_string("Product ID: ")
            if self._products.search_product(product_id) is None:
                return product_id
            IOManager.show_message("A product with that ID already exists.")

    def _ask_existing_supplier(self) -> Supplier:
        while True:
            supplier = self._suppliers.search_supplier(IOManager.get_non_empty_string("Supplier ID: "))
            if supplier is not None:
                return supplier
            available = ", ".join(s.supplier_id for s in self._suppliers.get_all_suppliers())
            IOManager.show_message(f"Supplier not found. Available supplier IDs: {available}")

    def _ask_existing_product_or_none(self) -> Product | None:
        if not self._products.get_all_products():
            IOManager.show_message("No products in the inventory.")
            return None
        product = self._products.search_product(IOManager.get_non_empty_string("Product ID: "))
        if product is None:
            IOManager.show_message("Product not found.")
        return product
