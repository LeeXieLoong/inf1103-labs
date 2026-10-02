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


def save_inventory(inventory):
    with open("inventory.json", "w", encoding="utf-8") as inventory_file:
        json.dump(inventory, inventory_file, indent=4)
        inventory_file.write("\n")
    print("Inventory saved successfully to inventory.json.")


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
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    inventory = load_inventory()

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
            display_all(inventory)
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
