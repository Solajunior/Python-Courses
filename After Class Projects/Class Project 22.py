print("Welcome to my library!")
books_avaliable = ["The Wonders Of Nature", "A Guide To Python", "How To Play Chess", "How To Play Roblox", "Top 100 Games Of All Time"]
chosen_book = input("What book would you like to borrow? ")
book_prices = [14, 35, 50, 12, 85]
if chosen_book not in books_avaliable:
    print(chosen_book, "is not available! Stopping the checker.")
    exit()
else:
    print(chosen_book, "is available!")
    buy_book = input("Would you like to buy this book? (yes/no) ")
    if buy_book == "yes":
        print("Great! The price of", chosen_book, "is $", book_prices[books_avaliable.index(chosen_book)])
        input("Would you like to borrow another book? (yes/no)")
    if buy_book == "no":
        print("If you don't want to read this, you can choose another one!") 
    else:
        print("Invalid input.")
        