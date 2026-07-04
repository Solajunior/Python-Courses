try:
    age = int(input("Please enter your age: "))
except ValueError:
    print("Invalid input!")
else:
    if age <= 0:
        print("Invalid age!")
    else:
        if age % 2 == 0:
            print("Your age is even.")
        else:
            print("Your age is odd.")