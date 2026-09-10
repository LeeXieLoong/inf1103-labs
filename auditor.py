inventory = 0
failedEntry = 0

while True:
    user = input("Enter a stock quantity: ")

    if user == "quit":
        print("Total Units Processed: " , inventory)
        print("Total Failed Entries: " , failedEntry)
        break
    if user.isdigit():
        validinventory = int(user)
        inventory += validinventory
    elif user.startswith("-"):
        print("Invalid input, please put in a posititve number.")
        failedEntry += 1
    else:
        print("Invalid input, please put a number and not spelled in text.")
        failedEntry += 1
    if inventory > 500:
        print("OVER 500 UNITS!!")
        break

    

    




