"""
Shared "Featured promos" page object (Android).

Opened from the promo strip's "See all" tile on tee time, event and
driving-range details — the screen is identical in all three, so every flow
uses this one page. Per-screen STEPS only, each recording evidence with
capture_step. XPaths come from locators/featured_promos_locators.py.
"""
from core.android_base_page import AndroidBasePage
from locators.featured_promos_locators import FeaturedPromosLocators as L


class FeaturedPromosPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_screen(self):
        self.wait_until_loaded()
        assert self.is_visible(L.label_title, timeout=20), "Featured promos screen not shown"
        self.capture_step("featured_promos", "Featured promos screen is visible")

    def verify_auto_claim_banner(self):
        assert self.is_visible(L.banner_auto_claim, timeout=10), "Auto-claim banner not shown"
        self.capture_step("featured_promos_banner", "Auto-claim banner is visible")

    def verify_promo(self, name: str):
        assert self.find_anywhere(L.promo_by_name % name) is not None, f"Promo '{name}' not listed"
        self.capture_step("featured_promo_shown", f"Promo listed: {name}")

    def verify_promo_count(self, expected: int):
        promos = self.get_promos()
        assert len(promos) == expected, \
            f"{len(promos)} promo(s) listed, expected {expected}"

    def verify_swing_pass_exclusive(self, name: str):
        assert self.find_anywhere(L.badge_swing_pass_by_promo % name) is not None, \
            f"Promo '{name}' is not marked Swing Pass Exclusive"
        self.capture_step("featured_promo_exclusive", f"'{name}' is Swing Pass Exclusive")

    # ================= parsing =================
    @staticmethod
    def parse_promo(desc: str) -> dict:
        lines = [line.strip() for line in (desc or "").split("\n") if line.strip()]
        # drop the immediate repeat of the title, if any
        if len(lines) > 1 and lines[0] == lines[1]:
            lines = lines[:1] + lines[2:]

        exclusive = "Swing Pass Exclusive" in lines
        promo = {
            "name": lines[0] if lines else "",
            "subtitle": "",
            "validity": "",
            "swing_pass_exclusive": exclusive,
            "label": desc or "",
        }
        if "Validity" in lines:
            index = lines.index("Validity")
            promo["subtitle"] = " / ".join(lines[1:index])
            after = lines[index + 1:index + 2]
            if after and after[0] != "Swing Pass Exclusive":
                promo["validity"] = after[0]
        return promo

    # ================= reading =================
    def get_promos(self, max_swipes: int = 15) -> list:
        """Every promo on the screen, scrolling the whole list.

        Flutter builds lazily, so a single find_all only ever sees the cards
        currently on screen — the list is walked top to bottom and cards are
        de-duplicated by name. A card met again while scrolled further into
        view can carry a fuller content-desc, so the longer one wins.
        """
        self.scroll_to_top()
        promos: dict = {}
        for _ in range(max_swipes):
            for element in self.find_all(L.promo_any):
                desc = element.get_attribute("content-desc") or ""
                promo = self.parse_promo(desc)
                name = promo["name"]
                if not name:
                    continue
                if name not in promos or len(desc) > len(promos[name]["label"]):
                    promos[name] = promo
            before = self.driver.page_source
            self._swipe_up()
            if self.driver.page_source == before:
                break
        return list(promos.values())

    def get_promo_names(self, max_swipes: int = 15) -> list:
        """Every promo name, listed in the PDF evidence as a numbered table."""
        names = [promo["name"] for promo in self.get_promos(max_swipes)]
        data = {"Total promos": len(names)}
        data.update({f"Promo {i}": name for i, name in enumerate(names, 1)})
        self.capture_step("featured_promo_names", f"{len(names)} featured promo(s) listed",
                          data=data)
        return names

    def capture_promos(self, max_swipes: int = 15) -> list:
        """Same walk as get_promo_names, but records each promo's details."""
        promos = self.get_promos(max_swipes)
        data = {"Total promos": len(promos)}
        for i, promo in enumerate(promos, 1):
            details = [promo["subtitle"], promo["validity"]]
            if promo["swing_pass_exclusive"]:
                details.append("Swing Pass Exclusive")
            data[f"{i}. {promo['name']}"] = " • ".join(d for d in details if d) or "—"
        self.capture_step("featured_promos_detail", f"{len(promos)} featured promo(s) listed",
                          data=data)
        return promos

    def get_promo(self, name: str) -> dict:
        element = self.find_anywhere(L.promo_by_name % name)
        assert element is not None, f"Promo '{name}' not listed"
        promo = self.parse_promo(element.get_attribute("content-desc") or "")
        self.capture_step("featured_promo", f"Promo '{name}'", data=promo)
        return promo

    def get_quota(self, name: str) -> str:
        """A promo's redemption quota badge, e.g. 'x1 / day'."""
        element = self.find_anywhere(L.quota_by_promo % name)
        return element.get_attribute("content-desc") or "" if element is not None else ""

    # ================= action steps =================
    def open_promo(self, name: str):
        self.click(L.promo_by_name % name)
        self.capture_step("featured_promo_open", f"Opened promo '{name}'")

    def tap_back(self):
        self.click(L.button_back)
        self.capture_step("featured_promos_back", "Left the Featured promos screen")
