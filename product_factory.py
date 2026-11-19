from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


class ProductFactory:
    @staticmethod
    def create(
        product_type: str, product_id: str, name: str, price: float,
        stock_quantity: int, supplier: Supplier, weight: float | None = None,
        download_size: float | None = None,
    ) -> Product:
        if product_type == "physical":
            if weight is None:
                raise ValueError("Physical products require a weight in kilograms.")
            return PhysicalProduct(
                product_id, name, price, stock_quantity, weight, supplier
            )
        if product_type == "digital":
            if download_size is None:
                raise ValueError("Digital products require a download size in megabytes.")
            return DigitalProduct(
                product_id, name, price, stock_quantity, download_size, supplier
            )
        raise ValueError(f"Unknown product type: {product_type}")
