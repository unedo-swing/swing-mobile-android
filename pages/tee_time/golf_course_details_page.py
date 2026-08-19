from core.android_base_page import AndroidBasePage
from locators.tee_time.golf_course_details_locators import GolfCourseDetailsLocators as L


class GolfCourseDetailsPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.label_title, timeout=20), "Golf course details screen not shown"
        self.capture_step("course_details", "Golf course details screen is visible")

    def verify_course_name(self, name: str):
        assert self.is_visible(L.label_course_name % name), f"Course '{name}' not shown"
        self.capture_step("course_name", f"Course name shown: {name}")

    # ================= header =================
    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("details_back", "Tapped back")

    def tap_share(self):
        self.click(L.button_share)
        self.capture_step("details_share", "Tapped share")

    # ================= date & session =================
    def open_calendar(self, course_name: str):
        self.click(L.button_calender % course_name)
        self.capture_step("open_calendar", "Opened the date calendar")

    def select_date_in_calendar(self, date_text: str):
        self.click(L.button_date_in_calender % date_text)
        self.capture_step("calendar_date", f"Picked date '{date_text}' in calendar")

    def select_date(self, date_text: str):
        self.click(L.date_by_text % date_text)
        self.capture_step("select_date", f"Selected date '{date_text}'")

    def select_day_session(self):
        self.click(L.tab_day_session)
        self.capture_step("day_session", "Selected Day Session")

    def select_night_session(self):
        self.click(L.tab_night_session)
        self.capture_step("night_session", "Selected Night Session")

    # ================= tee-time slots =================
    def select_time_slot(self, time_text: str):
        self.click(L.time_slot_by_text % time_text)
        self.capture_step("select_slot", f"Selected tee time '{time_text}'")

    # ================= prices / amenities / location / more info =================
    def verify_prices_section(self):
        assert self.is_visible(L.label_prices_include, timeout=15), "Prices section not shown"
        self.capture_step("prices_section", "Prices shown include section is visible")

    def verify_amenities_section(self):
        self.scroll_to_text("Amenities")
        assert self.is_visible(L.label_amenities, timeout=15), "Amenities section not shown"
        self.capture_step("amenities_section", "Amenities section is visible")

    def verify_amenity(self, name: str):
        assert self.is_visible(L.amenity_by_name % name), f"Amenity '{name}' not shown"
        self.capture_step("amenity", f"Amenity shown: {name}")

    def verify_location_section(self):
        self.scroll_to_text("Location")
        assert self.is_visible(L.label_location_section, timeout=15), "Location section not shown"
        self.capture_step("location_section", "Location section is visible")

    def tap_view_on_maps(self):
        self.click(L.button_view_on_maps)
        self.capture_step("view_on_maps", "Tapped View on Google Maps")

    def verify_more_info_section(self):
        self.scroll_to_text("More information")
        assert self.is_visible(L.label_more_information, timeout=15), "More information section not shown"
        self.capture_step("more_info_section", "More information section is visible")

    def get_stat(self, label: str) -> str:
        return self.find(L.stat_by_label % label).get_attribute("content-desc") or ""

    # ================= book =================
    def get_booking_summary(self) -> str:
        return self.find(L.label_booking_summary).get_attribute("content-desc") or ""

    def verify_slot_selected(self):
        assert self.is_visible(L.label_booking_summary, timeout=10), "No slot selected (summary not shown)"
        assert self.is_book_enabled(), "Book button is not enabled after selecting a slot"
        self.capture_step("slot_selected", f"Selected slot: {self.get_booking_summary()}")

    def verify_cashback_badge(self):
        assert self.is_visible(L.badge_cashback), "Cashback badge not shown"
        self.capture_step("cashback_badge", "Cashback badge is visible")

    def is_book_enabled(self) -> bool:
        return self.is_enabled(L.button_book)

    def tap_book(self):
        self.click(L.button_book)
        self.capture_step("book_tee_time", "Tapped Book tee time")
