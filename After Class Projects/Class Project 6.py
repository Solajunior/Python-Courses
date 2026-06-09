base = int(input("Enter a number: "))
exponent = int(input("Enter a number: "))
for i in range(base, base**exponent + 1, base):
    print(i)