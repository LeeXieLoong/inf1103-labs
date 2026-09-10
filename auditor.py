inventory = int(0)

while True:
    user = input("Enter a stock quantity: ")

    if user == "quit":
        break
    if user.isdigit():
        validinventory = int(user)
        inventory += validinventory
    elif user.startswith("-"):
        print("Invalid input, please put in a posititve number.")
    else:
        print("Invalid input, please put a number and not spelled in text.")
    if inventory > 500:
        print("OVER 500 UNITS!!")
        break

    

    




