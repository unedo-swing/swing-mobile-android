from core.android_base_page import AndroidBasePage
from locators.events.event_details_locators import EventDetailsLocators as L


class EventDetailsPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.title_header, timeout=20), "Event details not shown"
        self.capture_step("event_details", "Event details screen is visible")

    def verify_event_title(self, name: str):
        assert self.is_visible(L.title_event % name, timeout=20), (
            f"Event title '{name}' not shown"
        )
        self.capture_step("event_title", f"Event title shown: {name}")

    def verify_registration_closed_footer(self):
        if self.is_visible(L.button_reminder):
            self.click(L.button_reminder)

        self.scroll_to_element(L.label_successfully_reminder)
        assert self.is_visible(L.label_successfully_reminder, timeout=20), (
            "Reminder confirmation ('notify you if') not shown"
        )
        self.capture_step(
            "event_reg_closed", "Registration closed: footer 'notify you if' is visible"
        )

    def verify_registration_open(self):
        assert self.is_visible(L.button_booking, timeout=20), (
            "Registration button not shown — registration may not be open"
        )
        self.capture_step("event_reg_open", "Registration open")

    # ================= action steps =================
    def tap_notify_me(self):
        self.click(L.button_reminder)
        self.capture_step("tap_notify_me", "Tapped 'Notify me for the next event'")

    def tap_booking_button(self):
        self.click(L.button_booking)
        self.capture_step("tap_booking_button", "Tapped 'Secure your slot'")
