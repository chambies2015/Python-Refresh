from datetime import datetime, timedelta

class Library():
    def __init__(self):
        self.books = {}

    def add_book(self, book):
        self.books[(book.name, book.copy_id)] = book

    def get_book(self, name, copy_id):
        return self.books.get((name, copy_id))

    def describe(self, name, copy_id):
        book = self.get_book(name, copy_id)
        if book:
            book.describe()
        else:
            print(f"No copy {copy_id} of {name} found.")

    def list_books(self):
        for book in self.books.values():
            book.describe()

    def search(self, search_term):
        found_books = []
        for book in self.books.values():
            if search_term.lower() in book.name.lower():
                found_books.append(book)
        if  len(found_books) > 0:
            print(f"{len(found_books)} books found in our system with search term: {search_term}")
            for book in found_books:
                book.describe()

    def internal_available_search(self, search_term):
        found_books = []
        for book in self.books.values():
            if (search_term.lower() in book.name.lower()) and book.is_checked_out == "Available":
                found_books.append(book)
        if len(found_books) > 0:
            return found_books

    def internal_checked_out_search(self, search_term):
        found_books = []
        for book in self.books.values():
            if (search_term.lower() in book.name.lower()) and book.is_checked_out == "Checked Out":
                found_books.append(book)
        if len(found_books) > 0:
            return found_books
    def checkout_book(self, name, patron, days=14):
        results = self.internal_available_search(name)
        if (results != None) and (len(results) > 0):
            book = results[0]
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
            print("Book is not available.")

    def return_book(self, name, patron):
        results = self.internal_checked_out_search(name)
        if not results:
            print(f"No copies of {name} are currently checked out in the library.")
            return
        patron_copies = [
            book for book in results
            if (book.name, book.copy_id) in patron.borrowed_books
        ]
        if not patron_copies:
            print(f"{patron.name} has no copies of {name} to return.")
            return
        book = patron_copies[0]
        book.toggle_checkout_false()
        patron.return_book(book)
        print(f"{book.name} by {book.author} (Copy ID {book.copy_id}) returned successfully by {patron.name}.")

class Book():
    def __init__(self, name, author, copy_id: int, is_checked_out="Available"):
        self.name = name
        self.author = author
        self.is_checked_out = is_checked_out
        self.copy_id = copy_id

    def toggle_checkout_true(self):
        self.is_checked_out = "Checked Out"

    def toggle_checkout_false(self):
        self.is_checked_out = "Available"

    def describe(self):
        print(f"{self.name} by {self.author}, Copy ID: {self.copy_id} - {self.is_checked_out}")

class PhysicalBook(Book):
    def __init__(self, name, author, shelf_location, copy_id: int, is_checked_out="Available"):
        super().__init__(name, author, copy_id, is_checked_out)
        self.shelf_location = shelf_location

    def describe(self):
        print(f"{self.name} by {self.author} - Shelf: {self.shelf_location}, Copy ID: {self.copy_id} - {self.is_checked_out}")

class EBook(Book):
    def __init__(self, name, author, file_size_mb, copy_id: int, is_checked_out="Available"):
        super().__init__(name, author, copy_id, is_checked_out)
        self.file_size_mb = file_size_mb

    def describe(self):
        print(f"{self.name} by {self.author} - Size: {self.file_size_mb}mb, Copy ID: {self.copy_id} - {self.is_checked_out}")

class Patron():
    def __init__(self, name, max_loans):
        self.name = name
        self.borrowed_books = {}
        self.current_loans = 0
        self.max_loans = max_loans

    def borrow_book(self, book):
        key = (book.name, book.copy_id)
        if key not in self.borrowed_books:
            self.borrowed_books[key] = book
            self.current_loans += 1


    def return_book(self, book):
        key = (book.name, book.copy_id)
        if key in self.borrowed_books:
            self.borrowed_books.pop(key)
            self.current_loans -= 1

    def list_loans(self):
        print(f"{self.name} currently has {self.current_loans} books checked out of a max of {self.max_loans}.")

if __name__ == "__main__":
    library = Library()
    alice = Patron("Alice", max_loans=3)
    bob   = Patron("Bob", max_loans=3)

    # Add multiple copies (give unique copy_ids yourself)
    library.add_book(PhysicalBook("The Hobbit", "J.R.R. Tolkien", shelf_location="A3", copy_id=1))
    library.add_book(PhysicalBook("The Hobbit", "J.R.R. Tolkien", shelf_location="A3", copy_id=2))
    library.add_book(EBook("1984", "George Orwell", file_size_mb=2.5, copy_id=1))

    print("\n--- Inventory ---")
    library.list_books()

    print("\n--- Search 'the' ---")
    results = library.search("the")  # expect matches for The Hobbit
    # print results in whatever format you design

    print("\n--- Checkouts ---")
    library.checkout_book("The Hobbit", alice)  # gets one copy
    library.checkout_book("The Hobbit", bob)    # gets the other copy
    library.checkout_book("The Hobbit", alice)  # should fail (no copies left OR rule: already holds title)

    print("\n--- Alice Loans ---")
    alice.list_loans()

    print("\n--- Returns ---")
    library.return_book("The Hobbit", alice)    # frees one copy

    print("\n--- Final Inventory ---")
    library.list_books()
