"""
    This is like inventory, it just stores all suppliers.
    DataManager will read from and save to suppliers.csv.
"""

from suppliers.supplier import Supplier


class Suppliers():
    def __init__(self):
        self._suppliers = {}

    def add_supplier(self, supplier: Supplier) -> str:
        if supplier.supplier_id in self._suppliers:
            return "Supplier already exists."
        else:
            self._suppliers[supplier.supplier_id] = supplier
            return "Supplier added successfully."

    def remove_supplier(self, supplier_id: str) -> str:
        if supplier_id not in self._suppliers:
            return "Supplier does not exist."
        else:
            del self._suppliers[supplier_id]
            return "Supplier removed successfully."
    
    def search_supplier(self, supplier_id: str) -> Supplier | None:
        if supplier_id not in self._suppliers:
            return None
        else:
            return self._suppliers[supplier_id]

    def get_all_suppliers(self) -> list[Supplier]:
        return list(self._suppliers.values())
