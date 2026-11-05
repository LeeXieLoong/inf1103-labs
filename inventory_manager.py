import json
import math

from inventory import Inventory
from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


UNASSIGNED_SUPPLIER = Supplier("UNASSIGNED", "Unassigned supplier", "")


def load_inventory() -> Inventory:
    inventory = Inventory()
    suppliers: dict[str, Supplier] = {
        UNASSIGNED_SUPPLIER.get_supplier_id(): UNASSIGNED_SUPPLIER,
    }
    try:
        with open("inventory.json", "r", encoding="utf-8") as inventory_file:
            records = json.load(inventory_file)
        if not isinstance(records, list):
            raise ValueError("Inventory data must be a list of products.")
        for position, record in enumerate(records, start=1):
            details = (record["id"], record["name"], record["price"], record["stock"])
            supplier = UNASSIGNED_SUPPLIER
            if "supplier" in record:
                saved_supplier = Supplier(**record["supplier"])
                supplier_id = saved_supplier.get_supplier_id()
                supplier = suppliers.setdefault(supplier_id, saved_supplier)
                if supplier.to_dict() != saved_supplier.to_dict():
                    raise ValueError(f"Conflicting details for supplier {supplier_id}.")
            product_type = record.get("type")
            if product_type == "physical":
                product = PhysicalProduct(*details, record["weight"], supplier)
            elif product_type == "digital":
                product = DigitalProduct(*details, record["download_size"], supplier)
            elif "type" not in record:
                # Lab 6 records have no type or additional measurements yet.
                print(
                    f"\nExisting product setup ({position}/{len(records)}): "
                    f"{record['id']} - {record['name']}"
                )
                print("Choose 1 or 2 below, then enter its weight or download size.")
                print("Finish setting up all existing products to reach the main menu.")
                print("Option 5 (Save Inventory) is available in that main menu.")
                product = create_product(*details, supplier)
            else:
                raise ValueError(f"Unknown product type: {product_type!r}")
            if not inventory.add_product(product):
                raise ValueError(f"Duplicate product ID: {record['id']}")
        print("inventory.json found.")
        print("Inventory loaded successfully.")
    except FileNotFoundError:
        print("inventory.json not found. Starting with an empty inventory.")
    return inventory


def save_inventory(inventory: Inventory) -> None:
    records = [product.to_dict() for product in inventory.get_products()]
    with open("inventory.json", "w", encoding="utf-8") as inventory_file:
        json.dump(records, inventory_file, indent=4)
        inventory_file.write("\n")
    print("Inventory saved successfully to inventory.json.")


def get_stock(prompt: str) -> int:
    while True:
        value = input(prompt).strip()
        if value.isdecimal():
            return int(value)
        print("Please enter a non-negative whole number.")


def get_price() -> float:
    while True:
        try:
            price = float(input("Price: ").strip())
            if math.isfinite(price) and price >= 0:
                return price
        except ValueError:
            pass
        print("Please enter a valid non-negative price.")


def get_positive_number(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt).strip())
            if math.isfinite(value) and value > 0:
                return value
        except ValueError:
            pass
        print("Please enter a valid number greater than zero.")


def create_product(
    product_id: str, name: str, price: float, stock: int, supplier: Supplier
) -> Product:
    print("1. Physical product")
    print("2. Digital product")
    while True:
        product_type = input("Choose product type (1 or 2): ").strip()
        if product_type == "1":
            weight = get_positive_number("Weight (kg): ")
            return PhysicalProduct(product_id, name, price, stock, weight, supplier)
        if product_type == "2":
            download_size = get_positive_number("Download size (MB): ")
            return DigitalProduct(product_id, name, price, stock, download_size, supplier)
        print("Invalid product type. Please enter 1 or 2.")


def choose_supplier(inventory: Inventory) -> Supplier:
    supplier_id = input("Supplier ID (Enter if unassigned): ").strip().upper()
    if not supplier_id or supplier_id == UNASSIGNED_SUPPLIER.get_supplier_id():
        return UNASSIGNED_SUPPLIER
    for product in inventory.get_products():
        supplier = product.get_supplier()
        if supplier.get_supplier_id() == supplier_id:
            return supplier

    name = input("Supplier Name: ").strip()
    while not name:
        print("Supplier name cannot be empty.")
        name = input("Supplier Name: ").strip()
    contact_email = input("Supplier Email: ").strip()
    return Supplier(supplier_id, name, contact_email)


def add_product(inventory: Inventory) -> None:
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()
    if not product_id:
        print("Product ID cannot be empty.")
        return
    if inventory.search_product(product_id) is not None:
        print("Product ID already exists.")
        return

    name = input("Product Name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return

    price = get_price()
    stock = get_stock("Stock Quantity: ")
    supplier = choose_supplier(inventory)
    product = create_product(product_id, name, price, stock, supplier)
    inventory.add_product(product)
    print("Product added successfully!")


def update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)
    if product is None:
        print("Product not found.")
        return

    print("\nProduct Found:")
    print("Name:", product.get_name())
    print("Current Stock:", product.get_stock())
    inventory.update_stock(product_id, get_stock("New Stock Quantity: "))
    print("Stock updated successfully!")


def search_product(inventory: Inventory) -> None:
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)
    if product is None:
        print("Product not found.")
        return

    print("\nProduct Found")
    print("-" * 48)
    product.display_information()
    print("-" * 48)


def main() -> None:
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    try:
        inventory = load_inventory()
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Could not load inventory: {error}")
        print("Check inventory.json before running the program again.")
        return

    while True:
        print("\n----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("----------------------------")
        option = input("Enter option: ").strip()

        if option == "1":
            inventory.display_all()
        elif option == "2":
            add_product(inventory)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
        elif option == "5":
            print("\nSaving inventory...")
            save_inventory(inventory)
        elif option == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
