number = int(input("Enter a number: "))
if number < 0:
    print("Negative numbers are not allowed.")
else:
    square_root = number ** 0.5
    print("The square root of", number, "is", square_root)