import os
import shutil

import cv2
import pytesseract


def configure_tesseract():
    """
    Locate the Tesseract OCR executable.
    Works for local Windows development and Linux deployment.
    """

    # First try PATH
    tesseract_path = shutil.which("tesseract")

    # Windows default installation location
    if not tesseract_path and os.name == "nt":
        windows_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

        if os.path.exists(windows_path):
            tesseract_path = windows_path

    if not tesseract_path:
        raise RuntimeError(
            "Tesseract OCR was not found. "
            "Please install Tesseract OCR and make sure it is available."
        )

    pytesseract.pytesseract.tesseract_cmd = tesseract_path


def extract_text(image_path: str) -> str:
    configure_tesseract()

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Could not read the image.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, threshold = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    text = pytesseract.image_to_string(threshold)

    return text