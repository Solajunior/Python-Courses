medical=input("Did you have a medical cause? (Y/N): ").strip().upper()

if medical == 'Y':
    print("You are allowed")
else:
    atten=int(input("Enter the attendance of the student: "))
    if atten > 74:
        print("Allowed")
    else:
        print("Not Allowed")