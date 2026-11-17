
import cv2
import pytesseract
from pathlib import Path

# Main SHELFNEX project directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Tesseract installation location
TESSERACT_PATH = Path(
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

if TESSERACT_PATH.exists():
    pytesseract.pytesseract.tesseract_cmd = str(TESSERACT_PATH)


def read_book_text(image_path):
    """Read printed text from a shelf image."""

    image_path = Path(image_path)

    if not image_path.is_absolute():
        image_path = BASE_DIR / image_path

    if not image_path.exists():
        print(f"[ERROR] Image not found: {image_path}")
        return None

    image = cv2.imread(str(image_path))

    if image is None:
        print("[ERROR] Could not open image.")
        return None

    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Improve text visibility
    processed = cv2.threshold(
        gray, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    # Extract text using Tesseract
    try:
        extracted_text = pytesseract.image_to_string(
            processed,
            lang="eng",
            config="--psm 6"
        )

        print("\n===== SHELFNEX OCR RESULT =====")
        print(extracted_text.strip())
        print("===============================")

        return extracted_text.strip()

    except pytesseract.TesseractNotFoundError:
        print("[ERROR] Tesseract executable not found.")
        return None


if __name__ == "__main__":
    print("SHELFNEX OCR MODULE")
    print("OCR module is ready.")
