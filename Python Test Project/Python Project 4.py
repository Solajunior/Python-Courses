class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def get_info(self):
        return f"{self.title} by {self.author}, published in {self.year}"

    def borrow(self):
        self.is_borrowed = True
        print(f"{self.title} has been borrowed.")

    def return_book(self):
        self.is_borrowed = False
        print(f"{self.title} has been returned.")

book1 = Book("To Kill A Mockingbird", "Harper Lee", 1960)
book2 = Book("1984", "George Orwell", 1948)
book3 = Book("The Great Gatsby", "F. Scott Fitzgerald", 1925)
book4 = Book("Top 100 Roblox Games", "Roblox Corporation", 2026)
book5 = Book("Safety Rules On Roblox", "Roblox Corporation", 2025)
user_input = input("Press (1/2/3/4/5) to borrow a book: ")
if user_input == "1":
    book1.borrow()
elif user_input == "2":
    book2.borrow()
elif user_input == "3":
    book3.borrow()
elif user_input == "4":
    book4.borrow()
elif user_input == "5":
    book5.borrow()
user_input2 = input("Press (1/2/3/4/5) to return a book: ")
if user_input2 == "1":
    book1.return_book()
elif user_input2 == "2":
    book2.return_book()
elif user_input2 == "3":
    book3.return_book()
elif user_input2 == "4":
    book4.return_book()
elif user_input2 == "5":
    book5.return_book()