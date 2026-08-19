from core.android_base_page import AndroidBasePage
from locators.tee_time.add_player_locators import AddPlayerLocators as L


class AddPlayerPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.label_title, timeout=20), "Add a player sheet not shown"
        self.capture_step("add_player", "Add a player sheet is visible")

    def is_save_enabled(self) -> bool:
        return self.is_enabled(L.button_save_player)

    # ================= tabs =================
    def select_search_friend_tab(self):
        self.click(L.tab_search_friend)
        self.capture_step("tab_search_friend", "Selected 'Search a friend' tab")

    def select_add_manually_tab(self):
        self.click(L.tab_add_manually)
        self.capture_step("tab_add_manually", "Selected 'Add manually' tab")

    # ================= tab 1: search a friend =================
    def search_friend(self, query: str):
        self.type_text(L.input_search_friend, query)
        self.press_search()
        self.capture_step("search_friend", f"Searched friend '{query}'")

    def select_friend_result(self, name: str):
        self.click(L.friend_result_by_name % name)
        self.capture_step("select_friend", f"Selected friend '{name}'")

    # ================= tab 2: add manually =================
    def tap_add_from_contacts(self):
        self.click(L.link_add_from_contacts)
        self.capture_step("add_from_contacts", "Tapped Add from contacts")

    def enter_first_name(self, name: str):
        self.fill(L.input_first_name, name)
        self.capture_step("first_name", f"Entered first name '{name}'")

    def enter_last_name(self, name: str):
        self.fill(L.input_last_name, name)
        self.capture_step("last_name", f"Entered last name '{name}'")

    def open_country_picker(self):
        self.click(L.button_country)
        self.capture_step("player_country", "Opened country picker")

    def enter_phone(self, phone: str):
        self.fill_verified(L.input_phone, phone)
        self.capture_step("player_phone", f"Entered phone '{phone}'")

    def enter_email(self, email: str):
        self.fill(L.input_email, email)
        self.capture_step("player_email", f"Entered email '{email}'")

    def fill_manually(self, first_name: str, last_name: str, phone: str, email: str | None = None):
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_phone(phone)
        if email:
            self.enter_email(email)

    # ================= submit =================
    def tap_save_player(self):
        self.click(L.button_save_player)
        self.capture_step("save_player", "Tapped Save player")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("add_player_back", "Tapped back")
