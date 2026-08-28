from core.android_base_page import AndroidBasePage
from locators.home_locators import HomeLocators as L


class HomePage(AndroidBasePage):

    # ================= verify Page =================
    def verify_button_sport_icon(self, sport_type: str = "Golf"):
        assert self.is_visible(L.button_icon_sport_type % sport_type), "Sport Icon is Missing"
        self.capture_step(f"Button Sport {sport_type} is Show")
    
    def verify_button_region_select(self, region: str):
        assert self.is_visible(L.region_selector), "Regions Selector is Missing"
        assert self._desc(L.region_selector) == region, "Region Selected is Wrong"
        self.capture_step(f"Selected Region {region} is Visible")
    
    def verify_screen(self, sport_type: str, region: str):
        self.verify_button_sport_icon(sport_type)
        if sport_type == "Golf":
            self.verify_button_region_select(region)
    
    def is_loaded_home_screen(self, timeout: int = 5):
        self.wait_for(timeout)
        self.capture_step(f"Wait Until Home is Loaded For {timeout} seconds")
            

    # ================= quick actions =================
    def open_tee_time(self):
        self.click(L.action_tee_time)
        self.capture_step("open_tee_time")

    def open_driving_range(self):
        self.click(L.action_driving_range)
        self.capture_step("open_driving_range")

    def open_events(self):
        self.click(L.action_events)
        self.capture_step("open_events")

    def open_marketplace(self):
        self.click(L.action_marketplace)
        self.capture_step("open_marketplace")

    # ================= header =================
    def tap_search(self):
        self.click(L.search_bar)
        self.capture_step("tap_search")

    # ================= swing credits =================
    def get_credits(self) -> str:
        return self.scroll_and_find(L.label_credits).get_attribute("content-desc") or ""

    def open_swing_credits(self):
        self.go_to_home()
        self.click(L.label_credits)
        self.capture_step("open_swing_credits")
    
    # ============= region =============
    def tap_select_region(self):
        self.wait_for(5)
        self.click(L.region_selector)
        self.capture_step("tap select region")
    
    def verify_bottom_sheet_select_region(self):
        assert self.is_visible(L.title_select_region, timeout=20), "Bottom Sheet Select Region is not shown"
        self.capture_step("select_region")
    
    def close_bottom_sheet_select_region(self):
        self.click(L.button_close_bottom_sheet_select_region)
        self.capture_step("close_bottom_sheet")
    
    def select_region(self, region: str):
        if region == "ID":
            country = "Indonesia"
        elif region == "MY":
            country = "Malaysia"
        else:
            country = "Indonesia"
        self.click(L.label_region % country)
        self.capture_step(f"tap region : {country} ", f"Tap Region: {country}")
        

    # ================= explore: golf courses =================
    def scroll_to_courses(self):
        self.scroll_to_text("Explore golf")
        self.capture_step("scroll_courses")

    def tap_see_all_courses(self):
        self.click(L.see_all_courses)
        self.capture_step("see_all_courses")

    def open_course(self, name: str):
        self.click(L.course_card_by_name % name)
        self.capture_step("open_course", f"Opened course '{name}'")

    # ================= explore: driving ranges =================
    def scroll_to_ranges(self):
        self.scroll_to_text("Explore driving")
        self.capture_step("scroll_ranges")

    def verify_ranges_section(self):
        assert self.is_visible(L.label_explore_ranges_title, timeout=15), "Driving ranges section not shown"
        self.capture_step("ranges_section")

    def tap_see_all_ranges(self):
        self.click(L.see_all_ranges)
        self.capture_step("see_all_ranges")

    def open_range(self, name: str):
        self.click(L.range_card_by_name % name)
        self.capture_step("open_range", f"Opened driving range '{name}'")

    # ================= refer a friend =================
    def tap_refer_friend(self):
        self.click(L.button_refer_friend)
        self.capture_step("refer_friend")
    
    def tap_join_swing_pass(self):
        self.click(L.button_join_swing_pass)
        self.capture_step("Open Swing Pass Page")

    # ================= swing pass =================
    def has_swing_pass(self) -> bool:
        return self.find_anywhere(L.card_swing_pass) is not None

    def open_swing_pass(self):
        self.wait_visible(L.card_swing_pass)
        self.click(L.card_swing_pass)
        self.capture_step("open_swing_pass")
        

    # ================= need help / call center =================
    def tap_call_center(self):
        self.click(L.link_call_center)
        self.capture_step("call_center")

    # ================= footer cards =================
    def open_whats_new(self):
        self.click(L.card_whats_new)
        self.capture_step("whats_new")

    def open_give_feedback(self):
        self.click(L.card_give_feedback)
        self.capture_step("give_feedback")

    def open_follow_instagram(self):
        self.click(L.card_follow_instagram)
        self.capture_step("follow_instagram")

    def open_leave_rating(self):
        self.click(L.card_leave_rating)
        self.capture_step("leave_rating")

    def open_request_venue(self):
        self.click(L.card_request_venue)
        self.capture_step("request_venue")

    def open_contact_support(self):
        self.click(L.card_contact_support)
        self.capture_step("contact_support")

    # ================= bottom navigation =================
    def go_to_home(self):
        self.click(L.tab_home)
        self.capture_step("nav_home")

    def go_to_activity(self):
        self.click(L.tab_activity)
        self.capture_step("nav_activity")

    def go_to_account(self):
        self.click(L.tab_account)
        self.capture_step("nav_account")
