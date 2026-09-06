import time
from datetime import datetime

from core.android_base_page import AndroidBasePage
from locators.multisport.select_schedule_page_locators import (
    SelectSchedulePageLocators as L,
)


class SelectSchedulePage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.header_select_schedule_page, timeout=20),             "Select schedule page not shown"
        self.capture_step("select_schedule_screen",
                          "Select schedule screen is visible")

    # ================= next-day loop =================
    def navigate_to_next_day_until_gone(self):
        while self.is_visible(L.button_go_to_next_day, timeout=5):
            self.click(L.button_go_to_next_day)
            self.capture_step("go_to_next_day", "Tapped Go to next day")
            time.sleep(3)
        self.capture_step("next_day_stopped",
                          "Go to next day button is gone — stop looping")

    # ================= pick schedule =================
    def select_schedule(self, schedule_title: str, how_many: int):
        year = str(datetime.now().year)
        for idx in range(1, how_many + 1):
            locator = L.button_choose_schedule % (
                year,
                schedule_title.lower(),
                idx,
            )
            self.click(locator)
            self.capture_step(
                "select_schedule",
                f"Selected schedule: {schedule_title} (instance {idx})",
            )
        self.capture_step(
            "schedule_selected",
            f"Schedule '{schedule_title}' selected {how_many} times",
        )

    # ================= confirm =================
    def confirm_schedules(self):
        self.click(L.button_confirm_schedule)
        self.capture_step("confirm_schedules", "Tapped Confirm Schedules")
