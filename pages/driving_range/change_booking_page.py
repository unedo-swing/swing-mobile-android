"""
Driving Range Change Booking page object (Android).

Opened from a booking's ⋮ menu > 'Reschedule booking'. Two tabs — Reschedule
(Tab 1 of 2) and Cancellation (Tab 2 of 2). The Reschedule tab shows the
reschedule policy, the booking date & time, the reschedule cost and a
'Continue reschedule' action.

Flutter app — values surface through ``content-desc``.
XPaths come from locators/driving_range/change_booking_locators.py.
"""
from core.android_base_page import AndroidBasePage
from locators.driving_range.change_booking_locators import ChangeBookingLocators as L


class DrivingRangeChangeBookingPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_change_booking, timeout=20), "Change Booking screen not shown"
        self.capture_step("dr_change_booking", "Change Booking screen is visible")

    # ================= tabs =================
    def select_reschedule_tab(self):
        self.click(L.tab_reschedule)
        self.capture_step("dr_change_tab_reschedule", "Selected Reschedule tab")

    def select_cancellation_tab(self):
        self.click(L.tab_cancellation)
        self.capture_step("dr_change_tab_cancellation", "Selected Cancellation tab")

    def is_reschedule_tab_selected(self) -> bool:
        el = self.find_anywhere(L.tab_reschedule)
        return el is not None and el.get_attribute("selected") == "true"

    # ================= reschedule tab =================
    def verify_reschedule_policy(self):
        assert self.is_visible_after_scroll(L.label_reschedule_policy, timeout=15), \
            "Reschedule policy section not shown"
        self.capture_step("dr_reschedule_policy", "Reschedule policy section is visible")

    def get_policy_text(self) -> str:
        """The reschedule policy text, e.g.
        '•  Reschedule anytime:\\n•  Allowed for Rp. 15,000'."""
        return self.scroll_and_find(L.label_policy_text).get_attribute("content-desc") or ""

    def get_booking_datetime(self) -> str:
        """The booking date & time block, e.g.
        'Allowed for Rp. 15,000\\n18:00, 12 Aug 2026\\n(Booking date & time)'."""
        return self.scroll_and_find(L.label_booking_datetime).get_attribute("content-desc") or ""

    def get_reschedule_now_text(self) -> str:
        """e.g. 'You can reschedule now for Rp. 15,000'."""
        el = self.find_anywhere(L.label_reschedule_now)
        return "" if el is None else (el.get_attribute("content-desc") or "")

    # ================= cancellation tab =================
    def is_cancellation_tab_selected(self) -> bool:
        el = self.find_anywhere(L.tab_cancellation)
        return el is not None and el.get_attribute("selected") == "true"

    def verify_cancellation_policy(self):
        assert self.is_visible_after_scroll(L.label_cancellation_policy, timeout=15), \
            "Cancellation policy section not shown"
        self.capture_step("dr_cancellation_policy", "Cancellation policy section is visible")

    def get_refund_tier(self, starts_with: str) -> str:
        """A refund tier row by its leading text, e.g.
        get_refund_tier('100% refund') -> '100% refund (with promo code)\\n17:00, 12 Aug 2026'."""
        return self.scroll_and_find(L.refund_tier_by_text % starts_with).get_attribute("content-desc") or ""

    def get_cancel_now_text(self) -> str:
        """e.g. 'You can cancel now and still get refund for 50%!'."""
        el = self.find_anywhere(L.label_cancel_now)
        return "" if el is None else (el.get_attribute("content-desc") or "")

    def tap_continue_cancel(self):
        """Continue to the cancellation confirmation flow."""
        self.click(L.button_continue_cancel)
        self.capture_step("dr_continue_cancel", "Tapped Continue cancel")

    # ================= actions =================
    def is_continue_enabled(self) -> bool:
        return self.is_enabled(L.button_continue_reschedule)

    def tap_continue_reschedule(self):
        """Continue to the Confirm reschedule screen."""
        self.click(L.button_continue_reschedule)
        self.capture_step("dr_continue_reschedule", "Tapped Continue reschedule")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("dr_change_booking_back", "Tapped back")
