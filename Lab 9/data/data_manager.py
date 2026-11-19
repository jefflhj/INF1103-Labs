import csv
import pathlib
import os

from suppliers.suppliers import Suppliers
from suppliers.supplier import Supplier
from products.products import Products
from products.product_factory import ProductFactory

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent


class DataManager:
    def __init__(self):
        self.__suppliers_path = pathlib.Path(os.getenv("SUPPLIERS", str(BASE_DIR / "data" / "suppliers.csv")))
        self.__products_path = pathlib.Path(os.getenv("PRODUCTS", str(BASE_DIR / "data" / "products.csv")))

    # ===== Helpers =====
    @staticmethod
    def read_csv(filename: str) -> list[dict]:
        with open(filename, "r", newline="") as file:
            reader = csv.DictReader(file)
            return list(reader)

    @staticmethod
    def save_csv(filename: str, data: list[dict], fieldnames: list[str]) -> None:
        with open(filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    # ===== Managing =====
    def load_products(self) -> Products:
        data = DataManager.read_csv(self.__products_path)
        products = Products()
        for row in data:
            product = ProductFactory.create(row["product_type"], row["product_id"], row["name"], row["price"], row["stock_quantity"], Suppliers.search_supplier(row["supplier_id"]))
            products.add_product(product)
        return products

    def save_products(self, products: Products) -> None:
        data = []
        for product in products.get_all_products():
            data.append({"product_type": product.product_type, "product_id": product.product_id, "name": product.name, "price": product.price, "stock_quantity": product.stock_quantity, "supplier_id": product.supplier_id})
        DataManager.save_csv(self.__products_path, data, ["product_type", "product_id", "name", "price", "stock_quantity", "supplier_id"])

    def load_suppliers(self) -> Suppliers:
        data = DataManager.read_csv(self.__suppliers_path)
        suppliers = Suppliers()
        for row in data:
            supplier = Supplier(row["supplier_id"], row["name"], row["email"])
            suppliers.add_supplier(supplier)
        return suppliers

    def save_suppliers(self, suppliers: Suppliers) -> None:
        data = []
        for supplier in suppliers.get_all_suppliers():
            data.append({"supplier_id": supplier.supplier_id, "name": supplier.name, "email": supplier.email})
        DataManager.save_csv(self.__suppliers_path, data, ["supplier_id", "name", "email"])
