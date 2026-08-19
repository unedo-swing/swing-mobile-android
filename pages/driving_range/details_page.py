from core.android_base_page import AndroidBasePage
from locators.driving_range.details_locators import DrivingRangeDetailsLocators as L


class DrivingRangeDetailsPage(AndroidBasePage):

    # ================= helpers =================
    def _desc(self, locator) -> str:
        return self.find(locator).get_attribute("content-desc") or ""

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "Driving range details screen not shown"
        self.capture_step("dr_details", "Driving range details screen is visible")

    def verify_range_name(self, name: str):
        assert self.is_visible(L.label_range_name % name), f"Range '{name}' not shown"
        self.capture_step("dr_range_name", f"Range name shown: {name}")

    def verify_slots_loaded(self):
        assert self.wait_until_loaded(), "Driving range slots still loading"
        self.capture_step("dr_slots_loaded", "Time slots finished loading")

    def verify_book_enabled(self):
        assert self.is_book_enabled(), "Book driving range is disabled"
        self.capture_step("dr_book_enabled", "Book driving range is enabled")

    # ================= header =================
    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("dr_details_back", "Tapped back")

    def tap_share(self):
        self.click(L.button_share)
        self.capture_step("dr_details_share", "Tapped share")

    # ================= gallery =================
    def verify_gallery(self):
        assert self.is_visible(L.gallery_image, timeout=15), "Range image gallery not shown"
        self.capture_step("dr_gallery", "Image gallery is visible")

    def tap_gallery_image(self):
        self.click(L.gallery_image)
        self.capture_step("dr_gallery_tap", "Tapped the range image")

    def has_gallery_indicator(self) -> bool:
        return self.is_visible(L.gallery_indicator, timeout=5)

    # ================= location line =================
    def get_city(self) -> str:
        return self._desc(L.label_city)

    def get_distance(self) -> str:
        return self._desc(L.label_distance)

    def tap_distance(self):
        self.click(L.button_distance)
        self.capture_step("dr_distance", "Tapped the distance shortcut")

    # ================= promos =================
    def tap_promo(self, name: str):
        self.click(L.promo_by_name % name)
        self.capture_step("dr_promo", f"Tapped promo '{name}'")

    def get_promo_names(self) -> list:
        """Promo card titles, i.e. the first line of each card's content-desc."""
        return [
            (e.get_attribute("content-desc") or "").split("\n")[0]
            for e in self.find_all(L.promo_cards)
        ]

    def verify_promo(self, name: str):
        assert self.is_visible(L.promo_by_name % name), f"Promo '{name}' not shown"
        self.capture_step("dr_promo_shown", f"Promo '{name}' is shown")

    def verify_promo_active(self, name: str):
        assert self.is_visible(L.badge_active_by_promo % name), f"Promo '{name}' is not active"
        self.capture_step("dr_promo_active", f"Promo '{name}' carries the Active badge")

    def tap_promo_card(self, name: str):
        """Tap the clickable wrapper around a promo card (the card itself is inert)."""
        self.click(L.button_promo_by_name % name)
        self.capture_step("dr_promo_card", f"Opened promo '{name}'")

    def verify_promo_join(self, name: str):
        assert self.is_visible(L.badge_join_by_promo % name), f"Promo '{name}' has no Join badge"
        self.capture_step("dr_promo_join", f"Promo '{name}' carries the Join badge")

    # ----- featured promo strip: "See all" is the tile past the last promo,
    #       so it is only rendered once the strip is swiped left -----
    def swipe_promo_left(self):
        self.swipe_left_in(L.promo_carousel)
        self.capture_step("dr_promo_swipe", "Swiped the promo strip left")

    def reveal_see_all_promo(self, max_swipes: int = 5) -> bool:
        return self.swipe_left_to_element(
            L.button_see_all_featured_promo, L.promo_carousel, max_swipes
        )

    def verify_see_all_promo(self):
        assert self.reveal_see_all_promo(), "'See all' not shown after swiping the promo strip"
        self.capture_step("dr_promo_see_all", "'See all' is visible at the end of the promo strip")

    def tap_see_all_promo(self):
        self.verify_see_all_promo()
        self.click(L.button_see_all_featured_promo)
        self.capture_step("dr_promo_see_all_tap", "Tapped 'See all' on the promo strip")

    def verify_cashback_banner(self):
        assert self.is_visible(L.banner_cashback, timeout=10), "Cashback banner not shown"
        self.capture_step("dr_cashback", "Cashback banner is visible")

    def tap_cashback_banner(self):
        self.click(L.banner_cashback)
        self.capture_step("dr_cashback_tap", "Tapped the cashback banner")

    # ================= date / bay / time =================
    def select_date(self, name: str,date_text: str):
        self.click(L.button_calender % name)
        self.click(L.button_date_in_calender % date_text)
        self.capture_step("dr_select_date", f"Selected date '{date_text}'")

    def select_bay_tab(self, name: str):
        if name != "":
            self.click(L.bay_tab_by_name % name)
            self.capture_step("dr_bay_tab", f"Selected bay '{name}'")

    def select_time(self, time_start: str, time_end: str):
        from datetime import datetime, timedelta

        fmt = "%H:%M"
        current = datetime.strptime(time_start.strip(), fmt)
        end = datetime.strptime(time_end.strip(), fmt)
        if end < current:
            raise ValueError(
                f"time end '{time_end}' must be at or after start '{time_start}'"
            )
        while current <= end:
            slot = current.strftime(fmt)
            self.click(L.time_by_text % slot)
            self.capture_step("dr_select_time", f"Selected time slot '{slot}'")
            current += timedelta(minutes=60)

    def get_available_dates(self) -> list:
        """Every date chip in the strip, as shown: e.g. 'TUE\n18 Aug'."""
        return [e.get_attribute("content-desc") or "" for e in self.find_all(L.dates_all)]

    def select_date_in_strip(self, date_text: str):
        """Pick a date straight from the strip, without opening the calendar."""
        self.click(L.date_by_text % date_text)
        self.capture_step("dr_select_date_strip", f"Selected date '{date_text}' from the strip")

    def get_selected_bay(self) -> str:
        return self._desc(L.bay_tab_selected).split("\n")[0]

    def verify_bay_tab_selected(self, name: str):
        assert self.is_visible(L.bay_tab_selected_by_name % name), f"Bay tab '{name}' is not selected"
        self.capture_step("dr_bay_selected", f"Bay tab '{name}' is selected")

    def get_available_times(self) -> list:
        return [e.get_attribute("content-desc") or "" for e in self.find_all(L.time_slots_all)]

    def verify_time_available(self, slot: str):
        assert self.is_visible(L.time_slot_by_text % slot), f"Time slot '{slot}' not shown"
        self.capture_step("dr_time_available", f"Time slot '{slot}' is available")

    # ================= rates & prices =================
    def get_rate(self, duration_label: str) -> str:
        return self.find(L.rate_card_by_duration % duration_label).get_attribute("content-desc") or ""

    def tap_see_pricelist(self):
        self.click(L.button_see_pricelist)
        self.capture_step("dr_pricelist", "Tapped See complete pricelist")

    # ================= summary / location =================
    def get_booking_summary(self) -> str:
        return self.find(L.label_booking_summary).get_attribute("content-desc") or ""

    def verify_location_section(self):
        self.scroll_to_text("Location")
        assert self.is_visible(L.label_location_section, timeout=15), "Location section not shown"
        self.capture_step("dr_location", "Location section is visible")

    def tap_view_on_maps(self):
        self.click(L.button_view_on_maps)
        self.capture_step("dr_view_maps", "Tapped View on Google Maps")

    # ================= book =================
    def is_book_enabled(self) -> bool:
        return self.is_enabled(L.button_book)

    def tap_book(self):
        self.click(L.button_book)
        self.capture_step("dr_book", "Tapped Book driving range")

    def verify_book_disabled(self):
        assert self.is_visible(L.button_book_disabled, timeout=10), "Book driving range is enabled"
        self.capture_step("dr_book_disabled", "Book driving range is disabled")
