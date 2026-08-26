from core.android_base_page import AndroidBasePage
from locators.events.bottomsheet_add_player_locators import BottomsheetAddPlayerLocators as L


class BottomsheetAddPlayerPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.title_bottomsheet, timeout=20), (
            "Add a player bottom sheet not shown"
        )
        self.capture_step("add_player_sheet", "Add a player bottom sheet shown")

    def verify_player_added(self, name: str):
        if self.is_visible(L.button_close_bottomsheet_switch_to_group_registration):
            self.press_back()
        self.capture_step("add_player_done", f"Player selected: {name}")

    # ================= action steps =================
    def search_friend(self, name: str):
        self.type_text(L.input_search_friend_name, name)
        self.capture_step("add_player_search", f"Searched friend: {name}")

    def select_player(self, name: str):
        self.click(L.button_option_player_name_static)
        self.capture_step("add_player_select", f"Selected player: {name}")
