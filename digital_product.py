import math

from product import Product, ProductRecord
from supplier import Supplier


class DigitalProduct(Product):
    def __init__(
        self, product_id: str, name: str, price: float, stock: int,
        download_size: float, supplier: Supplier,
    ) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if not math.isfinite(download_size) or download_size <= 0:
            raise ValueError("Download size must be a positive number in megabytes.")
        self.__download_size: float = download_size

    def get_download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"Type: Digital | Download size: {self.__download_size:g} MB")
        print(self.get_fulfilment_info())

    def get_fulfilment_info(self) -> str:
        return "Delivered digitally by download."

    def to_dict(self) -> ProductRecord:
        record = super().to_dict()
        record["type"] = "digital"
        record["download_size"] = self.__download_size
        return record
