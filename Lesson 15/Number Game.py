import random
Playing = True
number = str(random.randint(1, 20))
print("I will generate a number from 1 to 20, and you have to guess the number one digit at a time.")
print("The game ends when you get 1 hero!")
while Playing:
    guess = input("Give me your best guess! \n")
    if number == guess:
        print("You win!")
        print("The number was", number)
        break
    else:
        print("Your guess isn't quite right, try again. \n")