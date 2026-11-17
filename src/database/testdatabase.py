
from src.database.database import add_book, get_all_books

books = [
    ("Sapiens: A Brief History of Humankind",
     "Yuval Noah Harari", "", "HISTORY-01"),

    ("Guns, Germs, and Steel: The Fates of Human Societies",
     "Jared Diamond", "", "HISTORY-02"),

    ("India After Gandhi",
     "Ramachandra Guha", "", "HISTORY-03"),

    ("Train to Pakistan",
     "Khushwant Singh", "", "LITERATURE-01"),

    ("The White Tiger",
     "Aravind Adiga", "", "LITERATURE-02"),

    ("Five Point Someone",
     "Chetan Bhagat", "", "LITERATURE-03")
]

for book in books:
    add_book(*book)

print("\nSHELFNEX BOOK COLLECTION")
print("------------------------")

all_books = get_all_books()

for book in all_books:
    print(book)

print(f"\nTotal registered books: {len(all_books)}")
