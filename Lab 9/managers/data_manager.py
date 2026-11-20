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
        self.__load_messages: list[str] = []

    @property
    def load_messages(self) -> list[str]:
        """Messages from the most recent load_* call (skipped rows, missing files, counts)."""
        return list(self.__load_messages)

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
            pathlib.Path(filename).parent.mkdir(parents=True, exist_ok=True)
            with open(filename, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
        except PermissionError as error:
            raise PermissionError(f"Permission denied when writing to {filename}") from error
        except (csv.Error, OSError) as error:
            raise RuntimeError(f"Unable to save CSV file {filename}") from error

    @staticmethod
    def _describe_error(error: Exception) -> str:
        if isinstance(error, KeyError):
            return f"missing column {error}"
        return str(error)

    # ===== Managing =====
    def load_products(self, suppliers: Suppliers) -> Products:
        """
        Products need their supplier, so suppliers must be loaded first.
        Invalid rows are skipped and reported through load_messages.
        """
        self.__load_messages = []
        products = Products()
        loaded = 0
        try:
            file = open(self.__products_path, newline="")
        except FileNotFoundError:
            self.__load_messages.append(f"Products file not found: {self.__products_path}")
        except PermissionError as error:
            raise PermissionError(f"Permission denied when reading {self.__products_path}") from error
        else:
            with file:
                try:
                    data = list(csv.DictReader(file))
                except csv.Error as error:
                    raise RuntimeError(f"Error reading CSV file {self.__products_path}") from error

            for line_number, row in enumerate(data, start=2):
                try:
                    supplier = suppliers.search_supplier(row["supplier_id"])
                    if supplier is None:
                        raise ValueError(f"Unknown supplier ID: {row['supplier_id']}")
                    weight = float(row["weight"]) if row.get("weight") else None
                    download_size = float(row["download_size"]) if row.get("download_size") else None

                    product = ProductFactory.create(
                        product_type=row["product_type"],
                        product_id=row["product_id"],
                        name=row["name"],
                        price=float(row["price"]),
                        stock_quantity=int(row["stock_quantity"]),
                        supplier=supplier,
                        weight=weight,
                        download_size=download_size,
                    )
                except (ValueError, KeyError, TypeError) as error:
                    self.__load_messages.append(f"Skipping invalid product row {line_number}: {DataManager._describe_error(error)}")
                    continue

                result = products.add_product(product)
                if result == "Product added successfully.":
                    loaded += 1
                else:
                    self.__load_messages.append(f"Skipping product row {line_number}: {result} ({product.product_id})")
            self.__load_messages.append(f"{loaded} products loaded.")
        finally:
            self.__load_messages.append("Load attempt finished.")
        return products

    def save_products(self, products: Products) -> None:
        data = [product.to_csv_dict() for product in products.get_all_products()]
        DataManager.save_csv(self.__products_path, data, ["product_type", "product_id", "name", "price", "stock_quantity", "supplier_id", "weight", "download_size"])

    def load_suppliers(self) -> Suppliers:
        self.__load_messages = []
        if not self.__suppliers_path.exists():
            self.__load_messages.append(f"Suppliers file not found: {self.__suppliers_path}. A new empty file will be created.")

        data = DataManager.read_csv(self.__suppliers_path)
        suppliers = Suppliers()
        for line_number, row in enumerate(data, start=2):
            try:
                supplier = Supplier(row["supplier_id"], row["name"], row["email"])
            except KeyError as error:
                self.__load_messages.append(f"Skipping invalid supplier row {line_number}: {DataManager._describe_error(error)}")
                continue

            result = suppliers.add_supplier(supplier)
            if result != "Supplier added successfully.":
                self.__load_messages.append(f"Skipping supplier row {line_number}: {result} ({supplier.supplier_id})")
        return suppliers

    def save_suppliers(self, suppliers: Suppliers) -> None:
        data = []
        for supplier in suppliers.get_all_suppliers():
            data.append({"supplier_id": supplier.supplier_id, "name": supplier.name, "email": supplier.email})
        DataManager.save_csv(self.__suppliers_path, data, ["supplier_id", "name", "email"])
