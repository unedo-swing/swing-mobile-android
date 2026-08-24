from core.android_base_page import AndroidBasePage
from locators.swing_pass.payment_option_locators import PaymentOptionLocators as L


class PaymentOptionPage(AndroidBasePage):

    OPTIONS = [L.OPTION_RECURRING, L.OPTION_ONE_TIME]

    def verify_sheet(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "Payment option sheet not shown"
        self.capture_step("payment_option")

    def verify_options(self):
        missing = [name for name in self.OPTIONS
                   if not self.is_visible(L.option_by_name % name)]
        if not self.is_visible(L.button_manual_transfer):
            missing.append("Or manually transfer to us")
        self.capture_step("payment_option_list", "All payment options are shown" if not missing
                          else f"missing: {', '.join(missing)}")
        assert not missing, f"Payment option(s) not shown: {missing}"

    def verify_option(self, name: str, description: str = ""):
        option = self.get_option(name)
        if description:
            assert description in option["body"], \
                f"'{name}' reads '{option['body']}', expected '{description}'"
        self.capture_step("payment_option_entry", option["label"], data=option)

    @staticmethod
    def parse_option(desc: str) -> dict:
        lines = [line.strip() for line in (desc or "").split("\n") if line.strip()]
        return {
            "title": lines[0] if lines else "",
            "body": " ".join(lines[1:]),
            "label": desc or "",
        }

    def get_options(self) -> list:
        options = [
            self.parse_option(e.get_attribute("content-desc") or "")
            for e in self.find_all(L.option_any)
        ]
        self.capture_step("payment_options", f"{len(options)} payment option(s)",
                          data={"options": [o["title"] for o in options]})
        return options

    def get_option(self, name: str) -> dict:
        element = self.find_anywhere(L.option_by_name % name)
        assert element is not None, f"Payment option '{name}' not listed"
        return self.parse_option(element.get_attribute("content-desc") or "")

    def get_title(self) -> str:
        return self.scroll_and_find(L.label_title).get_attribute("content-desc") or ""

    def select_option(self, name: str):
        self.click(L.option_by_name % name)
        self.capture_step("payment_option_pick", f"Picked '{name}'")

    def select_recurring(self):
        self.select_option(L.OPTION_RECURRING)

    def select_one_time(self):
        self.select_option(L.OPTION_ONE_TIME)

    def tap_manual_transfer(self):
        self.click(L.button_manual_transfer)
        self.capture_step("payment_option_manual_transfer")

    def tap_close(self):
        self.click(L.button_close)
        self.capture_step("payment_option_close")

    def dismiss(self):
        self.click(L.scrim)
        self.capture_step("payment_option_dismiss")
