from time import sleep, time
import pyperclip
from pyautogui import (
    click,
    hotkey,
    ImageNotFoundException,
    locateCenterOnScreen,
    locateOnScreen,
    locateAllOnScreen,
    screenshot,
)
import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\xinch\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)


def copy_and_paste(text):
    hotkey("ctrl", "a")
    pyperclip.copy(text)
    hotkey("ctrl", "v")
    sleep(0.2)
    print("Pasted text successfully")
    return True


def find_img(image_paths, timeout=10, region=None):
    start_time = time()

    if isinstance(image_paths, str):
        image_paths = [image_paths]

    while time() - start_time < timeout:
        for image_path in image_paths:
            try:
                location = locateCenterOnScreen(
                    image_path, confidence=0.9, region=region
                )
                if location is not None:
                    print(f"Found {image_path} at: {location[0]}, {location[1]}")
                    return location
            except ImageNotFoundException:
                pass
        sleep(0.1)

    print(f"Not found {image_paths}")
    return False


def find_img_region(image_paths, timeout=10, region=None):
    start_time = time()

    if isinstance(image_paths, str):
        image_paths = [image_paths]

    while time() - start_time < timeout:
        for image_path in image_paths:
            try:
                location = locateOnScreen(image_path, confidence=0.9, region=region)
                region = (
                    int(location.left),
                    int(location.top),
                    int(location.width),
                    int(location.height),
                )
                if location is not None:
                    print(f"Found {image_path} at: {region}")
                    return region
            except ImageNotFoundException:
                pass
        sleep(0.1)

    print(f"Not found {image_paths}")

    return False


def click_img(image_paths, timeout=10, region=None):
    start_time = time()

    if isinstance(image_paths, str):
        image_paths = [image_paths]

    while time() - start_time < timeout:
        for image_path in image_paths:
            try:
                location = locateCenterOnScreen(
                    image_path, confidence=0.8, region=region
                )
                if location is not None:
                    click(location)
                    print(f"Clicked {image_paths} at: {location[0]}, {location[1]}")
                    return location
            except ImageNotFoundException:
                pass
        sleep(0.1)

    print(f"Not found {image_paths}")
    return False


def find_all_img(image_paths, timeout=5, region=None):
    start_time = time()

    if isinstance(image_paths, str):
        image_paths = [image_paths]

    while time() - start_time < timeout:
        for image_path in image_paths:
            try:
                locations = list(
                    locateAllOnScreen(image_path, confidence=0.9, region=region)
                )
                if locations:
                    center_locations = [center_of(box) for box in locations]

                    return center_locations
            except ImageNotFoundException:
                pass
        sleep(0.1)

    return False


def center_of(box):
    center_x = box.left + box.width // 2
    center_y = box.top + box.height // 2
    return center_x, center_y


def capture_and_recognize_text(region):
    # Capture screenshot of the specified region
    screenshot_img = screenshot(region=region)

    # Convert screenshot to OpenCV format (BGR)
    screenshot_cv2 = cv2.cvtColor(np.array(screenshot_img), cv2.COLOR_RGB2BGR)

    # Convert screenshot to grayscale
    gray = cv2.cvtColor(screenshot_cv2, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to extract text regions
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area and aspect ratio to identify potential text regions
    potential_text_contours = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)
        aspect_ratio = w / float(h)
        if area > 100 and aspect_ratio > 0.5 and aspect_ratio < 5:
            potential_text_contours.append(contour)

    # Extract bounding boxes of potential text regions
    bounding_boxes = [cv2.boundingRect(contour) for contour in potential_text_contours]

    # Recognize text within each bounding box using Tesseract OCR
    for x, y, w, h in bounding_boxes:
        roi = gray[y : y + h, x : x + w]
        text = pytesseract.image_to_string(roi, config="--psm 6 outputbase digits")

    return text


if __name__ == "__main__":
    sleep(2)
    hotkey("alt", "tab")

    pass
