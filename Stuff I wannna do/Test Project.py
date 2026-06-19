secret = 15
hearts = 5
while hearts > 0:
    guess = int(input("Guess the secret number: "))
    if guess == secret:
        print("Congratulations! You guessed the secret number!")
        break
else:
    print("Sorry, that's wrong. Try again!")
    hearts -= 1
    print(f"You have {hearts} hearts left.")
if hearts == 0:
    print("Game over!")