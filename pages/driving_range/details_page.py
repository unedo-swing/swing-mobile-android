"""
Driving range details page object (Android).

Opened from the driving-range Explore card. Per-screen STEPS only, each recording
evidence with capture_step. XPaths come from
locators/driving_range/details_locators.py.
"""
from core.android_base_page import AndroidBasePage
from locators.driving_range.details_locators import DrivingRangeDetailsLocators as L


class DrivingRangeDetailsPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "Driving range details screen not shown"
        self.capture_step("dr_details", "Driving range details screen is visible")

    def verify_range_name(self, name: str):
        assert self.is_visible(L.label_range_name % name), f"Range '{name}' not shown"
        self.capture_step("dr_range_name", f"Range name shown: {name}")

    def verify_slots_loaded(self):
        """Times and durations reload after each date / bay change."""
        assert self.wait_until_loaded(), "Driving range slots still loading"
        self.capture_step("dr_slots_loaded", "Time slots finished loading")

    def verify_book_enabled(self):
        assert self.is_book_enabled(), "Book driving range is disabled"
        self.capture_step("dr_book_enabled", "Book driving range is enabled")

    # ================= header =================
    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("dr_details_back", "Tapped back")

    def tap_share(self):
        self.click(L.button_share)
        self.capture_step("dr_details_share", "Tapped share")

    # ================= promos =================
    def tap_promo(self, name: str):
        self.click(L.promo_by_name % name)
        self.capture_step("dr_promo", f"Tapped promo '{name}'")

    # ================= date / bay / time =================
    def select_date(self, name: str,date_text: str):
        self.click(L.button_calender % name)
        self.click(L.button_date_in_calender % date_text)
        self.capture_step("dr_select_date", f"Selected date '{date_text}'")

    def select_bay_tab(self, name: str):
        """Pick a bay tab by name, e.g. 'Regular' or 'QCorner'."""
        self.click(L.bay_tab_by_name % name)
        self.capture_step("dr_bay_tab", f"Selected bay '{name}'")

    def select_time(self, time_start: str, time_end: str):
        """Tap the time slots that bracket the booking, from start through end
        INCLUSIVE — the app needs both boundary slots selected to enable Book.
        So 18:00-19:00 taps '18:00' and '19:00' (a 60-min booking),
        17:00-19:00 taps 17:00/18:00/19:00, and 18:00-18:00 taps just '18:00'."""
        from datetime import datetime, timedelta

        fmt = "%H:%M"
        current = datetime.strptime(time_start.strip(), fmt)
        end = datetime.strptime(time_end.strip(), fmt)
        if end < current:
            raise ValueError(
                f"time end '{time_end}' must be at or after start '{time_start}'"
            )
        while current <= end:
            slot = current.strftime(fmt)
            self.click(L.time_by_text % slot)
            self.capture_step("dr_select_time", f"Selected time slot '{slot}'")
            current += timedelta(minutes=60)

    # ================= rates & prices =================
    def get_rate(self, duration_label: str) -> str:
        """Read a rate card's full text by its duration, e.g. '60 minutes'."""
        return self.find(L.rate_card_by_duration % duration_label).get_attribute("content-desc") or ""

    def tap_see_pricelist(self):
        self.click(L.button_see_pricelist)
        self.capture_step("dr_pricelist", "Tapped See complete pricelist")

    # ================= summary / location =================
    def get_booking_summary(self) -> str:
        """The top summary bar, e.g. 'From Rp. 20,000 ... 30 Jul • 17:00 • 60 min ...'."""
        return self.find(L.label_booking_summary).get_attribute("content-desc") or ""

    def verify_location_section(self):
        self.scroll_to_text("Location")
        assert self.is_visible(L.label_location_section, timeout=15), "Location section not shown"
        self.capture_step("dr_location", "Location section is visible")

    def tap_view_on_maps(self):
        self.click(L.button_view_on_maps)
        self.capture_step("dr_view_maps", "Tapped View on Google Maps")

    # ================= book =================
    def is_book_enabled(self) -> bool:
        return self.is_enabled(L.button_book)

    def tap_book(self):
        self.click(L.button_book)
        self.capture_step("dr_book", "Tapped Book driving range")
