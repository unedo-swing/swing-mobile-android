"""
Driving Range Reschedule booking page object (Android).

Opened from Change Booking > 'Continue reschedule'. Pick a new date & time
(keeping the same duration / bays / bay type). Shows the original booking
summary, a day grid, a time-slot grid, then 'Confirm new date & time'
(disabled until a date + time are chosen).

Flutter app — values surface through ``content-desc``.
XPaths come from locators/driving_range/reschedule_booking_locators.py.
"""
from core.android_base_page import AndroidBasePage
from locators.driving_range.reschedule_booking_locators import RescheduleBookingLocators as L


class DrivingRangeRescheduleBookingPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_reschedule_booking, timeout=20), \
            "Reschedule booking screen not shown"
        self.capture_step("dr_reschedule_booking", "Reschedule booking screen is visible")

    # ================= original booking summary =================
    def _desc(self, locator) -> str:
        return self.scroll_and_find(locator).get_attribute("content-desc") or ""

    def get_original_date_time(self) -> str:
        return self._desc(L.value_original_date_time)

    def get_duration(self) -> str:
        return self._desc(L.value_duration)

    def get_bays(self) -> str:
        return self._desc(L.value_bays)

    def get_bay_type(self) -> str:
        return self._desc(L.value_bay_type)

    def get_constraint_note(self) -> str:
        """e.g. 'You can only reschedule by maintaining the same duration, ...'."""
        return self._desc(L.label_description_reschedule)

    def get_week_range(self) -> str:
        """e.g. '03 Aug - 09 Aug'."""
        el = self.find_anywhere(L.label_week_range)
        return "" if el is None else (el.get_attribute("content-desc") or "")

    # ================= day grid =================
    def is_date_enabled(self, day) -> bool:
        el = self.find_anywhere(L.date_by_number % str(day))
        return el is not None and el.get_attribute("enabled") == "true"

    def select_date(self, date: str):
        self.click(L.button_open_calender)
        self.click(L.button_date_in_calender % date)
        self.capture_step("dr_reschedule_select_date", f"Selected date '{date}'")

    def open_calendar(self):
        self.click(L.button_open_calender)
        self.capture_step("dr_reschedule_open_calendar", "Opened calendar")

    # ================= time grid =================
    def is_time_available(self, time_text: str) -> bool:
        el = self.find_anywhere(L.button_slot_time % time_text)
        return el is not None and el.get_attribute("clickable") == "true"

    def select_time(self, time_text: str):
        self.click(L.button_slot_time % time_text)
        self.capture_step("dr_reschedule_select_time", f"Selected time '{time_text}'")

    # ================= confirm =================
    def is_confirm_enabled(self) -> bool:
        return self.is_enabled(L.button_confirm_new_date)

    def verify_confirm_enabled(self):
        assert self.is_confirm_enabled(), "Confirm new date & time is disabled"
        self.capture_step("dr_reschedule_confirm_enabled", "Confirm new date & time is enabled")

    def tap_confirm_new_date(self):
        """Confirm the new date & time -> Confirm reschedule screen."""
        self.click(L.button_confirm_new_date)
        self.capture_step("dr_reschedule_confirm_date", "Tapped Confirm new date & time")

    # ================= scenario =================
    def pick_new_slot(self, day, time_text: str):
        """Select a day + time slot and confirm."""
        self.select_date(day)
        self.select_time(time_text)
        self.verify_confirm_enabled()
        self.tap_confirm_new_date()

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("dr_reschedule_booking_back", "Tapped back")
