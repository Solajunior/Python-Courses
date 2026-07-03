bill = 0
print("How much do you want to order?")
i = int(input("Please enter the amount of items you want to order: "))
print("1. Rice - $4.50")
print("2. Pizza - $6.00 for a full pizza")
print("3. Chicken - $3.00 for 1 piece")
while i > 0:
    choice = int(input("Please enter your choice (1/2/3): "))
    if choice == 1:
        print("You have ordered rice.")
        i -= 1
        bill += 4.50
    elif choice == 2:
        print("You have ordered pizza.")
        i -= 1
        bill += 6.00
    elif choice == 3:
        print("You have ordered chicken.")
        i -= 1
        bill += 3.00
    else:
        print("Invalid input.")
print("Your total bill is: $", bill)