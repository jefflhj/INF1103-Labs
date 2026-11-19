"""
    All file interaction occurs here.
"""

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
        try:
            with open(filename, "r", newline="") as file:
                reader = csv.DictReader(file)
                return list(reader)
        except FileNotFoundError:
            pathlib.Path(filename).touch()
            return []
        except PermissionError as error:
            raise PermissionError(f"Permission denied when reading {filename}") from error
        except csv.Error as error:
            raise RuntimeError(f"Error reading CSV file {filename}") from error
        except OSError as error:
            raise OSError(f"Unable to access file {filename}") from error

    @staticmethod
    def save_csv(filename: str, data: list[dict], fieldnames: list[str]) -> None:
        try:
            with open(filename, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
        except PermissionError as error:
            raise PermissionError(f"Permission denied when writing to {filename}") from error
        except (csv.Error, OSError) as error:
            raise RuntimeError(f"Unable to save CSV file {filename}") from error

    # ===== Managing =====
    def load_products(self) -> Products:
        data = DataManager.read_csv(self.__products_path)
        products = Products()
        for row in data:
            weight = float(row["weight"]) if row["weight"] else None
            download_size = float(row["download_size"]) if row["download_size"] else None

            product = ProductFactory.create(product_type=row["product_type"], product_id=row["product_id"], name=row["name"], price=row["price"], stock_quantity=row["stock_quantity"], supplier=Suppliers.search_supplier(row["supplier_id"], weight=weight, download_size=download_size))
            products.add_product(product)
        return products

    def save_products(self, products: Products) -> None:
        data = [product.to_csv_dict() for product in products.get_all_products()]
        DataManager.save_csv(self.__products_path, data, ["product_type", "product_id", "name", "price", "stock_quantity", "supplier_id", "weight", "download_size"])

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
