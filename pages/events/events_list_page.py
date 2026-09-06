from core.android_base_page import AndroidBasePage
from locators.events.register_events_locators import RegisterEventsLocators as L


class EventsListPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.title_filter, timeout=20) or self.is_visible(
            L.card_event % "", timeout=5
        ), "Events list screen not shown"
        self.capture_step("events_list", "Events list screen is visible")

    def verify_event_card(self, name: str):
        self.scroll_to_element(L.card_event % name)
        assert self.is_visible(L.card_event % name, timeout=20), (
            f"Event card '{name}' not shown"
        )
        self.capture_step("events_card", f"Event card shown: {name}")

    # ================= action steps =================
    def open_event(self, name: str):
        self.click(L.card_event % name)
        self.capture_step("open_event", f"Opened event: {name}")
