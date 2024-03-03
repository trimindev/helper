from time import sleep, time
import pyperclip
from pyautogui import (
    click,
    hotkey,
    ImageNotFoundException,
    locateCenterOnScreen,
    locateAllOnScreen,
)


def copy_and_paste(text):
    hotkey("ctrl", "a")
    pyperclip.copy(text)
    hotkey("ctrl", "v")
    sleep(0.2)


def find_image_center_pos(image_paths, timeout=5, region=None):
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
                    print(f"Found {image_path} at: {location[0]}, {location[1]}")
                    return location
            except ImageNotFoundException:
                pass
        sleep(0.1)

    print(f"Not found {image_paths}")
    return False


def find_and_click_image_center_pos(image_paths, timeout=5, region=None):
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


def find_all_image_center_pos(image_paths, timeout=5, region=None):
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


if __name__ == "__main__":
    pass
