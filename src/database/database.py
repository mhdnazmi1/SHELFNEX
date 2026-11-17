
import sqlite3
from pathlib import Path


# Find the main SHELFNEX project folder
BASE_DIR = Path(__file__).resolve().parents[2]

# Database location
DB_DIR = BASE_DIR / "data" / "database"
DB_PATH = DB_DIR / "shelfnex.db"


def connect_db():
    """Connect to the SHELFNEX SQLite database."""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def create_tables():
    """Create the books table if it does not already exist."""
    with connect_db() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT DEFAULT '',
                isbn TEXT DEFAULT '',
                shelf_code TEXT NOT NULL
            )
        """)


def add_book(title, author="", isbn="", shelf_code=""):
    """Add a book, preventing duplicate ISBN or title-author entries."""
    title = title.strip()
    author = author.strip()
    isbn = isbn.strip()
    shelf_code = shelf_code.strip()

    if not title or not shelf_code:
        print("[ERROR] Book title and shelf code are required.")
        return False

    create_tables()

    with connect_db() as connection:
        # Check for an existing ISBN, if one was provided
        if isbn:
            duplicate = connection.execute(
                "SELECT id FROM books WHERE isbn = ? AND isbn != ''",
                (isbn,)
            ).fetchone()

            if duplicate:
                print("[INFO] This ISBN is already registered.")
                return False

        # Check for an existing title and author
        duplicate = connection.execute("""
            SELECT id FROM books
            WHERE LOWER(TRIM(title)) = LOWER(?)
            AND LOWER(TRIM(author)) = LOWER(?)
        """, (title, author)).fetchone()

        if duplicate:
            print("[INFO] This book is already registered.")
            return False

        connection.execute("""
            INSERT INTO books (title, author, isbn, shelf_code)
            VALUES (?, ?, ?, ?)
        """, (title, author, isbn, shelf_code))

    print(f"[OK] Added book: {title}")
    return True


def get_all_books():
    """Return all registered books."""
    create_tables()

    with connect_db() as connection:
        return connection.execute("""
            SELECT id, title, author, isbn, shelf_code
            FROM books
            ORDER BY id
        """).fetchall()


def search_books(keyword):
    """Search books by title or author."""
    keyword = keyword.strip()

    if not keyword:
        return []

    create_tables()

    with connect_db() as connection:
        return connection.execute("""
            SELECT id, title, author, isbn, shelf_code
            FROM books
            WHERE title LIKE ? OR author LIKE ?
            ORDER BY title
        """, (f"%{keyword}%", f"%{keyword}%")).fetchall()


def get_book_by_id(book_id):
    """Find one book using its database ID."""
    create_tables()

    with connect_db() as connection:
        return connection.execute("""
            SELECT id, title, author, isbn, shelf_code
            FROM books
            WHERE id = ?
        """, (book_id,)).fetchone()


def update_shelf_location(book_id, new_shelf_code):
    """Update the shelf code of an existing book."""
    new_shelf_code = new_shelf_code.strip()

    if not new_shelf_code:
        print("[ERROR] Shelf code cannot be empty.")
        return False

    create_tables()

    with connect_db() as connection:
        cursor = connection.execute("""
            UPDATE books
            SET shelf_code = ?
            WHERE id = ?
        """, (new_shelf_code, book_id))

        if cursor.rowcount == 0:
            print("[INFO] Book ID not found.")
            return False

    print(f"[OK] Updated shelf location for book ID {book_id}.")
    return True


if __name__ == "__main__":
    create_tables()

    print("\nSHELFNEX DATABASE")
    print("-----------------")
    print(f"Database: {DB_PATH}")
    print("\nRegistered books:")

    books = get_all_books()

    if books:
        for book in books:
            print(book)
    else:
        print("No books registered yet.")

    print(f"\nTotal registered books: {len(books)}")
    print("\n[OK] Database is ready.")
