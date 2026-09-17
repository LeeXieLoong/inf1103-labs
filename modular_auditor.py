def get_valid_input():
    user = input("Enter a stock quantity: ").strip().lower()

    if user == "quit":
        return "quit"

    if user.isdigit():
        return int(user)
    elif user.startswith("-"):
        print("Invalid input, please enter a positive number.")
        return "invalid"
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





    

    




