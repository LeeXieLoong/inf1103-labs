import math

from product import Product


class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        if not math.isfinite(download_size) or download_size <= 0:
            raise ValueError("Download size must be a positive number in megabytes.")
        self.__download_size = download_size

    def get_download_size(self):
        return self.__download_size

    def display_information(self):
        super().display_information()
        print(f"Type: Digital | Download size: {self.__download_size:g} MB")
        print(self.get_fulfilment_info())

    def get_fulfilment_info(self):
        return "Delivered digitally by download."

    def to_dict(self):
        record = super().to_dict()
        record["type"] = "digital"
        record["download_size"] = self.__download_size
        return record
