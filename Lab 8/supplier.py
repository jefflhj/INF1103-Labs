

class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self._supplier_id = supplier_id
        self._name = name
        self._contact_email = contact_email

    def display_information(self) -> None:
        print(f"ID: {self._supplier_id}")
        print(f"Name: {self._name}")
        print(f"Email: {self._contact_email}")

    def to_dict(self) -> dict:
        return {
            "supplier_id": self._supplier_id,
            "name": self._name,
            "contact_email": self._contact_email
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            supplier_id=data["supplier_id"],
            name=data["name"],
            contact_email=data["contact_email"]
        )

    @property
    def supplier_id(self):
        return self._supplier_id

