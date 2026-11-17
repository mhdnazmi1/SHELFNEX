
from src.database.database import (
    search_books,
    get_book_by_id,
    update_shelf_location,
    get_all_books
)

print("\n===== SHELFNEX DATABASE TESTING =====")

# TEST 1: Search books
print("\nTEST 1: SEARCH BOOKS")

results = search_books("Sapiens")

for book in results:
    print(book)

if results:
    print("[PASS] Book search works.")
else:
    print("[FAIL] Book search failed.")


# TEST 2: Find book by ID
print("\nTEST 2: FIND BOOK BY ID")

book = get_book_by_id(3)

print(book)

if book:
    print("[PASS] Finding book by ID works.")
else:
    print("[FAIL] Book ID not found.")


# TEST 3: Update shelf location
print("\nTEST 3: UPDATE SHELF LOCATION")

if book:
    original_shelf = book[4]

    # Temporarily update the shelf location
    update_shelf_location(3, "TEST-01")

    updated_book = get_book_by_id(3)

    if updated_book and updated_book[4] == "TEST-01":
        print("[PASS] Shelf update works.")

        # Restore the original shelf location
        update_shelf_location(3, original_shelf)

        print("[OK] Original shelf location restored.")
    else:
        print("[FAIL] Shelf update failed.")


# FINAL DATABASE CHECK
print("\n===== FINAL BOOK COLLECTION =====")

all_books = get_all_books()

for item in all_books:
    print(item)

print(f"\nTotal registered records: {len(all_books)}")
print("\n===== DATABASE TESTING FINISHED =====")


