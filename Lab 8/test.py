from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier
from suppliers import Suppliers
from inventory import Inventory
from order import Order
from can_be_shipped import CanBeShipped


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


def show_info_fulfilment(inventory: Inventory, product1: PhysicalProduct, product2: DigitalProduct) -> None:
    inventory.add_product(product1)
    inventory.add_product(product2)

    inventory.search_product(product1.product_id).display_information()
    print(inventory.search_product(product1.product_id).get_fulfilment_info())
    print()
    inventory.search_product(product2.product_id).display_information()
    print(inventory.search_product(product2.product_id).get_fulfilment_info())


def test_supplier_relationship():
    print("\n=== SUPPLIER RELATIONSHIP ===")

    supplier = Supplier("S001", "Tech Supplies", "tech@example.com")

    suppliers = Suppliers()
    suppliers.add_supplier(supplier)

    # Verify Suppliers manages Supplier objects
    assert suppliers.search_supplier("S001") is supplier

    # Both products are associated with the same supplier
    physical = PhysicalProduct(
        "P001", "Laptop", 1500.00, 10, 2.5, supplier
    )

    digital = DigitalProduct(
        "P002", "Antivirus Software", 50.00, 100, 500.0, supplier
    )

    print("Physical product supplier:")
    physical.display_supplier_information()

    print("\nDigital product supplier:")
    digital.display_supplier_information()

    print("\nSupplier relationship: PASSED")


def test_inventory_aggregation():
    print("\n=== INVENTORY AGGREGATION ===")

    supplier = Supplier("S001", "Tech Supplies", "tech@example.com")

    physical = PhysicalProduct(
        "P001", "Laptop", 1500.00, 10, 2.5, supplier
    )

    digital = DigitalProduct(
        "P002", "Antivirus Software", 50.00, 100, 500.0, supplier
    )

    inventory = Inventory()

    inventory.add_product(physical)
    inventory.add_product(digital)

    # Retrieve products from Inventory
    retrieved_physical = inventory.search_product("P001")
    retrieved_digital = inventory.search_product("P002")

    assert retrieved_physical is physical
    assert retrieved_digital is digital

    print("Physical product successfully added and retrieved.")
    print("Digital product successfully added and retrieved.")

    # Demonstrate that products can exist independently
    another_product = PhysicalProduct(
        "P003", "Keyboard", 80.00, 20, 0.5, supplier
    )

    assert inventory.search_product("P003") is None

    print("Independent product exists outside Inventory.")
    print("Inventory aggregation: PASSED")


def test_order_composition():
    print("\n=== ORDER COMPOSITION ===")

    supplier = Supplier("S001", "Tech Supplies", "tech@example.com")

    physical = PhysicalProduct(
        "P001", "Laptop", 1500.00, 10, 2.5, supplier
    )

    digital = DigitalProduct(
        "P002", "Antivirus Software", 50.00, 100, 500.0, supplier
    )

    order = Order("O001")

    # Add products to the order through OrderLine objects
    order.add_order_line(physical, 2)
    order.add_order_line(digital, 1)

    assert len(order.order_lines) == 2

    # Verify each OrderLine references its Product
    assert order.order_lines[0]._product is physical
    assert order.order_lines[1]._product is digital

    print("Order contains 2 OrderLine objects.")
    print("First OrderLine references the Laptop.")
    print("Second OrderLine references the Antivirus Software.")

    print(f"Order total: ${order.calculate_total():.2f}")

    assert order.calculate_total() == 3050.00

    print("Order composition and Product association: PASSED")


def test_polymorphism_and_lsp():
    print("\n=== POLYMORPHISM AND LSP ===")

    supplier = Supplier("S001", "Tech Supplies", "tech@example.com")

    physical = PhysicalProduct(
        "P001", "Laptop", 1500.00, 10, 2.5, supplier
    )

    digital = DigitalProduct(
        "P002", "Antivirus Software", 50.00, 100, 500.0, supplier
    )

    # Both subclasses are stored in a collection of Product references
    products: list[Product] = [physical, digital]

    for product in products:
        # Both objects can be treated as Product instances
        assert isinstance(product, Product)

        print(f"\nProduct: {product.name}")
        print(f"Price: ${product.price:.2f}")

        # Common inherited/overridden methods work on both subclasses
        product.display_information()

        print(product.get_fulfilment_info())

        product_dict = product.to_dict()
        assert isinstance(product_dict, dict)

    # PhysicalProduct has its own additional functionality
    assert isinstance(physical, CanBeShipped)
    print(f"\nPhysical shipping cost: ${physical.calculate_shipping_cost():.2f}")

    # Both subclasses can be passed into a function
    # that accepts a Product reference.
    def display_fulfilment(product: Product) -> str:
        return product.get_fulfilment_info()

    for product in products:
        print(display_fulfilment(product))

    print("\nPolymorphism and LSP: PASSED")


test_supplier_relationship()
test_inventory_aggregation()
test_order_composition()
test_polymorphism_and_lsp()