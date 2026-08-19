from core.android_base_page import AndroidBasePage
from locators.swing_pass.swing_pass_locators import SwingPassLocators as L


class SwingPassPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "Swing Pass screen not shown"
        self.capture_step("swing_pass", "Swing Pass screen is visible")

    def verify_active_membership(self):
        card = self.get_membership()
        assert card["valid_until"], \
            f"Membership card does not show an active period: {card['label']!r}"
        self.capture_step("swing_pass_active",
                          f"Active until {card['valid_until']}", data=card)

    def verify_pass_id(self, expected: str):
        actual = self.get_membership()["pass_id"]
        assert actual == expected, f"Pass ID is '{actual}', expected '{expected}'"

    def verify_member_name(self, expected: str):
        actual = self.get_membership()["name"]
        assert actual == expected, f"Card name is '{actual}', expected '{expected}'"

    def verify_renews_on(self, expected: str):
        billing = self.get_billing()
        assert not billing["cancelled"], \
            f"Membership is cancelled — the card reads '{billing['label']}'"
        actual = billing["next_date"]
        assert actual == expected, f"Renewal date is '{actual}', expected '{expected}'"

    def verify_ends_on(self, expected: str):
        billing = self.get_billing()
        assert billing["cancelled"], \
            f"Membership still renews — the card reads '{billing['label']}'"
        actual = billing["next_date"]
        assert actual == expected, f"End date is '{actual}', expected '{expected}'"

    def verify_cancelled(self, ends_on: str = ""):
        notice = self.get_cancellation_notice()
        assert notice, "No cancellation notice on the screen"
        assert self.is_visible(L.button_renew), "No Renew button on a cancelled membership"
        if ends_on:
            self.verify_ends_on(ends_on)
        self.capture_step("swing_pass_cancelled", notice)

    def verify_plan_updated(self, price: str = "", period: str = "", starts_on: str = "",
                            method: str = ""):
        notice = self.get_plan_update_notice()
        assert notice, "No 'You have updated your plan' banner on the screen"
        for label, want in (("price", price), ("period", period), ("start date", starts_on),
                            ("billing method", method)):
            if want and want not in notice:
                raise AssertionError(
                    f"Plan update banner does not name the {label} '{want}': {notice!r}"
                )

    def verify_promos_section(self):
        assert self.is_visible_after_scroll(L.label_promos_section), \
            "'Exclusive promos' section not shown"
        self.capture_step("swing_pass_promos", "Member-only promos section is visible")

    def verify_promo(self, code: str):
        assert self.find_anywhere(L.promo_by_code % code) is not None, \
            f"Promo '{code}' not listed"
        self.capture_step("swing_pass_promo", f"Promo '{code}' is listed")

    def verify_faq_section(self):
        assert self.is_visible_after_scroll(L.label_faq_section), "FAQ section not shown"
        self.capture_step("swing_pass_faq", "FAQs about Swing Pass section is visible")

    # ================= parsing =================
    @staticmethod
    def _lines(desc: str) -> list:
        return [
            line.strip()
            for line in (desc or "").split("\n")
            if line.strip() and line.strip() != "•"
        ]

    @classmethod
    def parse_membership(cls, desc: str) -> dict:
        lines = cls._lines(desc)
        card = {"name": "", "pass_id": "", "status": "", "valid_until": "",
                "label": desc or ""}
        if lines:
            card["name"] = lines[0]
        if len(lines) >= 2:
            card["pass_id"] = lines[1]
        if len(lines) >= 3:
            card["status"] = lines[2]
            if "until" in lines[2]:
                card["valid_until"] = lines[2].split("until", 1)[1].strip()
        return card

    @classmethod
    def parse_savings(cls, desc: str) -> dict:
        lines = cls._lines(desc)
        savings = {"since": "", "amount": "", "label": desc or ""}
        if lines and "," in lines[0]:
            # "Since <date>, you've saved" — the date is between "Since" and the comma
            savings["since"] = lines[0].split(",", 1)[0].replace("Since", "", 1).strip()
        if len(lines) >= 2:
            savings["amount"] = lines[1]
        return savings

    @classmethod
    def parse_comparison(cls, desc: str) -> dict:
        lines = cls._lines(desc)
        comparison = {"without": "", "with": "", "label": desc or ""}
        if lines:
            comparison["without"] = lines[0]
        if len(lines) >= 3:
            comparison["with"] = lines[2]
        return comparison

    @classmethod
    def parse_billing(cls, desc: str) -> dict:
        lines = cls._lines(desc)
        billing = {"price": "", "period": "", "next_date": "", "cancelled": False,
                   "label": desc or ""}
        if lines:
            price, sep, period = lines[0].partition("/")
            billing["price"] = price.strip()
            billing["period"] = period.strip() if sep else ""
        if len(lines) >= 2 and " on " in lines[1]:
            billing["cancelled"] = lines[1].strip().startswith("Ends")
            billing["next_date"] = lines[1].split(" on ", 1)[1].strip()
        return billing

    @staticmethod
    def parse_entry(desc: str) -> dict:
        lines = [line.strip() for line in (desc or "").split("\n") if line.strip()]
        return {
            "title": lines[0] if lines else "",
            "body": " ".join(lines[1:]),
            "label": desc or "",
        }

    # ================= reading values =================
    def _desc(self, locator) -> str:
        return self.scroll_and_find(locator).get_attribute("content-desc") or ""

    def get_membership(self) -> dict:
        card = self.parse_membership(self._desc(L.card_membership))
        self.capture_step("swing_pass_card", f"Pass {card['pass_id']} — {card['status']}",
                          data=card)
        return card

    def get_pass_id(self) -> str:
        return self.get_membership()["pass_id"]

    def get_savings(self) -> dict:
        savings = self.parse_savings(self._desc(L.card_savings))
        self.capture_step("swing_pass_savings",
                          f"Saved {savings['amount']} since {savings['since']}",
                          data=savings)
        return savings

    def get_comparison(self) -> dict:
        comparison = self.parse_comparison(self._desc(L.card_comparison))
        self.capture_step("swing_pass_comparison",
                          f"Without {comparison['without']} vs with {comparison['with']}",
                          data=comparison)
        return comparison

    def get_billing(self) -> dict:
        billing = self.parse_billing(self._desc(L.card_billing))
        self.capture_step("swing_pass_billing",
                          f"{billing['price']} / {billing['period']}, "
                          f"{'ends' if billing['cancelled'] else 'renews'} "
                          f"{billing['next_date']}", data=billing)
        return billing

    def get_plan_update_notice(self) -> str:
        element = self.find_anywhere(L.label_plan_updated)
        notice = element.get_attribute("content-desc") or "" if element is not None else ""
        self.capture_step("swing_pass_plan_updated", notice or "No plan update banner")
        return notice

    def get_cancellation_notice(self) -> str:
        element = self.find_anywhere(L.label_cancellation_notice)
        notice = element.get_attribute("content-desc") or "" if element is not None else ""
        self.capture_step("swing_pass_cancel_notice", notice or "No cancellation notice")
        return notice

    def get_promo_category(self, code: str) -> str:
        return self.scroll_and_find(L.promo_category_by_code % code) \
            .get_attribute("content-desc") or ""

    def get_promo_codes(self) -> list:
        codes = [
            self.parse_entry(e.get_attribute("content-desc") or "")["title"]
            for e in self.find_all(L.promo_any)
        ]
        self.capture_step("swing_pass_promo_codes", f"{len(codes)} promo(s) listed",
                          data={"codes": codes})
        return codes

    def get_benefits(self) -> list:
        return [
            self.parse_entry(e.get_attribute("content-desc") or "")
            for e in self.find_all(L.benefit_any)
        ]

    def get_faqs(self) -> list:
        faqs = [
            self.parse_entry(e.get_attribute("content-desc") or "")
            for e in self.find_all(L.faq_any)
        ]
        self.capture_step("swing_pass_faqs", f"{len(faqs)} FAQ(s) listed",
                          data={"questions": [f["title"] for f in faqs]})
        return faqs

    def get_faq(self, question: str) -> dict:
        element = self.find_anywhere(L.faq_by_question % question)
        assert element is not None, f"FAQ '{question}' not listed"
        faq = self.parse_entry(element.get_attribute("content-desc") or "")
        self.capture_step("swing_pass_faq_entry", faq["title"], data=faq)
        return faq

    def get_benefit(self, title: str) -> dict:
        element = self.find_anywhere(L.benefit_by_title % title)
        assert element is not None, f"Benefit '{title}' not listed"
        benefit = self.parse_entry(element.get_attribute("content-desc") or "")
        self.capture_step("swing_pass_benefit", benefit["title"], data=benefit)
        return benefit

    # ================= action steps =================
    def tap_enlarge_card(self):
        self.click(L.button_enlarge_card)
        self.capture_step("swing_pass_enlarge", "Tapped Enlarge card")

    def open_savings_breakdown(self):
        self.click(L.card_savings)
        self.capture_step("swing_pass_open_savings", "Opened the savings breakdown")

    def open_earnings_breakdown(self):
        self.click(L.button_see_earnings)
        self.capture_step("swing_pass_open_earnings", "Opened the earnings breakdown")

    def open_manage(self):
        self.click(L.button_manage)
        self.capture_step("swing_pass_manage", "Opened Manage membership")

    def tap_renew(self):
        self.click(L.button_renew)
        self.capture_step("swing_pass_renew", "Tapped Renew")

    def open_promo(self, code: str):
        self.click(L.promo_by_code % code)
        self.capture_step("swing_pass_open_promo", f"Opened promo '{code}'")

    def open_all_cashbacks(self):
        self.click(L.button_see_all_cashbacks)
        self.capture_step("swing_pass_cashbacks", "Tapped See all cashbacks")

    def open_faq(self, question: str):
        self.click(L.faq_by_question % question)
        self.capture_step("swing_pass_open_faq", f"Tapped FAQ '{question}'")

    def tap_contact_us(self):
        self.click(L.button_contact_us)
        self.capture_step("swing_pass_contact_us", "Tapped Contact us here.")

    def change_region(self, code: str = "ID"):
        self.click(L.button_region_by_code % code)
        self.capture_step("swing_pass_region", f"Tapped region '{code}'")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("swing_pass_back", "Left the Swing Pass screen")
