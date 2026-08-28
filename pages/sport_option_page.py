from core.android_base_page import AndroidBasePage
from locators.sport_option_locators import SportOptionLocators as L


class SportOptionPage(AndroidBasePage):

    SPORTS = {
        "Golf": "GOLF",
        "Billiard": "BILLIARD",
        "Padel": "PADEL",
        "Badminton": "BADMINTON",
        "Tennis": "TENNIS",
        "Basketball": "BASKETBALL",
        "Football": "FOOTBALL",
        "Volleyball": "VOLLEYBALL",
        "Running": "RUNNING",
        "Table Tennis": "TABLE_TENNIS",
    }

    AVAILABLE_SPORTS = ["Golf", "Padel", "Running", "Table Tennis"]
    BETA_SPORTS = ["Billiard"]
    COMING_SOON_SPORTS = ["Badminton", "Tennis", "Basketball", "Football", "Volleyball"]

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.label_title, timeout=20), \
            "'So, what are we playing today?' screen not shown"
        self.capture_step("sport_option")

    def get_title(self) -> str:
        return self.find(L.label_title).get_attribute("content-desc") or ""

    def get_sports(self) -> list:
        return [
            e.get_attribute("content-desc") or ""
            for e in self.find_all(L.cards_all)
        ]

    def verify_sports(self, expected: list | None = None):
        expected = expected or list(self.SPORTS)
        actual = self.get_sports()
        missing = [name for name in expected if name not in actual]
        self.capture_step(
            "sport_option_cards",
            f"{len(actual)} sport card(s) shown",
            data={"sports": actual},
        )
        assert not missing, f"Sport card(s) not shown: {missing}"

    def is_sport_visible(self, sport: str) -> bool:
        return self.is_visible_after_scroll(L.card_by_code % self.SPORTS[sport])

    def has_beta_badge(self, sport: str) -> bool:
        return self.is_visible(L.badge_beta_in_card % self.SPORTS[sport], timeout=5)

    def has_coming_soon_badge(self, sport: str) -> bool:
        return self.is_visible(L.badge_coming_soon_in_card % self.SPORTS[sport], timeout=5)

    def verify_badges(self):
        beta = [s for s in self.BETA_SPORTS if not self.has_beta_badge(s)]
        coming_soon = [s for s in self.COMING_SOON_SPORTS if not self.has_coming_soon_badge(s)]
        self.capture_step("sport_option_badges")
        assert not beta, f"BETA badge not shown on: {beta}"
        assert not coming_soon, f"COMING SOON badge not shown on: {coming_soon}"

    # ================= action steps =================
    def select_sport(self, sport: str):
        locator = L.card_by_code % self.SPORTS[sport]
        self.scroll_to_element(locator)
        self.click(locator)
        self.capture_step("sport_selected", f"Selected sport '{sport}'")

