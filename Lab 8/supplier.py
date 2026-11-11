

class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self._supplier_id = supplier_id
        self._name = name
        self._contact_email = contact_email

    def display_information(self):
        print(f"ID: {self._supplier_id}")
        print(f"Name: {self._name}")
        print(f"Email: ${self._contact_email}")

