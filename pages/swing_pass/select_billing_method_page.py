from core.android_base_page import AndroidBasePage
from locators.swing_pass.select_billing_method_locators import SelectBillingMethodLocators as L


class SelectBillingMethodPage(AndroidBasePage):

    # what the wallet rows append to their name, e.g. "OVO Connect"
    CONNECT_SUFFIX = " Connect"

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "Select billing method screen not shown"
        self.capture_step("select_method", "Select billing method screen is visible")

    def verify_sections(self):
        missing = [name for name, locator in (("Credit cards", L.label_credit_cards),
                                              ("E-wallets", L.label_ewallets))
                   if not self.is_visible_after_scroll(locator)]
        self.capture_step("select_method_sections", "Both sections are shown" if not missing
                          else f"missing: {', '.join(missing)}")
        assert not missing, f"Section(s) not shown: {missing}"

    def verify_card_listed(self, label: str):
        cards = self.get_cards()
        assert label in cards, f"Card '{label}' not listed — screen shows {cards}"
        self.capture_step("select_method_card", f"Card '{label}' is listed")

    def verify_wallet_listed(self, name: str):
        wallets = self.get_wallets()
        assert name in wallets, f"E-wallet '{name}' not listed — screen shows {wallets}"
        self.capture_step("select_method_wallet", f"E-wallet '{name}' is listed")

    def verify_card_count(self, expected: int):
        cards = self.get_cards()
        assert len(cards) == expected, \
            f"{len(cards)} saved card(s) listed, expected {expected}"

    # ================= reading =================
    def get_cards(self) -> list:
        cards = [
            e.get_attribute("content-desc") or ""
            for e in self.find_all(L.card_any)
        ]
        self.capture_step("select_method_cards", f"{len(cards)} saved card(s)",
                          data={"cards": cards})
        return cards

    def get_wallets(self) -> list:
        wallets = []
        for element in self.find_all(L.wallet_any):
            desc = element.get_attribute("content-desc") or ""
            wallets.append(desc[: -len(self.CONNECT_SUFFIX)]
                           if desc.endswith(self.CONNECT_SUFFIX) else desc)
        self.capture_step("select_method_wallets", f"{len(wallets)} e-wallet(s)",
                          data={"wallets": wallets})
        return wallets

    def get_card(self, index: int = 1) -> str:
        return self.scroll_and_find(L.card_at % index).get_attribute("content-desc") or ""

    # ================= action steps =================
    def select_card(self, index: int = 1):
        label = self.get_card(index)
        self.click(L.card_at % index)
        self.capture_step("select_method_pick_card", f"Picked card #{index} ({label})")

    def select_card_by_label(self, label: str):
        self.click(L.card_by_label % label)
        self.capture_step("select_method_pick_card", f"Picked card '{label}'")

    def tap_add_credit_card(self):
        self.click(L.button_add_card)
        self.capture_step("select_method_add_card", "Tapped Add credit card")

    def connect_wallet(self, name: str):
        self.click(L.button_connect_by_wallet % name)
        self.capture_step("select_method_connect", f"Tapped Connect on '{name}'")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("select_method_back", "Left the Select billing method screen")
