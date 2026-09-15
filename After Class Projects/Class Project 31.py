class Book:
	def __init__(self, title, author):
		self.title = title.strip()
		self.author = author.strip()
		self.is_borrowed = False
		self.borrowed_by = ""

	def status(self):
		if self.is_borrowed:
			return f"Borrowed by {self.borrowed_by}"
		return "Available"


class Library:
	def __init__(self):
		self.books = [
			Book("The Secret Garden", "Frances Hodgson Burnett"),
			Book("The Hobbit", "J. R. R. Tolkien"),
			Book("Charlotte's Web", "E. B. White"),
		]

	def list_books(self, books=None):
		books = self.books if books is None else books
		if not books:
			print("No books found.")
			return

		print("\nLibrary books")
		print("-------------")
		for number, book in enumerate(books, start=1):
			print(f"{number}. {book.title} by {book.author} - {book.status()}")

	def search_books(self, search_term):
		search_term = search_term.lower()
		return [
			book
			for book in self.books
			if search_term in book.title.lower()
			or search_term in book.author.lower()
		]

	def add_book(self, title, author):
		if not title.strip() or not author.strip():
			return "Title and author cannot be empty."
		self.books.append(Book(title, author))
		return f'"{title.strip()}" was added to the library.'

	def borrow_book(self, title, member_name):
		book = self.find_book(title)
		if book is None:
			return "That book is not in the library."
		if book.is_borrowed:
			return f'"{book.title}" is already borrowed by {book.borrowed_by}.'
		if not member_name.strip():
			return "Member name cannot be empty."

		book.is_borrowed = True
		book.borrowed_by = member_name.strip()
		return f'"{book.title}" was borrowed by {book.borrowed_by}.'

	def return_book(self, title):
		book = self.find_book(title)
		if book is None:
			return "That book is not in the library."
		if not book.is_borrowed:
			return f'"{book.title}" is already available.'

		book.is_borrowed = False
		book.borrowed_by = ""
		return f'"{book.title}" was returned successfully.'

	def find_book(self, title):
		title = title.lower().strip()
		return next((book for book in self.books if book.title.lower() == title), None)


def get_book_title():
	return input("Enter the exact book title: ").strip()


def run_library_system():
	library = Library()
	print("LIBRARY SYSTEM")
	print("==============")

	while True:
		print("\n1. View all books")
		print("2. Search for a book")
		print("3. Add a book")
		print("4. Borrow a book")
		print("5. Return a book")
		print("6. Exit")
		choice = input("Choose an option: ").strip()

		if choice == "1":
			library.list_books()
		elif choice == "2":
			search_term = input("Search by title or author: ").strip()
			library.list_books(library.search_books(search_term))
		elif choice == "3":
			title = input("Book title: ").strip()
			author = input("Author: ").strip()
			print(library.add_book(title, author))
		elif choice == "4":
			title = get_book_title()
			member_name = input("Member name: ").strip()
			print(library.borrow_book(title, member_name))
		elif choice == "5":
			print(library.return_book(get_book_title()))
		elif choice == "6":
			print("Library system closed. Goodbye!")
			break
		else:
			print("Invalid option. Please choose 1-6.")


if __name__ == "__main__":
	run_library_system()
