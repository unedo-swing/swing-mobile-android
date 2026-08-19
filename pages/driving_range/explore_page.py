from core.android_base_page import AndroidBasePage
from locators.driving_range.explore_locators import DrivingRangeExploreLocators as L


class DrivingRangeExplorePage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.search_bar, timeout=20), "Driving range explore screen not shown"
        self.capture_step("driving_range_explore", "Driving range explore screen is visible")

    def is_loaded(self) -> bool:
        return self.is_visible(L.search_bar, timeout=20)

    def verify_results_loaded(self):
        assert self.wait_until_loaded(), "Driving range results still loading"
        self.capture_step("dr_results_loaded", "Driving range results finished loading")

    # ================= header / search =================
    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("dr_back", "Tapped back")

    def tap_search(self):
        self.click(L.search_bar)
        self.capture_step("dr_search", "Tapped Search driving range")

    def type_search(self, query: str):
        self.type_text(L.search_input, query)
        self.press_search()
        self.capture_step("dr_search_typed", f"Typed search '{query}'")

    def search_range(self, query: str):
        self.tap_search()
        self.type_text(L.search_input, query)
        self.press_search()
        self.capture_step("dr_search_range", f"Searched driving range '{query}'")

    # ================= recent searches =================
    def verify_recent_searches(self):
        assert self.is_visible(L.label_recent_searches, timeout=15), "Recent searches not shown"
        self.capture_step("dr_recent_searches", "Recent searches are visible")

    def select_recent_search(self, name: str):
        self.click(L.recent_search_by_name % name)
        self.capture_step("dr_recent_pick", f"Selected recent search '{name}'")

    # ================= Swing Pass filter =================
    def is_swing_pass_on(self) -> bool:
        return self.find(L.switch_swing_pass).get_attribute("checked") == "true"

    def toggle_swing_pass_partners(self):
        self.click(L.switch_swing_pass)
        self.capture_step("dr_toggle_swing_pass", "Toggled Only show Swing Pass partners")

    def set_swing_pass_partners(self, on: bool):
        if self.is_swing_pass_on() != on:
            self.toggle_swing_pass_partners()
        self.capture_step("dr_swing_pass_state", f"Swing Pass partners = {on}")

    # ================= range cards =================
    def open_range(self, name: str):
        self.click(L.range_card_by_name % name)
        self.capture_step("dr_open_range", f"Opened driving range '{name}'")

    def verify_range_visible(self, name: str):
        assert self.is_visible(L.range_card_by_name % name), f"Driving range '{name}' not shown"
        self.capture_step("dr_range_visible", f"Driving range '{name}' is visible")
