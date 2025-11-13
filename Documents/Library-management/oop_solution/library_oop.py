# oop_version.py

class Book:
    def __init__(self, id, title, author, total_copy):
        self.id = id
        self.title = title
        self.author = author
        self.total_copy = total_copy
        self.available_copies = total_copy

    def borrow(self):
        """number of available copies when borrowed"""
        if self.available_copies > 0:
            self.available_copies -= 1
            return True
        return False

    def return_book(self):
        """number of available copies when returned"""
        if self.available_copies < self.total_copy:
            self.available_copies += 1
            return True
        return False

    def __str__(self):
        return f"[{self.id}] {self.title} by {self.author} ({self.available_copies}/{self.total_copy} available)"

class Member:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
        self.borrowed_books_list = []

    def can_borrow(self):
        """Check member borrow books"""
        return len(self.borrowed_books_list) < 3

    def borrow_book(self, book):
        """Borrow a book if allowed"""
        if book.id in self.borrowed_books_list:
            print("Error: Member already borrowed this book!")
            return False

        if not self.can_borrow():
            print("Error: Member has reached the borrowing limit!")
            return False

        if not book.borrow():
            print("Error: No copies available!")
            return False

        self.borrowed_books_list.append(book.id)
        print(f"{self.name} borrowed '{book.title}'")
        return True

    def return_book(self, book):
        """Return borrow book"""
        if book.id not in self.borrowed_books_list:
            print("Error: This member hasn't borrowed this book!")
            return False

        book.return_book()
        self.borrowed_books_list.remove(book.id)
        print(f"{self.name} returned '{book.title}'")
        return True

    def __str__(self):
        """Display member borrow book """
        if not self.borrowed_books_list:
            borrowed = "No books borrowed"
        else:
            borrowed = ""
            for book_id in self.borrowed_books_list:
                borrowed += f"{book_id}, "
            borrowed = borrowed.rstrip(", ")
        return f"Member: {self.name} ({self.email}) | Borrowed: {borrowed}"

class Library:
    def __init__(self):
        self.books = {}    
        self.members = {}  
        self.borrowed_books = []  

    def add_book(self, book_id, title, author, total_copies):
        if book_id in self.books:
            print("Error: Book ID already exists!")
            return
        self.books[book_id] = Book(book_id, title, author, total_copies)
        print(f"Book '{title}' added successfully!")

    def find_book(self, book_id):
        return self.books.get(book_id, None)

    
    def add_member(self, member_id, name, email):
        if member_id in self.members:
            print("Error: Member ID already exists!")
            return
        self.members[member_id] = Member(member_id, name, email)
        print(f"Member '{name}' registered successfully!")

    def find_member(self, member_id):
        return self.members.get(member_id, None)

    def borrow_book(self, member_id, book_id):
        member = self.find_member(member_id)
        book = self.find_book(book_id)

        if not member:
            print("Error: Member not found!")
            return False

        if not book:
            print("Error: Book not found!")
            return False

        success = member.borrow_book(book)
        if success:
            transaction = {
                "member_id": member.id,
                "book_id": book.id,
                "member_name": member.name,
                "book_title": book.title
            }
            self.borrowed_books.append(transaction)
        return success

    def return_book(self, member_id, book_id):
        member = self.find_member(member_id)
        book = self.find_book(book_id)

        if not member or not book:
            print("Error: Member or book not found!")
            return False

        success = member.return_book(book)
        if success:
            # Remove 
            for i, t in enumerate(self.borrowed_books):
                if t["member_id"] == member_id and t["book_id"] == book_id:
                    self.borrowed_books.pop(i)
                    break
        return success

    def display_available_books(self):
        print("\n=== Available Books ===")
        available = [b for b in self.books.values() if b.available_copies > 0]
        if not available:
            print("No books available at the moment.")
            return
        for book in available:
            print(book)

    def display_member_books(self, member_id):
        member = self.find_member(member_id)
        if not member:
            print("Error: Member not found!")
            return
        print(f"\n=== Books borrowed by {member.name} ===")
        if not member.borrowed_books_list:
            print("No books currently borrowed.")
        else:
            for bid in member.borrowed_books_list:
                book = self.find_book(bid)
                if book:
                    print(f"- {book.title} by {book.author}")

    def display_all_members(self):
        print("\n=== Members ===")
        for member in self.members.values():
            print(member)

