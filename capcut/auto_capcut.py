import subprocess
from pyautogui import (
    click,
    hotkey,
)
from time import sleep
from auto_utils import (
    find_image_center_pos,
    find_and_click_image_center_pos,
)


class AutoCapcut:
    def __init__(self):
        self.setup_track_positions(813, 48)

    def create_new_project(self):
        # Open capcut_exe
        subprocess.Popen("C:\\Users\\xinch\\AppData\\Local\\CapCut\\CapCut.exe")

        # Click create new project
        if not find_and_click_image_center_pos("cc_img/new_project.png", 7):
            if not find_and_click_image_center_pos("cc_img/new_project.png"):
                return False

        sleep(2)

        self.find_and_setup_track_positions()
        return True

    def setup_track_positions(self, main_y, lock_x):
        # Margin y of tracks
        main_mb = 67
        audio_mb = 55
        video_mt = 70

        # Y of tracks ----------------------------------------
        self.main_y = main_y
        print("main_y:", self.main_y)

        self.video_2_y = self.main_y - video_mt
        self.video_3_y = self.main_y - video_mt * 2

        self.audio_1_y = self.main_y + main_mb
        self.audio_2_y = self.audio_1_y + audio_mb
        self.audio_3_y = self.audio_1_y + audio_mb * 2

        self.text_1_y = None

        # Lock button posititons ------------------------------
        self.lock_x = lock_x
        print("lock_x:", self.lock_x)

        self.lock_main_pos = self.lock_x, self.main_y
        self.lock_video_2_pos = (self.lock_x, self.video_2_y)
        self.lock_video_3_pos = (self.lock_x, self.video_3_y)

        self.lock_audio_1_pos = (self.lock_x, self.audio_1_y)
        self.lock_audio_2_pos = (self.lock_x, self.audio_2_y)
        self.lock_audio_3_pos = (self.lock_x, self.audio_3_y)

        self.lock_text_1_pos = (self.lock_x, self.text_1_y)

    def find_and_setup_track_positions(self):
        # Find select mode
        select_mode_pos = find_image_center_pos("cc_img/select_mode.png")

        # Find drag material here
        drag_material_here_pos = find_image_center_pos("cc_img/drag_material_here.png")

        self.setup_track_positions(drag_material_here_pos[1], select_mode_pos[0])

        return True

    def select_track(self, *track_positions):

        if isinstance(track_positions[0], list):
            track_positions = track_positions[0]

        lock_positions = [
            self.lock_main_pos,
            self.lock_video_2_pos,
            self.lock_video_3_pos,
            self.lock_audio_1_pos,
            self.lock_audio_2_pos,
            self.lock_audio_3_pos,
            self.lock_text_1_pos,
        ]

        # Filter out the positions with None values and the positions not to click
        click_positions = [
            p
            for p in lock_positions
            if p[1] is not None and p[1] not in track_positions
        ]

        # Click on the positions except for the track_positions
        for position in click_positions:
            click(position)
            # Don't need sleep

        hotkey("ctrl", "a")

        # Click on the positions except for the track_positions again to deselect
        for position in click_positions:
            click(position)
            # Don't need sleep

        print("Tracks selected")
        return True

    def find_and_click_current_clip_pos(self):
        pos = find_image_center_pos("cc_img/point.png")
        if not pos:
            return False

        current_clip_pos = pos[0] + 10, self.main_y
        click(current_clip_pos)

        print("Clicked current clip at:", current_clip_pos[0], current_clip_pos[1])
        return current_clip_pos


def main():
    app = AutoCapcut()
    app.create_new_project()


if __name__ == "__main__":
    main()
