"""
Android-specific base page.

Put here anything that only makes sense on Android: UiAutomator scroll gestures,
keyboard/permission handling, hardware back, etc. Android page objects (or the
Android variant of a shared page) inherit from this.
"""
import time

from appium.webdriver.common.appiumby import AppiumBy

from config import settings
from core.base_page import BasePage


class AndroidBasePage(BasePage):

    # ------------------------------------------------------------------ #
    # Scroll-into-view, then click
    # ------------------------------------------------------------------ #
    # Swipe speed in pixels/second — lower is slower (Appium default is ~5000).
    SCROLL_SPEED = 700
    # Pause after each swipe so the momentum scroll finishes before we check /
    # click. Raise it if a click still lands mid-scroll.
    SCROLL_SETTLE = 0.8

    def _swipe_up(self):
        size = self.driver.get_window_size()
        w, h = size["width"], size["height"]
        self.driver.execute_script(
            "mobile: swipeGesture",
            {
                "left": int(w * 0.1), "top": int(h * 0.2),
                "width": int(w * 0.8), "height": int(h * 0.6),
                "direction": "up", "percent": 0.8,
                "speed": self.SCROLL_SPEED,
            },
        )
        time.sleep(self.SCROLL_SETTLE)

    def _swipe_down(self):
        size = self.driver.get_window_size()
        w, h = size["width"], size["height"]
        self.driver.execute_script(
            "mobile: swipeGesture",
            {
                "left": int(w * 0.1), "top": int(h * 0.2),
                "width": int(w * 0.8), "height": int(h * 0.6),
                "direction": "down", "percent": 0.8,
                "speed": self.SCROLL_SPEED,
            },
        )
        time.sleep(self.SCROLL_SETTLE)

    def scroll_to_top(self, max_swipes: int = 3):
        for _ in range(max_swipes):
            before = self.driver.page_source
            self._swipe_down()
            if self.driver.page_source == before:
                break

    def scroll_to_element(self, locator, max_swipes: int = 10):
        by, value = self._resolve(locator)
        self.driver.implicitly_wait(0)
        try:
            for _ in range(max_swipes):
                els = self.driver.find_elements(by, value)
                if els:
                    return els[0]
                self._swipe_up()
            return None
        finally:
            self.driver.implicitly_wait(settings.IMPLICIT_WAIT)

    def click(self, locator):
        self.scroll_to_element(locator)
        super().click(locator)

    def find_anywhere(self, locator, max_swipes: int = 10):
        """Locate an element anywhere on a scrollable screen, whatever the
        current scroll position. Returns None when it really isn't there.

        ``scroll_to_element`` only swipes up, so it can't reach a row we have
        already scrolled past — which happens whenever a caller reads several
        fields down a long screen. Searching downward from here first keeps the
        common case at zero extra swipes; only a miss pays for the trip back to
        the top and a second pass.
        """
        element = self.scroll_to_element(locator, max_swipes)
        if element is None:
            self.scroll_to_top()
            element = self.scroll_to_element(locator, max_swipes)
        return element

    def is_visible_after_scroll(self, locator, timeout: int = 5) -> bool:
        """``is_visible`` that swipes first.

        The base check only sees the current viewport, so a row that is simply
        below the fold reads as missing — unlike ``click``, which scrolls. Use
        this for verify steps; keep plain ``is_visible`` for negative checks,
        where the swipe search would burn ~10 swipes before returning False.
        """
        if self.find_anywhere(locator) is None:
            return False
        return self.is_visible(locator, timeout)

    def scroll_and_find(self, locator):
        """Swipe the element into view, then return it.

        Flutter builds lazily, so a widget off-screen is usually absent from
        the accessibility tree entirely and a plain ``find`` would time out.
        Falls back to ``find`` so the caller still gets the normal error.
        """
        element = self.find_anywhere(locator)
        return element if element is not None else self.find(locator)

    # ------------------------------------------------------------------ #
    # Loading state
    # ------------------------------------------------------------------ #
    # Flutter draws spinners as a ProgressBar; full-screen waits (payment, in
    # particular) come through as a View whose content-desc carries the wording.
    LOADING = (
        '//android.widget.ProgressBar'
        ' | //*[contains(@content-desc,"Loading")]'
        ' | //*[contains(@content-desc,"loading")]'
        ' | //*[contains(@content-desc,"Processing")]'
        ' | //*[contains(@content-desc,"Please wait")]'
    )

    def is_loading(self) -> bool:
        """True while a spinner / 'Loading' overlay is on screen."""
        self.driver.implicitly_wait(0)
        try:
            return bool(self.driver.find_elements(*self._resolve(self.LOADING)))
        finally:
            self.driver.implicitly_wait(settings.IMPLICIT_WAIT)

    def wait_until_loaded(self, timeout: int = 10, stable_for: float = 0.5) -> bool:
        deadline = time.time() + timeout
        clear_since = None
        while time.time() < deadline:
            if self.is_loading():
                clear_since = None
            else:
                clear_since = clear_since or time.time()
                if time.time() - clear_since >= stable_for:
                    return True
            time.sleep(0.25)
        self._log(f"still loading after {timeout}s")
        return False

    def hide_keyboard(self):
        try:
            if self.driver.is_keyboard_shown():
                self.driver.hide_keyboard()
        except Exception:
            pass

    def press_back(self):
        """Android hardware back button."""
        self.driver.back()

    def press_search(self):
        """Press the on-screen keyboard's Search (IME action) key to submit."""
        try:
            self.driver.execute_script("mobile: performEditorAction", {"action": "search"})
        except Exception:
            self.driver.press_keycode(66)  # KEYCODE_ENTER as a fallback

    def scroll_to_text(self, text: str):
        """Scroll a scrollable container until an element with ``text`` shows."""
        selector = (
            'new UiScrollable(new UiSelector().scrollable(true))'
            f'.scrollIntoView(new UiSelector().textContains("{text}"))'
        )
        self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector)

    def accept_permission(self):
        """Tap a system permission 'Allow' dialog if one is present."""
        for rid in (
            "com.android.permissioncontroller:id/permission_allow_button",
            "com.android.packageinstaller:id/permission_allow_button",
        ):
            found = self.driver.find_elements(AppiumBy.ID, rid)
            if found:
                found[0].click()
                return
