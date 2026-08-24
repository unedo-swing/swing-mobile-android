from core.android_base_page import AndroidBasePage
from locators.swing_pass.swing_pass_locators import SwingPassLocators as L


class SwingPassPage(AndroidBasePage):

    STATUS_WORDS = ("Active", "Inactive", "Expired", "Cancelled", "Waiting")

    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "Swing Pass screen not shown"
        self.capture_step("swing_pass")

    def verify_join_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "Swing Pass screen not shown"
        assert self.is_visible(L.button_join, timeout=20), \
            "No 'Join Swing Pass' button — the account may already hold a Pass"
        self.capture_step("swing_pass_join_screen")

    def verify_active_membership(self):
        card = self.get_membership()
        assert card["valid_until"], \
            f"Membership card does not show an active period: {card['label']!r}"
        self.capture_step("swing_pass_active",
                          f"Active until {card['valid_until']}", data=card)

    def verify_inactive_membership(self):
        card = self.get_membership()
        assert card["status"].lower() == "inactive", \
            f"Membership card is not inactive: {card['label']!r}"
        self.capture_step("swing_pass_inactive", card["label"], data=card)

    def verify_waiting_verification(self):
        card = self.get_membership()
        assert card["status"] == "Waiting for verification", \
            f"Membership card is not waiting for verification: {card['label']!r}"
        self.capture_step("swing_pass_waiting", card["label"], data=card)

    def verify_verification_submitted(self, note: str = ""):
        assert self.is_visible(L.label_verification_submitted, timeout=20), \
            "'Verification submitted!' not shown"
        actual = self.get_verification_note()
        assert actual, "No verification notice on the screen"
        if note:
            assert note in actual, f"Verification notice is '{actual}', expected '{note}'"
        assert self.is_visible(L.button_ok_got_it), "No 'Ok, got it!' button on the screen"
        self.capture_step("swing_pass_verification_submitted", actual)

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

    def verify_tagline(self, expected: str = ""):
        tagline = self.get_tagline()
        assert tagline, "No Swing Pass tagline on the screen"
        if expected:
            assert expected in tagline, f"Tagline is '{tagline}', expected '{expected}'"
        self.capture_step("swing_pass_tagline", tagline)

    def verify_subscribe_info(self, expected: str = ""):
        info = self.get_subscribe_info()
        assert info, "No Swing Pass subscription description on the screen"
        if expected:
            assert expected in info, f"Description is '{info}', expected '{expected}'"
        self.capture_step("swing_pass_subscribe_info", info)

    def verify_promos_section(self):
        assert self.is_visible_after_scroll(L.label_promos_section), \
            "'Exclusive promos' section not shown"
        self.capture_step("swing_pass_promos")

    def verify_promo(self, code: str):
        assert self.find_anywhere(L.promo_by_code % code) is not None, \
            f"Promo '{code}' not listed"
        self.capture_step("swing_pass_promo", f"Promo '{code}' is listed")

    def verify_faq_section(self):
        assert self.is_visible_after_scroll(L.label_faq_section), "FAQ section not shown"
        self.capture_step("swing_pass_faq")

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
        rest = lines[1:]
        if rest and rest[-1].startswith(cls.STATUS_WORDS):
            card["status"] = rest[-1]
            rest = rest[:-1]
            if "until" in card["status"]:
                card["valid_until"] = card["status"].split("until", 1)[1].strip()
        if rest:
            card["pass_id"] = rest[0]
        return card

    @classmethod
    def parse_savings(cls, desc: str) -> dict:
        lines = cls._lines(desc)
        savings = {"since": "", "amount": "", "label": desc or ""}
        if lines and "," in lines[0]:
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

    def _desc(self, locator) -> str:
        return self.scroll_and_find(locator).get_attribute("content-desc") or ""

    def _optional_desc(self, locator) -> str:
        element = self.find_anywhere(locator)
        return element.get_attribute("content-desc") or "" if element is not None else ""

    def is_member(self) -> bool:
        return self.find_anywhere(L.button_join) is None

    def get_membership(self) -> dict:
        card = self.parse_membership(self._desc(L.card_membership_any))
        self.capture_step("swing_pass_card",
                          f"Pass {card['pass_id']} — {card['status']}", data=card)
        return card

    def get_pass_id(self) -> str:
        return self.get_membership()["pass_id"]

    def get_status(self) -> str:
        return self.get_membership()["status"]

    def get_tagline(self) -> str:
        return self._optional_desc(L.label_tagline)

    def get_subscribe_info(self) -> str:
        return self._optional_desc(L.label_subscribe_info)

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
        notice = self._optional_desc(L.label_plan_updated)
        self.capture_step("swing_pass_plan_updated", notice or "No plan update banner")
        return notice

    def get_verification_note(self) -> str:
        return self._optional_desc(L.label_verification_note)

    def get_cancellation_notice(self) -> str:
        notice = self._optional_desc(L.label_cancellation_notice)
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

    def tap_enlarge_card(self):
        self.click(L.button_enlarge_card)
        self.capture_step("swing_pass_enlarge")

    def tap_membership_card(self):
        self.click(L.card_membership_any)
        self.capture_step("swing_pass_open_card")

    def tap_join(self):
        self.click(L.button_join)
        self.capture_step("swing_pass_tap_join")

    def open_savings_breakdown(self):
        self.click(L.card_savings)
        self.capture_step("swing_pass_open_savings")

    def open_earnings_breakdown(self):
        self.click(L.button_see_earnings)
        self.capture_step("swing_pass_open_earnings")

    def open_manage(self):
        self.click(L.button_manage)
        self.capture_step("swing_pass_manage")

    def tap_renew(self):
        self.click(L.button_renew)
        self.capture_step("swing_pass_renew")

    def open_promo(self, code: str):
        self.click(L.promo_by_code % code)
        self.capture_step("swing_pass_open_promo", f"Opened promo '{code}'")

    def open_all_cashbacks(self):
        self.click(L.button_see_all_cashbacks)
        self.capture_step("swing_pass_cashbacks")

    def open_faq(self, question: str):
        self.click(L.faq_by_question % question)
        self.capture_step("swing_pass_open_faq", f"Tapped FAQ '{question}'")

    def tap_ok_got_it(self):
        self.click(L.button_ok_got_it)
        self.wait_until_loaded()
        self.capture_step("swing_pass_ok_got_it")

    def tap_contact_support(self):
        self.click(L.button_contact_support)
        self.capture_step("swing_pass_contact_support")

    def tap_contact_us(self):
        self.click(L.button_contact_us)
        self.capture_step("swing_pass_contact_us")

    def change_region(self, code: str = "ID"):
        self.click(L.button_region_by_code % code)
        self.capture_step("swing_pass_region", f"Tapped region '{code}'")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("swing_pass_back")
