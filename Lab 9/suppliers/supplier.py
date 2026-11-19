"""
    This creates supplier objects.
"""


class Supplier:
    def __init__(self, supplier_id: str, name: str, email: str):
        self._supplier_id = supplier_id
        self._name = name
        self._email = email

    def display_information(self) -> None:
        print(f"ID: {self._supplier_id}")
        print(f"Name: {self._name}")
        print(f"Email: {self._email}")

    @property
    def supplier_id(self):
        return self._supplier_id

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email
