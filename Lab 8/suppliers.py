from supplier import Supplier


class Suppliers:
    def __init__(self):
        self.__suppliers: dict[str, Supplier] = {}

    def add_supplier(self, supplier: Supplier) -> None: # adds supplier to dict or prints exists message
        if supplier.supplier_id in self.__suppliers:
            print(f"{supplier.supplier_id} - {supplier.name} already exists in the Suppliers Database, it will not be added.")
        else:
            self.__suppliers[supplier.supplier_id] = supplier

    def remove_supplier(self, supplier: Supplier) -> None:
        if supplier.supplier_id in self.__suppliers:
            del self.__suppliers[supplier.supplier_id]
        else:
            print(f"{supplier.__suppliers} - {supplier.name} does not exists in the Suppliers Database, nothing happened.")

    def search_supplier(self, supplier_id: str) -> dict | None:
        for _, details in self.__products.items():
            if supplier_id in details:
                return details[supplier_id] # returns a dict version of supplier object
        return None

    def to_dict(self) -> dict[str, dict]: # returns dict of dicts of suppliers
        return {
            supplier_id: supplier.to_dict()
            for supplier_id, supplier in self.__suppliers.items()
        }

    