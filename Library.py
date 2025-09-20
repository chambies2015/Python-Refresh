from datetime import datetime, timedelta

class Library():
    def __init__(self):
        self.books = {}

    def add_book(self, book):
        self.books[book.name] = book

    def describe(self, name):
        book = self.books.get(name)
        book.describe(book)

    def list_books(self):
        for book in self.books.values():
            self.describe(book.name)

    def checkout_book(self, name, patron, days=14):
        if self.books.get(name):
            book = self.books.get(name)
            if patron.current_loans < patron.max_loans:
                if book and book.is_checked_out == "Available":
                    book.toggle_checkout_true()
                    print(f"{book.name} by {book.author} checked out successfully by {patron.name}.")
                    patron.borrow_book(book)
                else:
                    print("Book unavailable.")
            else:
                print(f"{patron.name} has max number of borrowed books checked out: {patron.max_loans}")
        else:
            print("Book does not exist in our system.")

    def return_book(self, name, patron):
        if name in self.books and name in patron.borrowed_books:
            book = self.books.get(name)
            patron_books = patron.borrowed_books
            if book.name in patron_books:
                book.toggle_checkout_false()
                print(f"{book.name} by {book.author} checked in successfully.")
                patron.return_book(book)
            else:
                print(f"{patron.name} has not checked out {book.name} by {book.author}")
        else:
            print(f"{name} is not in our catalog")

class Book():
    def __init__(self, name, author, is_checked_out="Available"):
        self.name = name
        self.author = author
        self.is_checked_out = is_checked_out

    def toggle_checkout_true(self):
        self.is_checked_out = "Checked Out"

    def toggle_checkout_false(self):
        self.is_checked_out = "Available"

    def describe(self, book):
        print(f"{book.name} by {book.author} - {book.is_checked_out}")

class PhysicalBook(Book):
    def __init__(self, name, author, shelf_location, is_checked_out="Available"):
        super().__init__(name, author, is_checked_out)
        self.shelf_location = shelf_location

    def describe(self, book):
        print(f"{book.name} by {book.author} - Shelf: {book.shelf_location} - {book.is_checked_out}")

class EBook(Book):
    def __init__(self, name, author, file_size_mb, is_checked_out="Available"):
        super().__init__(name, author, is_checked_out)
        self.file_size_mb = file_size_mb

    def describe(self, book):
        print(f"{book.name} by {book.author} - Size: {book.file_size_mb}mb - {book.is_checked_out}")

class Patron():
    def __init__(self, name, max_loans):
        self.name = name
        self.borrowed_books = {}
        self.current_loans = 0
        self.max_loans = max_loans

    def borrow_book(self, book):

        self.borrowed_books[book.name] = book
        self.current_loans += 1


    def return_book(self, book):

        self.borrowed_books.pop(book.name)
        self.current_loans -= 1

    def list_loans(self):
        print(f"{self.name} currently has {self.current_loans} books checked out of a max of {self.max_loans}.")

if __name__ == "__main__":
    library = Library()
    alice = Patron("Alice", max_loans=2)
    bob = Patron("Bob", max_loans=2)

    # Inventory
    library.add_book(PhysicalBook("The Hobbit", "J.R.R. Tolkien", shelf_location="A3"))
    library.add_book(EBook("1984", "George Orwell", file_size_mb=2.5))

    print("\n--- Inventory ---")
    library.list_books()

    # Checkouts with due dates
    print("\n--- Checkouts ---")
    library.checkout_book("1984", alice, days=7)      # should succeed
    library.checkout_book("1984", bob)                # should fail (already checked out)
    library.checkout_book("The Hobbit", alice)        # should succeed
    library.checkout_book("The Hobbit", alice)        # should fail (already checked out or at limit)

    # Show patron state
    print("\n--- Alice Loans ---")
    alice.list_loans()  # implement however you like

    # Returns
    print("\n--- Returns ---")
    library.return_book("1984", alice)                # should clear borrower/due date
    library.return_book("1984", bob)                  # should warn: bob didn't borrow it

    print("\n--- Final Inventory ---")
    library.list_books()

