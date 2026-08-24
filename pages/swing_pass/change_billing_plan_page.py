from core.android_base_page import AndroidBasePage
from locators.swing_pass.change_billing_plan_locators import ChangeBillingPlanLocators as L


class ChangeBillingPlanPage(AndroidBasePage):

    FIELDS = {
        "player_name": L.FIELD_PLAYER_NAME,
        "renew_date": L.FIELD_RENEW_DATE,
        "membership_id": L.FIELD_MEMBERSHIP_ID,
    }

    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "Change billing plan screen not shown"
        self.capture_step("change_plan")

    def verify_plan_listed(self, duration: str):
        assert self.find_anywhere(L.plan_by_duration % duration) is not None, \
            f"Plan '{duration}' not listed"
        self.capture_step("change_plan_listed", f"Plan '{duration}' is listed")

    def verify_plan_selected(self, duration: str):
        assert self.is_plan_selected(duration), f"Plan '{duration}' is not selected"
        self.capture_step("change_plan_selected", f"Plan '{duration}' is selected")

    def verify_current_plan(self, duration: str):
        actual = self.get_current_plan()["duration"]
        assert actual == duration, f"Current plan is '{actual}', expected '{duration}'"

    def verify_terms_accepted(self, accepted: bool = True):
        actual = self.is_terms_accepted()
        assert actual == accepted, \
            f"Terms checkbox is {'on' if actual else 'off'}, expected {'on' if accepted else 'off'}"

    @staticmethod
    def parse_plan(desc: str) -> dict:
        lines = [line.strip() for line in (desc or "").split("\n") if line.strip()]
        plan = {"badge": "", "duration": "", "price": "", "original_price": "",
                "label": desc or ""}
        prices = [line for line in lines if line.startswith("Rp.")]
        durations = [line for line in lines if "month" in line and not line.startswith("Rp.")]
        if durations:
            plan["duration"] = durations[0]
            index = lines.index(durations[0])
            if index:
                plan["badge"] = lines[0]
        if len(prices) >= 2:
            plan["original_price"] = prices[0]
            plan["price"] = prices[1]
        elif prices:
            plan["price"] = prices[0]
        return plan

    def _desc(self, locator) -> str:
        return self.scroll_and_find(locator).get_attribute("content-desc") or ""

    def get_field(self, label: str) -> str:
        return self._desc(L.value_by_label % label)

    def get_details(self) -> dict:
        details = {key: self.get_field(label) for key, label in self.FIELDS.items()}
        self.capture_step("change_plan_details",
                          f"{details['membership_id']} renews {details['renew_date']}",
                          data=details)
        return details

    def get_plans(self) -> list:
        plans = [
            self.parse_plan(e.get_attribute("content-desc") or "")
            for e in self.find_all(L.plan_any)
        ]
        self.capture_step("change_plan_options", f"{len(plans)} plan(s) listed",
                          data={"plans": plans})
        return plans

    def get_current_plan(self) -> dict:
        plan = self.parse_plan(self._desc(L.plan_current))
        self.capture_step("change_plan_current", f"Current plan: {plan['duration']}", data=plan)
        return plan

    def get_selected_plan(self) -> dict:
        plan = self.parse_plan(self._desc(L.plan_selected))
        self.capture_step("change_plan_selection", f"Selected: {plan['duration']}", data=plan)
        return plan

    def get_plan(self, duration: str) -> dict:
        element = self.find_anywhere(L.plan_by_duration % duration)
        assert element is not None, f"Plan '{duration}' not listed"
        plan = self.parse_plan(element.get_attribute("content-desc") or "")
        self.capture_step("change_plan_option", f"Plan '{duration}'", data=plan)
        return plan

    def is_plan_selected(self, duration: str) -> bool:
        radio = self.scroll_and_find(L.radio_by_duration % duration)
        return radio.get_attribute("checked") == "true"

    def get_start_note(self) -> str:
        note = self._desc(L.label_start_note)
        self.capture_step("change_plan_note", note)
        return note

    def is_terms_accepted(self) -> bool:
        return self.scroll_and_find(L.checkbox_terms).get_attribute("checked") == "true"

    def select_plan(self, duration: str):
        self.click(L.plan_by_duration % duration)
        assert self.is_plan_selected(duration), \
            f"Tapped plan '{duration}' but its radio did not turn on"
        self.capture_step("change_plan_select", f"Selected plan '{duration}'")

    def toggle_terms(self):
        self.click(L.checkbox_terms)
        self.capture_step("change_plan_terms_toggled")

    def set_terms(self, accepted: bool = True):
        if self.is_terms_accepted() == accepted:
            self.capture_step("change_plan_terms",
                              f"Terms already {'accepted' if accepted else 'not accepted'}")
            return
        self.toggle_terms()
        actual = self.is_terms_accepted()
        assert actual == accepted, f"Terms checkbox is {actual}, expected {accepted}"

    def accept_terms(self):
        self.set_terms(True)

    def open_terms(self):
        self.click(L.link_terms)
        self.capture_step("change_plan_open_terms")

    def slide_to_confirm(self):
        self.slide_to_end(L.slider_confirm, L.slider_thumb)
        self.wait_until_loaded()
        self.capture_step("change_plan_confirm")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("change_plan_back")
