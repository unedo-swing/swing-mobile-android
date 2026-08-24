from core.android_base_page import AndroidBasePage
from locators.tee_time.promo_locators import PromoLocators as L


class PromoPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.label_title, timeout=20), "Available promos screen not shown"
        self.capture_step("available_promos")

    def verify_promo(self, name: str):
        assert self.is_visible(L.promo_by_name % name), f"Promo '{name}' not shown"
        self.capture_step("promo_shown", f"Promo shown: {name}")

    # ================= actions =================
    def search_promo(self, query: str):
        self.type_text(L.input_search, query)
        self.press_search()
        self.capture_step("search_promo", f"Searched promo '{query}'")

    def select_promo(self, name: str):
        self.click(L.promo_by_name % name)
        self.capture_step("select_promo", f"Selected promo '{name}'")

    def apply_promo(self, name: str | None = None):
        locator = L.apply_by_promo_name % name if name else L.button_apply
        self.click(locator)
        self.capture_step("apply_promo", f"Applied promo{f' {name}' if name else ''}")

    def is_promo_applied(self, name: str | None = None) -> bool:
        return self.is_visible(L.button_remove_promo, timeout=5)
    

    def remove_promo(self):
        self.click(L.button_remove_promo)
        self.capture_step("remove_promo")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("promo_back")

    # ================= "Add a Promo Code" dialog =================
    def open_add_promo_code(self):
        self.click(L.button_add_promo_code)
        self.capture_step("open_add_promo")

    def verify_add_promo_dialog(self):
        assert self.is_visible(L.input_promo_code, timeout=15), "Add a Promo Code dialog not shown"
        self.capture_step("add_promo_dialog")

    def enter_promo_code(self, code: str):
        self.type_text(L.input_promo_code, code)
        self.capture_step("promo_code", f"Entered promo code '{code}'")

    def submit_promo_code(self):
        self.click(L.button_submit_promo)
        self.capture_step("submit_promo")

    def add_promo_code(self, code: str):
        self.open_add_promo_code()
        self.enter_promo_code(code)
        self.submit_promo_code()
