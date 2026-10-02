import json
import math


def load_inventory():
    try:
        with open("inventory.json", "r", encoding="utf-8") as inventory_file:
            inventory = json.load(inventory_file)
        print("inventory.json found.")
        print("Inventory loaded successfully.")
        return inventory
    except FileNotFoundError:
        print("inventory.json not found. Starting with an empty inventory.")
        return []


def find_product(inventory, product_id):
    for product in inventory:
        if product["id"].upper() == product_id.upper():
            return product
    return None


def get_stock(prompt):
    while True:
        value = input(prompt).strip()
        if value.isdecimal():
            return int(value)
        print("Please enter a non-negative whole number.")


def get_price():
    while True:
        try:
            price = float(input("Price: ").strip())
            if math.isfinite(price) and price >= 0:
                return price
        except ValueError:
            pass
        print("Please enter a valid non-negative price.")


def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()
    if not product_id:
        print("Product ID cannot be empty.")
        return
    if find_product(inventory, product_id) is not None:
        print("Product ID already exists.")
        return

    name = input("Product Name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return

    price = get_price()
    stock = get_stock("Stock Quantity: ")
    product = {"id": product_id, "name": name, "price": price, "stock": stock}
    inventory.append(product)
    print("Product added successfully!")


def update_stock(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = find_product(inventory, product_id)
    if product is None:
        print("Product not found.")
        return

    print("\nProduct Found:")
    print("Name:", product["name"])
    print("Current Stock:", product["stock"])
    product["stock"] = get_stock("New Stock Quantity: ")
    print("Stock updated successfully!")


def search_product(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    product = find_product(inventory, product_id)
    if product is None:
        print("Product not found.")
        return

    print("\nProduct Found")
    print("-" * 48)
    print("ID:", product["id"])
    print("Name:", product["name"])
    print(f"Price: ${product['price']:.2f}")
    print("Stock:", product["stock"])
    print("-" * 48)


def display_all(inventory):
    print("\nCurrent Inventory")
    print("-" * 48)
    if not inventory:
        print("Inventory is empty.")
    for product in inventory:
        print(
            f"ID: {product['id']} | Name: {product['name']} | "
            f"Price: ${product['price']:.2f} | Stock: {product['stock']}"
        )
    print("-" * 48)


def main():
    inventory = load_inventory()
    display_all(inventory)


if __name__ == "__main__":
    main()
