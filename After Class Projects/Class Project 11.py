while True:

    number = float(input("Enter a decimal number: "))

    for i in range(1):  # Nested loop
        whole_number = int(number)

    print("Whole number =", whole_number)

    choice = input("Continue? (y/n): ").lower()

    if choice != "y":
        break