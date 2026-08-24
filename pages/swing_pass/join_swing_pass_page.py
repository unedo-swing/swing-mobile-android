from core.android_base_page import AndroidBasePage
from locators.swing_pass.join_swing_pass_locators import JoinSwingPassLocators as L


class JoinSwingPassPage(AndroidBasePage):

    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "Join Swing Pass screen not shown"
        self.capture_step("join_pass")

    def verify_plan_listed(self, duration: str):
        assert self.find_anywhere(L.plan_by_duration % duration) is not None, \
            f"Plan '{duration}' not listed"
        self.capture_step("join_pass_plan_listed", f"Plan '{duration}' is listed")

    def verify_plan_not_listed(self, duration: str):
        assert self.find_anywhere(L.plan_by_duration % duration) is None, \
            f"Plan '{duration}' is listed but should not be"
        self.capture_step("join_pass_plan_absent", f"Plan '{duration}' is not listed")

    def verify_plan_selected(self, duration: str):
        assert self.is_plan_selected(duration), f"Plan '{duration}' is not selected"
        self.capture_step("join_pass_plan_selected", f"Plan '{duration}' is selected")

    def verify_summary(self, price: str = "", duration: str = ""):
        summary = self.get_summary()
        for label, want, got in (("price", price, summary["price"]),
                                 ("duration", duration, summary["duration"])):
            if want:
                assert want == got, f"Summary {label} is '{got}', expected '{want}'"

    def verify_billing_method(self, expected: str):
        actual = self.get_billing_method()
        assert actual == expected, f"Billing method is '{actual}', expected '{expected}'"

    def verify_method_not_selected(self):
        actual = self.get_billing_method()
        assert actual == L.PLACEHOLDER_METHOD, \
            f"A billing method is already picked: '{actual}'"

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

    @staticmethod
    def parse_summary(desc: str) -> dict:
        lines = [line.strip() for line in (desc or "").split("\n") if line.strip()]
        summary = {"price": "", "duration": "", "label": desc or ""}
        if lines:
            summary["price"] = lines[0]
        if len(lines) >= 2:
            summary["duration"] = lines[1].replace("for", "", 1).strip()
        return summary

    def _desc(self, locator) -> str:
        return self.scroll_and_find(locator).get_attribute("content-desc") or ""

    def get_summary(self) -> dict:
        summary = self.parse_summary(self._desc(L.label_summary))
        self.capture_step("join_pass_summary",
                          f"{summary['price']} for {summary['duration']}", data=summary)
        return summary

    def get_plans(self) -> list:
        plans = [
            self.parse_plan(e.get_attribute("content-desc") or "")
            for e in self.find_all(L.plan_any)
        ]
        self.capture_step("join_pass_plans", f"{len(plans)} plan(s) listed",
                          data={"plans": plans})
        return plans

    def get_plan(self, duration: str) -> dict:
        element = self.find_anywhere(L.plan_by_duration % duration)
        assert element is not None, f"Plan '{duration}' not listed"
        plan = self.parse_plan(element.get_attribute("content-desc") or "")
        self.capture_step("join_pass_plan", f"Plan '{duration}'", data=plan)
        return plan

    def get_selected_plan(self) -> dict:
        plan = self.parse_plan(self._desc(L.plan_selected))
        self.capture_step("join_pass_selection", f"Selected: {plan['duration']}", data=plan)
        return plan

    def get_most_popular_plan(self) -> dict:
        plan = self.parse_plan(self._desc(L.plan_most_popular))
        self.capture_step("join_pass_most_popular", plan["duration"], data=plan)
        return plan

    def is_plan_selected(self, duration: str) -> bool:
        radio = self.scroll_and_find(L.radio_by_duration % duration)
        return radio.get_attribute("checked") == "true"

    def get_billing_method(self) -> str:
        method = self._desc(L.row_method)
        self.capture_step("join_pass_method", method)
        return method

    def is_terms_accepted(self) -> bool:
        return self.scroll_and_find(L.checkbox_terms).get_attribute("checked") == "true"

    def select_plan(self, duration: str):
        self.click(L.plan_by_duration % duration)
        assert self.is_plan_selected(duration), \
            f"Tapped plan '{duration}' but its radio did not turn on"
        self.capture_step("join_pass_select_plan", f"Selected plan '{duration}'")

    def open_billing_method(self):
        self.click(L.button_select_method)
        self.capture_step("join_pass_open_method")

    def tap_add_promo(self):
        self.click(L.button_add_promo)
        self.capture_step("join_pass_add_promo")

    def toggle_terms(self):
        self.click(L.checkbox_terms)
        self.capture_step("join_pass_terms_toggled")

    def set_terms(self, accepted: bool = True):
        if self.is_terms_accepted() == accepted:
            self.capture_step("join_pass_terms",
                              f"Terms already {'accepted' if accepted else 'not accepted'}")
            return
        self.toggle_terms()
        actual = self.is_terms_accepted()
        assert actual == accepted, f"Terms checkbox is {actual}, expected {accepted}"

    def accept_terms(self):
        self.set_terms(True)

    def open_terms(self):
        self.click(L.link_terms)
        self.capture_step("join_pass_open_terms")

    def slide_to_confirm(self):
        self.slide_to_end(L.slider_confirm, L.slider_thumb)
        self.wait_until_loaded()
        self.capture_step("join_pass_confirm")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("join_pass_back")
