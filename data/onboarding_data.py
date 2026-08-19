import os
from datetime import date, datetime

from utils.excel_reader import get_rows_by_tc_id, read_row

# Where the test data lives — file path + worksheet (both overridable by env).
# One row per onboarding test case on the Onboarding sheet.
_DATA_PATH = os.getenv(
    "TEST_DATA_MOBILE",
    os.path.join(os.path.dirname(__file__), "test_data_swing_mobile.xlsx"),
)
_SHEET = os.getenv("ONBOARDING_SHEET", "Onboarding")


def _str_or_empty(value):
    """str(value), but an empty cell stays empty — a phone or OTP read from
    Excel can come back as a number, and a blank must not become "None"."""
    return "" if value in (None, "") else str(value)


def _date_text(value):
    """Birthday as the app spells it, e.g. "02 September 1998" — the cell is
    text, but Excel turns it into a real date the moment someone retypes it."""
    if isinstance(value, (datetime, date)):
        return f"{value.day:02d} {value.strftime('%B %Y')}"
    return _str_or_empty(value)


class OnboardingData:

    @classmethod
    def load(cls, tc_id: str | None = None):
        if tc_id:
            row = get_rows_by_tc_id(_DATA_PATH, tc_id, id_column="TC_ID", sheet=_SHEET)[0]
        else:
            row = read_row(_DATA_PATH, sheet=_SHEET)
        cls.TC_ID = row.get("TC_ID")
        cls.TC_NAME = row.get("TC_NAME")
        # --- login leg (a brand-new number, so it lands on profile setup) ---
        cls.COUNTRY = row.get("COUNTRY")
        cls.PHONE_NUMBER = _str_or_empty(row.get("PHONE_NUMBER"))
        cls.VERIFICATION_METHOD = (
            str(row.get("VERIFICATION_METHOD") or "whatsapp").strip().lower()
        )
        # normally blank: an unregistered number needs the real code typed in
        cls.OTP = _str_or_empty(row.get("OTP"))
        # --- profile setup ---
        cls.FIRST_NAME = row.get("FIRST_NAME")
        cls.LAST_NAME = row.get("LAST_NAME")
        cls.BIRTH_DATE = _date_text(row.get("BIRTH_DATE"))
        cls.NATIONALITY = row.get("NATIONALITY")
        cls.GENDER = row.get("GENDER")
        cls.USERNAME = row.get("USERNAME")
        cls.EMAIL = row.get("EMAIL")
        # blank -> the referral field is skipped entirely
        cls.REFERRAL_CODE = row.get("REFERRAL_CODE") or ""
        # --- "how did you find out about Swing?" ---
        cls.SOURCE = row.get("SOURCE")
        cls.EXPECTED_RESULT = row.get("EXPECTED_RESULT")
        return cls


# default: first row, so D.X works even before a TC_ID is selected
OnboardingData.load()
