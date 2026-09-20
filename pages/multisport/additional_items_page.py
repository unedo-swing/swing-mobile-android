"""
Additional items page object (Android).

Shown after confirming schedules on the booking confirmation screen.
The caller picks a schedule card, adds additional items (e.g. BALLS),
sets the quantity, then saves & confirms — returning to booking
confirmation with the extra items added.
"""

from core.android_base_page import AndroidBasePage
from locators.multisport.additional_items_page_locators import (
    AdditionalItemsPageLocators as L,
)


class AdditionalItemsPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.header_page_title, timeout=20), \
            "Additional items page not shown"
        self.capture_step("additional_items_screen",
                          "Additional items screen is visible")

    def verify_selected_additional_items(self, item_name: str):
        self.wait_until_loaded()
        assert self.is_visible(L.button_edit_additional_items % item_name, timeout=10), \
            f"Additional item '{item_name}' not selected"
        self.capture_step("additional_items_selected",
                          f"Additional item selected: {item_name}")

    def verify_removed_additional_items(self, item_name: str):
        self.wait_until_loaded()
        assert self.is_visible(L.button_add_additional_items % item_name, timeout=10), \
            f"Additional item '{item_name}' not removed"
        self.capture_step("additional_items_removed",
                          f"Additional item removed: {item_name}")

    # ================= pick an item =================
    def pick_item(self, item_name: str):
        locator = L.button_add_additional_items % item_name
        self.click(locator)
        self.capture_step("pick_item", f"Picked item: {item_name}")

    def edit_item(self, item_name: str):
        locator = L.button_edit_additional_items % item_name
        self.click(locator)
        self.capture_step("edit_item", f"Edited item: {item_name}")

    # ================= add / remove item =================
    def add_item(self):
        locator = L.button_plus_additional_items
        self.click(locator)
        self.capture_step("add_item", f"Added one")

    def remove_item(self):
        locator = L.button_minus_additional_items
        self.click(locator)
        self.capture_step("remove_item", f"Removed one")

    # ================= save & confirm =================
    def save_items(self):
        self.click(L.button_save_additional_items)
        self.capture_step("save_items", "Tapped Save items")

    def confirm_items(self):
        self.click(L.button_confirm_additional_items)
        self.capture_step("confirm_items", "Tapped Confirm additional items")

    def skip_items(self):
        self.click(L.button_skip_additional_items)
        self.capture_step("skip_items", "Tapped Skip additional items")
