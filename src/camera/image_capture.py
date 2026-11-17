
import cv2
from pathlib import Path
from datetime import datetime

# Main SHELFNEX project folder
BASE_DIR = Path(__file__).resolve().parents[2]

# Folder where captured images will be stored
IMAGE_DIR = BASE_DIR / "data" / "captured_images"


def capture_from_webcam(camera_index=0):
    """Capture and save a shelf image using a webcam."""

    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    camera = cv2.VideoCapture(camera_index)

    if not camera.isOpened():
        print("[ERROR] Webcam not detected or unavailable.")
        return None

    print("[INFO] Webcam connected.")
    print("[INFO] Press SPACE to capture.")
    print("[INFO] Press ESC to cancel.")

    saved_path = None

    try:
        while True:
            success, frame = camera.read()

            if not success:
                print("[ERROR] Could not read webcam image.")
                break

            cv2.imshow("SHELFNEX - Shelf Camera", frame)

            key = cv2.waitKey(1) & 0xFF

            if key == 32:  # SPACE key
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"shelf_{timestamp}.jpg"
                saved_path = IMAGE_DIR / filename

                if cv2.imwrite(str(saved_path), frame):
                    print(f"[OK] Image saved: {saved_path}")
                else:
                    print("[ERROR] Could not save image.")
                    saved_path = None

                break

            elif key == 27:  # ESC key
                print("[INFO] Capture cancelled.")
                break

    finally:
        camera.release()
        cv2.destroyAllWindows()

    return saved_path


def load_saved_image(image_path):
    """Load an existing shelf image for offline testing."""

    path = Path(image_path)

    if not path.is_absolute():
        path = BASE_DIR / path

    image = cv2.imread(str(path))

    if image is None:
        print(f"[ERROR] Could not load image: {path}")
        return None

    print("[OK] Shelf image loaded successfully.")
    print(f"[INFO] Image dimensions: {image.shape[1]} x {image.shape[0]}")

    return image


if __name__ == "__main__":
    print("\n===== SHELFNEX IMAGE CAPTURE SYSTEM =====")
    capture_from_webcam()
