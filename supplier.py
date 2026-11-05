class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        if not supplier_id.strip() or not name.strip():
            raise ValueError("Supplier ID and name cannot be empty.")
        self.__supplier_id: str = supplier_id.strip().upper()
        self.__name: str = name.strip()
        self.__contact_email: str = contact_email.strip()

    def get_supplier_id(self) -> str:
        return self.__supplier_id

    def display_information(self) -> None:
        print(f"Supplier: {self.__name} ({self.__supplier_id})")
        if self.__contact_email:
            print(f"Supplier email: {self.__contact_email}")

    def to_dict(self) -> dict[str, str]:
        return {
            "supplier_id": self.__supplier_id,
            "name": self.__name,
            "contact_email": self.__contact_email,
        }
