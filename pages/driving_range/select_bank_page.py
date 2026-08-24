from core.android_base_page import AndroidBasePage
from locators.driving_range.select_bank_locators import SelectBankLocators as L

import time


class SelectBankPage(AndroidBasePage):

    def verify_screen(self):
        assert self.is_visible(L.label_title, timeout=20), "Select bank dialog not shown"
        self.capture_step("select_bank")

    def search_bank(self, query: str):
        self.type_text(L.input_search, query)
        self.capture_step("search_bank", f"Searched bank '{query}'")

    def select_bank(self, name: str):
        time.sleep(2)
        self.click(L.bank_by_name % name)
        self.capture_step("select_bank_pick", f"Selected bank '{name}'")

    def choose_bank(self, name: str):
        self.search_bank(name)
        self.select_bank(name)

    def dismiss(self):
        self.click(L.scrim)
        self.capture_step("select_bank_dismiss")
