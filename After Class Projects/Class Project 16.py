choice = input("Enter cos, sin or tan: ")
if choice == "cos":
    opposite = float(input("Enter the length of the opposite side: "))
    hypotenuse = float(input("Enter the length of the hypotenuse side: "))
    cos = opposite / hypotenuse
    print("The cosine of the angle is:", cos)
elif choice == "sin":
    adjacent = float(input("Enter the length of the adjacent side: "))
    hypotenuse = float(input("Enter the length of the hypotenuse side: "))
    sin = adjacent / hypotenuse
    print("The sine of the angle is", sin)
elif choice == "tan":
    opposite = float(input("Enter the length of the opposite side: "))
    adjacent = float(input("Enter the length of the adjacent side: "))
    tan = opposite / adjacent
    print("The tangent of the angle is", tan)
else:
    print("Invalid choice!")