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
    SCROLL_SPEED = 500
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

    # ------------------------------------------------------------------ #
    # Horizontal carousels
    # ------------------------------------------------------------------ #
    def _swipe_in_element(self, locator, direction: str, percent: float = 0.8):
        """Swipe *inside* one element instead of across the whole screen.

        Carousels (promos, images, date strip) scroll horizontally within their
        own bounds; a full-width gesture would drag the page behind them, so the
        gesture is bound to the element via ``elementId``.
        """
        element = self.scroll_and_find(locator)
        self.driver.execute_script(
            "mobile: swipeGesture",
            {
                "elementId": element.id,
                "direction": direction, "percent": percent,
                "speed": self.SCROLL_SPEED,
            },
        )
        time.sleep(self.SCROLL_SETTLE)

    def swipe_left_in(self, locator, percent: float = 0.8):
        """Advance a carousel one page (finger moves left, later items arrive)."""
        self._swipe_in_element(locator, "left", percent)

    def swipe_right_in(self, locator, percent: float = 0.8):
        """Go back one page in a carousel."""
        self._swipe_in_element(locator, "right", percent)

    def swipe_left_to_element(self, locator, container, max_swipes: int = 5) -> bool:
        """Swipe ``container`` left until ``locator`` shows up. True when found.

        Stops early once the container stops changing, so a carousel already at
        its end doesn't burn every swipe.
        """
        if self.is_visible(locator, timeout=1, log=False):
            return True
        for _ in range(max_swipes):
            before = self.driver.page_source
            self.swipe_left_in(container)
            if self.is_visible(locator, timeout=1, log=False):
                return True
            if self.driver.page_source == before:
                break
        return False

    def scroll_to_top(self, max_swipes: int = 3):
        for _ in range(max_swipes):
            before = self.driver.page_source
            self._swipe_down()
            if self.driver.page_source == before:
                break
        
    def scroll_up_to_element(self, locator, max_swipes: int = 10):
        by, value = self._resolve(locator)
        self.driver.implicitly_wait(0)
        try:
            for _ in range(max_swipes):
                els = self.driver.find_elements(by, value)
                if els:
                    return els[0]
                self._swipe_down()
            return None
        finally:
            self.driver.implicitly_wait(settings.IMPLICIT_WAIT)
    
    def scroll_down_to_element(self, locator, max_swipes: int = 10):
        by, value = self._resolve(locator)
        self.driver.implicitly_wait(0)
        try:
            for _ in range(max_swipes):
                els = self.driver.find_elements(by, value)
                if els:
                    return els[0]
                self._swipe_up()
                self.wait_for(1)
            return None
        finally:
            self.driver.implicitly_wait(settings.IMPLICIT_WAIT)

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

    # Every click waits for the screen to settle first — Flutter publishes a
    # node before the widget can take a tap, so an eager tap lands on nothing.
    # Set CLICK_STABLE = False (or call click_now) where that wait is wasted.
    CLICK_STABLE = True
    CLICK_SETTLE_TIMEOUT = 10
    CLICK_STABLE_TIMEOUT = 5

    def click(self, locator, retries: int = 3, stable: bool | None = None):
        if self.CLICK_STABLE if stable is None else stable:
            self.wait_settled(self.CLICK_SETTLE_TIMEOUT)
            self.scroll_to_element(locator)
            self.wait_stable(locator, self.CLICK_STABLE_TIMEOUT)
        else:
            self.scroll_to_element(locator)
        super().click(locator, retries)

    def click_now(self, locator, retries: int = 3):
        """Click without the settle/stable wait — for a screen already still."""
        self.click(locator, retries, stable=False)

    def click_when_stable(self, locator, timeout: int = 5, retries: int = 3):
        """Kept for callers that ask for it explicitly; click() does this now."""
        self.click(locator, retries, stable=True)

    def wait_settled(self, timeout: int = 10):
        """Wait out the spinner, then let the frame finish rendering."""
        self.wait_until_loaded(timeout=timeout, stable_for=0.25)
        time.sleep(0.15)

    def wait_stable(self, locator, timeout: int = 5, stable_for: float = 0.25):
        deadline = time.time() + timeout
        previous, still_since = None, None
        self.driver.implicitly_wait(0)
        try:
            while time.time() < deadline:
                try:
                    element = self.driver.find_element(*self._resolve(locator))
                    rect = element.rect
                except Exception:
                    previous, still_since = None, None
                    time.sleep(0.15)
                    continue
                if rect == previous:
                    still_since = still_since or time.time()
                    if time.time() - still_since >= stable_for:
                        return element
                else:
                    previous, still_since = rect, None
                time.sleep(0.15)
        finally:
            self.driver.implicitly_wait(settings.IMPLICIT_WAIT)
        self._log(f"element still moving after {timeout}s")
        return None

    def find_anywhere(self, locator, max_swipes: int = 10):
        element = self.scroll_to_element(locator, max_swipes)
        if element is None:
            self.scroll_to_top()
            element = self.scroll_to_element(locator, max_swipes)
        return element

    def is_visible_after_scroll(self, locator, timeout: int = 5) -> bool:
        if self.find_anywhere(locator) is None:
            return False
        return self.is_visible(locator, timeout)

    def scroll_and_find(self, locator):
        if self.is_visible(locator):
            return self.find(locator)
        element = self.find_anywhere(locator)
        if element is not None:
            return element
        return self.find(locator)

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

    def wait_until_loaded(self, timeout: int = 5, stable_for: float = 0.5) -> bool:
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

    def wait_for_keyboard(self, timeout: int = 5) -> bool:
        """Block until the soft keyboard is up. True when it showed in time.

        The keyboard can come up before or after the field is filled, and the
        Search (IME action) key is swallowed while it is still animating in —
        so callers wait for it before pressing Search.
        """
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                if self.driver.is_keyboard_shown():
                    return True
            except Exception:
                pass
            time.sleep(0.25)
        self._log(f"keyboard not shown after {timeout}s")
        return False

    def press_search(self):
        """Press the on-screen keyboard's Search (IME action) key to submit."""
        try:
            self.driver.execute_script("mobile: performEditorAction", {"action": "search"})
        except Exception:
            self.driver.press_keycode(66)  # KEYCODE_ENTER as a fallback

    def slide_to_end(self, track_locator, thumb_locator=None):
        """Drag a slide-to-confirm control's thumb from left to right.

        These controls ignore a tap — only a drag commits — so ``click`` on
        them silently does nothing. The drag ends half a thumb-width inside the
        right edge: releasing exactly on the boundary sometimes lands outside
        the track and the thumb springs back.

        ``thumb_locator`` defaults to the track's own ImageView child, which is
        how the Swing Pass sliders are built.
        """
        track = self.scroll_and_find(track_locator)
        thumb = self.find(thumb_locator or f"{track_locator}/android.widget.ImageView")
        track_box, thumb_box = track.rect, thumb.rect
        start_x = thumb_box["x"] + thumb_box["width"] // 2
        end_x = track_box["x"] + track_box["width"] - thumb_box["width"] // 2
        y = thumb_box["y"] + thumb_box["height"] // 2
        self.driver.execute_script(
            "mobile: dragGesture",
            {"startX": start_x, "startY": y, "endX": end_x, "endY": y,
             "speed": self.SCROLL_SPEED},
        )
        time.sleep(self.SCROLL_SETTLE)

    def scroll_to_text(self, text: str):
        """Scroll a scrollable container until an element with ``text`` shows."""
        selector = (
            'new UiScrollable(new UiSelector().scrollable(true))'
            f'.scrollIntoView(new UiSelector().textContains("{text}"))'
        )
        self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector)

    PERMISSION_ALLOW_IDS = (
        "com.android.permissioncontroller:id/permission_allow_button",
        "com.android.packageinstaller:id/permission_allow_button",
        # location asks for a scope instead of a plain "Allow"
        "com.android.permissioncontroller:id/permission_allow_foreground_only_button",
        "com.android.permissioncontroller:id/permission_allow_one_time_button",
    )

    def accept_permission(self, timeout: int = 5) -> bool:
        """Tap a system permission 'Allow' dialog if one shows up within ``timeout``."""
        deadline = time.time() + timeout
        while True:
            for rid in self.PERMISSION_ALLOW_IDS:
                found = self.driver.find_elements(AppiumBy.ID, rid)
                if found:
                    found[0].click()
                    self.wait_settled()
                    return True
            if time.time() >= deadline:
                return False
            time.sleep(0.5)

    def _desc(self, locator) -> str:
        return self.scroll_and_find(locator).get_attribute("content-desc") or ""