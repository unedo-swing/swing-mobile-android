from core.android_base_page import AndroidBasePage
from locators.tee_time.explore_locators import ExploreLocators as L


class ExplorePage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.search_bar, timeout=20), "Explore screen not shown"
        self.capture_step("explore_screen", "Explore screen is visible")

    def is_loaded(self) -> bool:
        return self.is_visible(L.search_bar, timeout=20)

    # ================= header =================
    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("explore_back", "Tapped back")

    def tap_search(self):
        self.click(L.search_bar)
        self.capture_step("explore_search", "Tapped Search golf courses")

    def type_search(self, query: str):
        self.type_text(L.search_input, query)
        self.press_search()
        self.capture_step("search_typed", f"Typed search '{query}' and pressed Search")

    def search_course(self, query: str):
        self.tap_search()
        self.type_text(L.search_input, query)
        self.press_search()
        self.capture_step("search_course", f"Searched course '{query}'")

    def clear_search(self):
        self.click(L.button_clear_search)
        self.capture_step("clear_search", "Cleared the search field")

    # ================= search results =================
    def get_results_header(self) -> str:
        return self.find(L.label_results_count).get_attribute("content-desc") or ""

    def verify_results_shown(self, query: str | None = None):
        assert self.is_visible(L.label_results_count, timeout=15), "Search results header not shown"
        header = self.get_results_header()
        if query:
            assert query in header, f"Results header '{header}' does not mention '{query}'"
        self.capture_step("search_results", f"Results header: {header}")

    # ================= empty results state =================
    def verify_no_results(self):
        assert self.is_visible(L.label_no_results, timeout=15), "Empty-results state not shown"
        self.capture_step("no_results", "No-results empty state is visible")

    def tap_request_location(self):
        self.click(L.button_request_location)
        self.capture_step("request_location", "Tapped Request a location")

    # ================= Swing Pass filter =================
    def is_swing_pass_on(self) -> bool:
        return self.find(L.switch_swing_pass).get_attribute("checked") == "true"

    def toggle_swing_pass_partners(self):
        self.click(L.switch_swing_pass)
        self.capture_step("toggle_swing_pass", "Toggled Only show Swing Pass partners")

    def set_swing_pass_partners(self, on: bool):
        if self.is_swing_pass_on() != on:
            self.toggle_swing_pass_partners()
        self.capture_step("swing_pass_state", f"Swing Pass partners = {on}")

    # ================= course cards =================
    def open_course(self, name: str):
        self.click(L.course_card_by_name % name)
        self.capture_step("open_course", f"Opened course '{name}'")

    def verify_course_visible(self, name: str):
        assert self.is_visible(L.course_card_by_name % name), f"Course '{name}' not shown"
        self.capture_step("course_visible", f"Course '{name}' is visible")
