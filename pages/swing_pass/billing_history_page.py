from core.android_base_page import AndroidBasePage
from locators.swing_pass.billing_history_locators import BillingHistoryLocators as L


class BillingHistoryPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "Billing History screen not shown"
        self.capture_step("billing_history", "Billing History screen is visible")

    def verify_entry_count(self, expected: int):
        entries = self.get_entries()
        assert len(entries) == expected, \
            f"{len(entries)} billing entr(y/ies) listed, expected {expected}"

    def verify_entry(self, index: int = 1, **expected):
        actual = self.get_entry(index)
        mismatches = {
            field: (want, actual.get(field, ""))
            for field, want in expected.items()
            if want and want.strip().casefold() != (actual.get(field, "") or "").strip().casefold()
        }
        assert not mismatches, (
            f"Billing entry #{index} does not match:\n"
            + "\n".join(
                f"  {field}: expected '{want}' but entry reads '{got}'"
                for field, (want, got) in mismatches.items()
            )
        )

    # ================= parsing =================
    @staticmethod
    def parse_entry(desc: str) -> dict:
        lines = [line.strip() for line in (desc or "").split("\n") if line.strip()]
        entry = {"price": "", "period": "", "date": "", "time": "", "label": desc or ""}
        if lines:
            price, sep, period = lines[0].partition("/")
            entry["price"] = price.strip()
            entry["period"] = period.strip() if sep else ""
        if len(lines) >= 2:
            date, sep, time = lines[1].partition(",")
            entry["date"] = date.strip()
            entry["time"] = time.strip() if sep else ""
        return entry

    # ================= reading =================
    def get_entries(self) -> list:
        entries = [
            self.parse_entry(e.get_attribute("content-desc") or "")
            for e in self.find_all(L.entry_any)
        ]
        self.capture_step("billing_entries", f"{len(entries)} billing entr(y/ies) listed",
                          data={"entries": entries})
        return entries

    def get_entry(self, index: int = 1) -> dict:
        element = self.scroll_and_find(L.entry_at % index)
        entry = self.parse_entry(element.get_attribute("content-desc") or "")
        self.capture_step("billing_entry", f"Entry #{index}: {entry['label']}", data=entry)
        return entry

    def get_latest_entry(self) -> dict:
        return self.get_entry(1)

    def get_entry_by_text(self, text: str) -> dict:
        element = self.find_anywhere(L.entry_by_text % text)
        assert element is not None, f"No billing entry matching '{text}'"
        entry = self.parse_entry(element.get_attribute("content-desc") or "")
        self.capture_step("billing_entry", f"Entry matching '{text}'", data=entry)
        return entry

    # ================= action steps =================
    def open_entry(self, index: int = 1):
        self.click(L.entry_at % index)
        self.capture_step("billing_open_entry", f"Opened billing entry #{index}")

    def open_latest_entry(self):
        self.open_entry(1)

    def open_entry_by_text(self, text: str):
        self.click(L.entry_by_text % text)
        self.capture_step("billing_open_entry", f"Opened billing entry '{text}'")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("billing_history_back", "Left the Billing History screen")
