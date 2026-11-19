"""
    This is like inventory, it just stores all suppliers.
    DataManager will read from and save to suppliers.csv.
"""

from suppliers.supplier import Supplier


class Suppliers():
    def __init__(self):
        self._suppliers = {}

    def add_supplier(supplier: Supplier) -> None:
        pass

    def remove_supplier():
        pass
    
    def search_supplier():
        pass

    def get_all_suppliers(self) -> list[Supplier]:
        return list(self._suppliers.values())
