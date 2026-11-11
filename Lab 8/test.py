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
    supplier = Supplier("S001", "Tech Supplies", "tech@example.com")

    suppliers = Suppliers()
    suppliers.add_supplier(supplier)

    assert suppliers.search_supplier("S001") is supplier # suppliers manages Supplier objects

    physical = PhysicalProduct("P001", "Laptop", 1500.00, 10, 2.5, supplier) # same supplier
    digital = DigitalProduct("P002", "Antivirus Software", 50.00, 100, 500.0, supplier) # same supplier

    print("Physical product supplier:")
    physical.display_supplier_information()

    print("\nDigital product supplier:")
    digital.display_supplier_information()

    print("\nSupplier relationship: OK")


def test_inventory_aggregation():
    supplier = Supplier("S001", "Tech Supplies", "tech@example.com")
    physical = PhysicalProduct("P001", "Laptop", 1500.00, 10, 2.5, supplier)
    digital = DigitalProduct("P002", "Antivirus Software", 50.00, 100, 500.0, supplier)

    inventory = Inventory()

    inventory.add_product(physical)
    inventory.add_product(digital)

    retrieved_physical = inventory.search_product("P001") # from inventory
    retrieved_digital = inventory.search_product("P002") # from inventory

    assert retrieved_physical is physical
    assert retrieved_digital is digital

    print("Physical and Digital products added and retrieved.")

    another_product = PhysicalProduct("P003", "Keyboard", 80.00, 20, 0.5, supplier) # exist independently

    assert inventory.search_product("P003") is None

    print("\nInventory aggregation: OK")


def test_order_composition():
    supplier = Supplier("S001", "Tech Supplies", "tech@example.com")
    physical = PhysicalProduct("P001", "Laptop", 1500.00, 10, 2.5, supplier)
    digital = DigitalProduct("P002", "Antivirus Software", 50.00, 100, 500.0, supplier)
    order = Order("O001")

    order.add_order_line(physical, 2)
    order.add_order_line(digital, 1)

    assert len(order.order_lines) == 2

    assert order.order_lines[0]._product is physical
    assert order.order_lines[1]._product is digital

    print("Order contains 2 OrderLine objects.")
    print("First OrderLine references the Laptop.")
    print("Second OrderLine references the Antivirus Software.")

    print(f"\nOrder total: ${order.calculate_total():.2f}")

    assert order.calculate_total() == 3050.00

    print("\nOrder composition and Product association: OK")


def test_polymorphism_and_lsp():
    supplier = Supplier("S001", "Tech Supplies", "tech@example.com")
    physical = PhysicalProduct("P001", "Laptop", 1500.00, 10, 2.5, supplier)
    digital = DigitalProduct("P002", "Antivirus Software", 50.00, 100, 500.0, supplier)

    products: list[Product] = [physical, digital]

    for product in products:
        assert isinstance(product, Product)

        print(f"\nProduct: {product.name}")
        print(f"Price: ${product.price:.2f}")

        product.display_information()

        print(product.get_fulfilment_info())

        product_dict = product.to_dict()
        assert isinstance(product_dict, dict)

    # PhysicalProduct has its own additional functionality
    assert isinstance(physical, CanBeShipped)
    print(f"\nPhysical shipping cost: ${physical.calculate_shipping_cost():.2f}")

    # Both subclasses can be passed into a function that accepts a Product reference.
    def display_fulfilment(product: Product) -> str:
        return product.get_fulfilment_info()

    for product in products:
        print(display_fulfilment(product))

    print("\nPolymorphism and LSP: OK")


test_supplier_relationship()
test_inventory_aggregation()
test_order_composition()
test_polymorphism_and_lsp()
