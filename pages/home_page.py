from core.android_base_page import AndroidBasePage
from locators.home_locators import HomeLocators as L


class HomePage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        assert self.is_visible(L.tab_home, timeout=20), "Home screen not shown"
        self.capture_step("home_screen", "Home screen is visible")

    def is_loaded(self) -> bool:
        return self.is_visible(L.tab_home, timeout=20)

    def verify_greeting_for(self, name: str):
        greeting = self.get_text(L.label_greeting) or ""
        # content-desc holds the label; read it if text is empty
        if not greeting:
            greeting = self.find(L.label_greeting).get_attribute("content-desc") or ""
        self.capture_step("home_greeting", f"Greeting: {greeting}")
        assert name in greeting, f"Greeting '{greeting}' does not mention '{name}'"

    # ================= quick actions =================
    def open_tee_time(self):
        self.click(L.action_tee_time)
        self.capture_step("open_tee_time", "Opened Tee time")

    def open_driving_range(self):
        self.click(L.action_driving_range)
        self.capture_step("open_driving_range", "Opened Driving range")

    def open_events(self):
        self.click(L.action_events)
        self.capture_step("open_events", "Opened Events")

    def open_marketplace(self):
        self.click(L.action_marketplace)
        self.capture_step("open_marketplace", "Opened Marketplace")

    # ================= header =================
    def tap_search(self):
        self.click(L.search_bar)
        self.capture_step("tap_search", "Tapped search bar")

    # ================= swing credits =================
    def get_credits(self) -> str:
        return self.scroll_and_find(L.label_credits).get_attribute("content-desc") or ""

    def open_swing_credits(self):
        self.click(L.label_credits)
        self.capture_step("open_swing_credits", "Opened Swing Credits")
    
    # ============= region =============
    def tap_select_region(self):
        self.click(L.region_selector)
        self.capture_step("tap select region", "Tap Select Region")
    
    def verify_bottom_sheet_select_region(self):
        assert self.is_visible(L.title_select_region, timeout=20), "Bottom Sheet Select Region is not shown"
        self.capture_step("select_region", "Verify Bottom Sheet Select Region")
    
    def close_bottom_sheet_select_region(self):
        self.click(L.button_close_bottom_sheet_select_region)
        self.capture_step("close_bottom_sheet", "Close Bottom Sheet Select Region")
    
    def select_region(self, region_name: str):
        self.click(L.label_region % region_name)
        self.capture_step(f"tap region : {region_name} ", f"Tap Region: {region_name}")
        

    # ================= explore: golf courses =================
    def scroll_to_courses(self):
        self.scroll_to_text("Explore golf")
        self.capture_step("scroll_courses", "Scrolled to golf courses section")

    def tap_see_all_courses(self):
        self.click(L.see_all_courses)
        self.capture_step("see_all_courses", "Tapped See all (golf courses)")

    def open_course(self, name: str):
        self.click(L.course_card_by_name % name)
        self.capture_step("open_course", f"Opened course '{name}'")

    # ================= explore: driving ranges =================
    def scroll_to_ranges(self):
        self.scroll_to_text("Explore driving")
        self.capture_step("scroll_ranges", "Scrolled to driving ranges section")

    def verify_ranges_section(self):
        assert self.is_visible(L.label_explore_ranges_title, timeout=15), "Driving ranges section not shown"
        self.capture_step("ranges_section", "Driving ranges section is visible")

    def tap_see_all_ranges(self):
        self.click(L.see_all_ranges)
        self.capture_step("see_all_ranges", "Tapped See all (driving ranges)")

    def open_range(self, name: str):
        self.click(L.range_card_by_name % name)
        self.capture_step("open_range", f"Opened driving range '{name}'")

    # ================= refer a friend =================
    def tap_refer_friend(self):
        self.click(L.button_refer_friend)
        self.capture_step("refer_friend", "Tapped Refer a friend")
    
    def tap_join_swing_pass(self):
        self.click(L.button_join_swing_pass)
        self.capture_step("Open Swing Pass Page")

    # ================= swing pass =================
    def has_swing_pass(self) -> bool:
        return self.find_anywhere(L.card_swing_pass) is not None

    def open_swing_pass(self):
        self.click(L.card_swing_pass)
        self.capture_step("open_swing_pass", "Opened Swing Pass")
        
    def open_swing_credits(self):
        self.click(L.label_credits)
        self.capture_step("Open Swing Credits")

    # ================= need help / call center =================
    def tap_call_center(self):
        self.click(L.link_call_center)
        self.capture_step("call_center", "Tapped Go to call center")

    # ================= footer cards =================
    def open_whats_new(self):
        self.click(L.card_whats_new)
        self.capture_step("whats_new", "Opened What's new")

    def open_give_feedback(self):
        self.click(L.card_give_feedback)
        self.capture_step("give_feedback", "Opened Give us feedback")

    def open_follow_instagram(self):
        self.click(L.card_follow_instagram)
        self.capture_step("follow_instagram", "Opened Follow us on Instagram")

    def open_leave_rating(self):
        self.click(L.card_leave_rating)
        self.capture_step("leave_rating", "Opened Leave a rating")

    def open_request_venue(self):
        self.click(L.card_request_venue)
        self.capture_step("request_venue", "Opened Request a golf venue")

    def open_contact_support(self):
        self.click(L.card_contact_support)
        self.capture_step("contact_support", "Opened Contact Swing support")

    # ================= bottom navigation =================
    def go_to_home(self):
        self.click(L.tab_home)
        self.capture_step("nav_home", "Navigated to Home tab")

    def go_to_activity(self):
        self.click(L.tab_activity)
        self.capture_step("nav_activity", "Navigated to Activity tab")

    def go_to_account(self):
        self.click(L.tab_account)
        self.capture_step("nav_account", "Navigated to Account tab")
