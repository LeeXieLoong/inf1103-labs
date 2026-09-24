import json


def load_inventory():
    try:
        with open("inventory.txt", "r", encoding="utf-8") as inventory_file:
            data = json.load(inventory_file)
        return data["total"], data["history"]
    except FileNotFoundError:
        return 0, []


def get_valid_input():
    user = input("Enter a stock quantity: ").strip().lower()

    if user == "quit":
        return "quit"

    if user.isdecimal():
        return int(user)
    elif user.startswith("-"):
        print("Invalid input, please enter a non-negative number.")
    else:
        print("Invalid input, please enter a whole number.")
    return "invalid"


def process_delivery(current_total, new_value):
    return current_total + new_value


def calculate_tax(amount):
    return amount * 0.10


def generate_report(total_deliveries, failed_attempts):
    print("Total Deliveries Processed:", total_deliveries)
    print("Total Failed Entries:", failed_attempts)


def main():
    inventory, history = load_inventory()
    failed_entry = 0
    deliveries_processed = 0
    total_tax = 0.0

    print("Current inventory:", inventory)
    print("Transaction history:", history)

    while True:
        result = get_valid_input()

        if result == "invalid":
            failed_entry += 1
        elif result == "quit":
            break
        else:
            inventory = process_delivery(inventory, result)
            history.append(result)
            total_tax += calculate_tax(result)
            deliveries_processed += 1
            print("Delivery Processed!")
            if inventory > 500:
                print("OVER 500 UNITS!!")
                break

    generate_report(deliveries_processed, failed_entry)
    print("Total Units Processed:", inventory)
    print("Transaction history:", history)
    print("Tax for this session:", format(total_tax, ".2f"))


if __name__ == "__main__":
    main()
