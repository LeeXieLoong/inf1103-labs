inventory = 0
failedEntry = 0
deliveries_processed = 0

def get_valid_input():
    user = input("Enter a stock quantity: ").strip().lower()

    if user == "quit":
        return "quit"
    
    if inventory > 500:
        print("OVER 500 UNITS!!")
        return "over500"
    
    if user.isdigit():
        return int(user)   
    elif user.startswith("-"):
        print("Invalid input, please put in a posititve number.")
        return "invalid"
    else:
        print("Invalid input, please put a number and not spelled in text.")
        return "invalid"
        
def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(amount):
    return amount * 0.10

def generate_report(total_units, failed_attempts):
    print("Total Units Processed:", total_units)
    print("Total Failed Entries:", failed_attempts)

while True:
    result = get_valid_input()

    if result == "invalid":
        failedEntry += 1
    elif result =="quit":
        break
    elif result =="over500":
        print("OVER 500 UNITS!!")

    else:
        delivery_amount = result
        inventory = process_delivery(inventory, delivery_amount)
        tax = calculate_tax(delivery_amount)
        deliveries_processed += 1
        print("Delivery Processed!")

generate_report(deliveries_processed, failedEntry)



    

    




