import os

from utils.excel_reader import get_rows_by_tc_id, read_row

# Where the test data lives — file path + worksheet (both overridable by env).
# One row per login test case on the Login sheet.
_DATA_PATH = os.getenv(
    "TEST_DATA_MOBILE",
    os.path.join(os.path.dirname(__file__), "test_data_swing_mobile.xlsx"),
)
_SHEET = os.getenv("LOGIN_SHEET", "Login")


def _str_or_empty(value):
    """str(value), but an empty cell stays empty — a phone or OTP read from
    Excel can come back as a number, and a blank must not become "None"."""
    return "" if value in (None, "") else str(value)


class LoginData:

    @classmethod
    def load(cls, tc_id: str | None = None):
        if tc_id:
            row = get_rows_by_tc_id(_DATA_PATH, tc_id, id_column="TC_ID", sheet=_SHEET)[0]
        else:
            row = read_row(_DATA_PATH, sheet=_SHEET)
        cls.TC_ID = row.get("TC_ID")
        cls.TC_NAME = row.get("TC_NAME")
        cls.COUNTRY = row.get("COUNTRY")
        cls.PHONE_NUMBER = _str_or_empty(row.get("PHONE_NUMBER"))
        # OTP channel: "whatsapp" (default) or "sms"
        cls.VERIFICATION_METHOD = (
            str(row.get("VERIFICATION_METHOD") or "whatsapp").strip().lower()
        )
        # blank cell -> the test asks for the real code at the terminal
        cls.OTP = _str_or_empty(row.get("OTP"))
        cls.EXPECTED_RESULT = row.get("EXPECTED_RESULT")
        return cls


# default: first row, so D.X works even before a TC_ID is selected
LoginData.load()
