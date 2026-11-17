
import re
from difflib import SequenceMatcher

from src.database.database import get_all_books


def normalize_text(text):
    """Convert text into a standard format for comparison."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return " ".join(text.split())


def find_book_match(ocr_line, books):
    """Find the closest registered book title for an OCR line."""

    line = normalize_text(ocr_line)

    if len(line) < 4:
        return None

    best_book = None
    best_score = 0

    for book in books:
        book_id, title, author, isbn, shelf_code = book

        normalized_title = normalize_text(title)

        if not normalized_title:
            continue

        # Exact or partial title match
        if normalized_title in line or (
            len(line) >= 5 and line in normalized_title
        ):
            return book

        score = SequenceMatcher(
            None, line, normalized_title
        ).ratio()

        if score > best_score:
            best_score = score
            best_book = book

    # Avoid accepting weak matches
    if best_score >= 0.62:
        return best_book

    return None


def check_misplaced_books(detected_text, scanned_shelf_code):
    """
    Compare OCR-detected titles with registered shelf locations.
    """

    if not detected_text:
        print("[ERROR] No text received from OCR.")
        return []

    books = get_all_books()

    if not books:
        print("[ERROR] No books found in the database.")
        return []

    scanned_shelf_code = scanned_shelf_code.strip().upper()

    results = []
    processed_books = set()

    lines = detected_text.splitlines()

    for line in lines:
        matched_book = find_book_match(line, books)

        if matched_book is None:
            continue

        book_id, title, author, isbn, correct_shelf = matched_book

        # Avoid reporting the same database record twice
        if book_id in processed_books:
            continue

        processed_books.add(book_id)

        correct_shelf = correct_shelf.strip().upper()

        if correct_shelf == scanned_shelf_code:
            status = "CORRECT"
        else:
            status = "MISPLACED"

        result = {
            "book_id": book_id,
            "title": title,
            "scanned_shelf": scanned_shelf_code,
            "correct_shelf": correct_shelf,
            "status": status
        }

        results.append(result)

    print("\n===== SHELFNEX DETECTION REPORT =====")

    if not results:
        print("No registered book titles were recognised.")

    for result in results:
        print(f"\nBook: {result['title']}")
        print(f"Scanned shelf: {result['scanned_shelf']}")

        if result["status"] == "MISPLACED":
            print(f"[MISPLACED] Correct shelf: {result['correct_shelf']}")
        else:
            print("[CORRECT] Book is on its registered shelf.")

    print("\n=====================================")

    return results


if __name__ == "__main__":

    # Temporary demonstration using sample OCR text.
    # This does not require a webcam or OCR image.

    sample_ocr_text = """
    The Silk Road
    Guns Germs and Steel
    """

    check_misplaced_books(
        sample_ocr_text,
        "HISTORY-02"
    )
