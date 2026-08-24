from core.android_base_page import AndroidBasePage
from locators.login_locators import LoginLocators as L
import re
import time


class LoginPage(AndroidBasePage):

    # ================= verify steps =================
    def verify_login_screen(self):
        assert self.is_visible(L.label_header, timeout=30), "Login (phone entry) screen not shown"
        self.capture_step("login_screen")

    def verify_continue_enabled(self, expected: bool = True):
        actual = self.is_enabled(L.button_continue)
        self.capture_step(
            "continue_state", f"Continue enabled = {actual} (expected {expected})"
        )
        assert actual == expected, f"Continue enabled={actual}, expected {expected}"

    def verify_verification_method_screen(self):
        assert self.is_visible(L.label_verification_title), "Verification method screen not shown"
        self.capture_step("verification_method")

    def await_otp_screen(self, timeout: int = 180, poll: int = 3) -> bool:
        import time

        deadline = time.time() + timeout
        challenge_announced = False
        while time.time() < deadline:
            if self.is_visible(L.label_otp_title, timeout=1, log=False):
                self.capture_step("otp_screen")
                return True
            if not challenge_announced and self.is_visible(L.label_secure_challenge, timeout=1, log=False):
                challenge_announced = True
                self.capture_step("secure_challenge")
                print(
                    "\n" + "=" * 64 +
                    "\n[secure challenge] 'Verify you are human' muncul."
                    "\n[secure challenge] Selesaikan CAPTCHA-nya MANUAL di device."
                    "\n[secure challenge] Otomatisasi menunggu, tidak menyentuh CAPTCHA."
                    "\n" + "=" * 64
                )
            time.sleep(poll)
        self.capture_step("otp_screen_timeout")
        return False

    def verify_otp_screen(self):
        assert self.await_otp_screen(), "OTP screen not shown (check for an unsolved human-check)"

    # ================= action steps =================
    def enter_phone(self, phone_number: str):
        self.fill(L.input_phone_number, phone_number)
        self.capture_step("phone_entered", f"Entered phone number {phone_number}")

    def tap_continue(self):
        self.hide_keyboard()
        self.click(L.button_continue)
        self.capture_step("continue_tapped")

    def open_country_picker(self):
        self.wait_for(3)
        self.click(L.button_country_code)
        self.capture_step("country_picker_opened")

    def read_dial_code(self) -> str:
        for locator in (L.label_country_code, L.button_country_code):
            try:
                raw = self.get_text(locator)
            except Exception:
                continue
            match = re.search(r"\+\s*(\d+)", raw or "")
            if match:
                code = f"+{match.group(1)}"
                self.capture_step("dial_code", f"Country code on the login screen: {code}")
                return code
        self.capture_step("dial_code_unread")
        return ""

    def choose_sms(self):
        self.click(L.button_verification_sms)
        self.capture_step("chose_sms")

    def choose_whatsapp(self):
        self.click(L.button_verification_whatsapp)
        self.capture_step("chose_whatsapp")

    def enter_code(self, code: str):
        time.sleep(3)
        field = self.wait_visible(L.input_verification_code)
        field.click()
        for ch in code.strip():
            if ch.isdigit():
                self.driver.press_keycode(7 + int(ch))
                time.sleep(1)
        self.capture_step("code_entered", f"Entered verification code ({len(code.strip())} digits)")

    def wait_for_manual_otp(self, timeout: int = 300, poll: int = 3) -> bool:
        print(
            "\n" + "=" * 64 +
            "\n[manual OTP] Masukkan kode OTP LANGSUNG di device sekarang."
            f"\n[manual OTP] Menunggu hingga {timeout}s sampai layar OTP hilang..."
            "\n" + "=" * 64
        )
        self.capture_step("waiting_manual_otp")
        deadline = time.time() + timeout
        while time.time() < deadline:
            if not self.is_visible(L.label_otp_title, timeout=1, log=False):
                self.capture_step("otp_accepted")
                print("[manual OTP] Layar OTP hilang — login lanjut.")
                return True
            time.sleep(poll)
        self.capture_step("otp_timeout")
        return False
