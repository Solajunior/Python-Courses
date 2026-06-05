string = input("Please enter your own string : ")

string2 = ('')
for i in string:
    string2 = i + string2

    print("\nThe original string is : ", string)
    print("The reversed string is : ", string2)