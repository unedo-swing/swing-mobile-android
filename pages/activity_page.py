from locators.activity_locators import ActivityLocators as L
from core.android_base_page import AndroidBasePage

class ActivityPage(AndroidBasePage):
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_activity, timeout=10), "Activity screen not shown"
        self.capture_step("Verify Activity Page")
    
    def click_filter_activity(self, type_filter: str):
        match type_filter:
            case "Driving range":
                self.click(L.label_filter_driving_range)
            case "Tee time":
                self.click(L.label_filter_tee_time)
            case "Event":
                self.click(L.label_filter_event)
            case "Marketplace":
                self.click(L.label_filter_marketplace)
        self.capture_step(f"Tap Filter {type_filter}")
    
    def click_card_activity(self, name: str, time_start: str, booking_date: str):
        self.click(L.card_activity % (name, time_start, booking_date))
        self.capture_step("Tap Card Activity")
    
    