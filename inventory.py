from product import Product


class Inventory:
    def __init__(self) -> None:
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        if self.find_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def find_product(self, product_id: str) -> Product | None:
        product_id = product_id.strip().upper()
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def search_product(self, product_id: str) -> Product | None:
        return self.find_product(product_id)

    def remove_product(self, product_id: str) -> Product | None:
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    def update_stock(self, product_id: str, quantity: int) -> bool:
        product = self.find_product(product_id)
        if product is None:
            return False
        product.update_stock(quantity)
        return True

    def display_all(self) -> None:
        print("\nCurrent Inventory")
        print("-" * 48)
        if not self.__products:
            print("Inventory is empty.")
        for product in self.__products:
            product.display_information()
        print("-" * 48)

    def get_products(self) -> list[Product]:
        return self.__products.copy()
