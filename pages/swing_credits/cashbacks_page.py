from core.android_base_page import AndroidBasePage
from locators.swing_credits.cashbacks_locators import CashbacksLocators as L


class CashbacksPage(AndroidBasePage):

    TABS = [L.TAB_ALL, L.TAB_DRIVING_RANGE, L.TAB_GOLF_COURSE, L.TAB_EVENT]

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "Swing Credits cashbacks screen not shown"
        self.capture_step("cashbacks", "Swing Credits cashbacks screen is visible")

    def verify_columns(self):
        assert self.is_visible(L.label_regular_players), "'Regular Swing players' column not shown"
        assert self.is_visible(L.label_pass_members), "'Swing Pass members' column not shown"
        self.capture_step("cashbacks_columns", "Both cashback columns are labelled")

    def is_venue_listed(self, name: str) -> bool:
        return self.find_anywhere(L.venue_by_name % name) is not None

    def verify_venue_listed(self, name: str):
        assert self.is_venue_listed(name), f"Venue '{name}' not listed"
        self.capture_step("cashbacks_venue", f"Venue '{name}' is listed")

    # ================= tabs =================
    def get_selected_tab(self) -> str:
        elements = self.find_all(L.tab_selected)
        if not elements:
            return ""
        desc = elements[0].get_attribute("content-desc") or ""
        return desc.split("\n")[-1].strip()

    def select_tab(self, label: str):
        self.click(L.tab_by_label % label)
        self.capture_step("cashbacks_tab", f"Selected tab '{label}'")

    def verify_tab_selected(self, label: str):
        actual = self.get_selected_tab()
        self.capture_step("cashbacks_tab_state", f"Selected tab: {actual}")
        assert actual == label, f"Selected tab is '{actual}', expected '{label}'"

    # ================= search =================
    def search(self, query: str):
        self.fill(L.input_search, query)
        self.press_search()
        self.capture_step("cashbacks_search", f"Searched '{query}'")

    # ================= reading a venue row =================
    def _desc(self, locator) -> str:
        element = self.find_anywhere(locator)
        return "" if element is None else (element.get_attribute("content-desc") or "")

    def get_venue(self, name: str) -> dict:
        row = {
            "name": name,
            "type": self._desc(L.venue_type % name),
            "location": self._desc(L.venue_location % name),
            "days": self._desc(L.venue_days % name),
            "hours": self._desc(L.venue_hours % name),
            "cashback_regular": self._desc(L.venue_cashback_regular % name),
            "cashback_pass": self._desc(L.venue_cashback_pass % name),
        }
        self.capture_step("cashbacks_row", f"Cashbacks for '{name}'", data=row)
        return row

    def verify_venue(self, name: str, **expected):
        actual = self.get_venue(name)
        mismatches = {
            field: (want, actual.get(field, ""))
            for field, want in expected.items()
            if want and want.strip().casefold() != (actual.get(field, "") or "").strip().casefold()
        }
        assert not mismatches, (
            f"Cashback row for '{name}' does not match:\n"
            + "\n".join(
                f"  {field}: expected '{want}' but row reads '{got}'"
                for field, (want, got) in mismatches.items()
            )
        )

    # ================= navigation =================
    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("cashbacks_back", "Left the cashbacks screen")
