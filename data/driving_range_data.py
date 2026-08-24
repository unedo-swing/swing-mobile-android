import os

from utils.excel_reader import find_rows, get_rows_by_tc_id, read_row

# Where the test data lives — file path + worksheet (both overridable by env).
_DATA_PATH = os.getenv(
    "TEST_DATA_MOBILE",
    os.path.join(os.path.dirname(__file__), "test_data_swing_mobile.xlsx"),
)
_SHEET = os.getenv("DRIVING_RANGE_SHEET", "Driving_Range")
_ADD_ONS_SHEET = os.getenv("DRIVING_RANGE_ADDONS_SHEET", "Addons_Driving_Range")

def load_add_ons(tc_id: str) -> list[dict]:
    """The add-ons for one test case, or [] when the sheet lists none.

    find_rows (not get_rows_by_tc_id) on purpose: a booking without add-ons is
    a real scenario, so a TC missing from the add-ons sheet must not blow the
    test up. A typo'd TC id still fails loudly — the TC_ID fixture loads the
    Driving_Range sheet first, and that lookup does raise.
    """
    rows = find_rows(_DATA_PATH, "TC_ID", tc_id, sheet=_ADD_ONS_SHEET)
    add_ons = []
    for row in rows:
        name = row.get("ADD_ONS_NAME")
        if name in (None, ""):
            continue
        add_ons.append({
            "add_ons_name": name,
            "add_ons_qty": int(row.get("ADD_ONS_QTY") or 1),
        })
    return add_ons


def _int_or_empty(value):
    return "" if value in (None, "") else int(value)


def _str_or_empty(value) -> str:
    return "" if value in (None, "") else str(value).strip()


class DrivingRangeData:

    @classmethod
    def load(cls, tc_id: str | None = None):
        if tc_id:
            row = get_rows_by_tc_id(_DATA_PATH, tc_id, id_column="TC_ID", sheet=_SHEET)[0]
        else:
            row = read_row(_DATA_PATH, sheet=_SHEET)
        cls.TC_ID = row.get("TC_ID")
        cls.TC_NAME = row.get("TC_NAME")
        cls.MEMBERSHIP = row.get("MEMBERSHIP")
        cls.VENUE_TYPE = row.get("VENUE_TYPE")
        cls.REGION = row.get("REGION")
        cls.DRIVING_RANGE_NAME = row.get("DRIVING_RANGE_NAME")
        cls.BOOKING_DATE = row.get("BOOKING_DATE")
        cls.BAY_NAME = row.get("BAY_NAME")
        cls.TIME_SLOT_START = row.get("TIME_SLOT_START")
        cls.TIME_SLOT_END = row.get("TIME_SLOT_END")
        cls.NUMBER_OF_BAYS = _int_or_empty(row.get("NUMBER_OF_BAYS"))
        cls.ADDON_NAME = row.get("ADDON_NAME")
        cls.ADDON_QTY = _int_or_empty(row.get("ADDON_QTY"))
        cls.PROMO_NAME = row.get("PROMO_NAME")
        cls.PROMO_CODE = row.get("PROMO_CODE")
        cls.PAYMENT_METHOD = row.get("PAYMENT_METHOD")
        # total shown on the Activity booking card (used to pick the card)
        cls.TOTAL_PAYMENT = row.get("TOTAL_PAYMENT")
        # --- reschedule ---
        cls.RESCHEDULE_DAY = row.get("RESCHEDULE_DAY")     # day-of-month cell, e.g. 6
        cls.RESCHEDULE_TIME = row.get("RESCHEDULE_TIME")   # e.g. "22:00"
        cls.RESCHEDULE_REASON = row.get("RESCHEDULE_REASON")
        # --- cancellation ---
        cls.CANCEL_REASON = row.get("CANCEL_REASON")
        cls.BANK_NAME = row.get("BANK_NAME")
        _acct = row.get("BANK_ACCOUNT_NUMBER")
        cls.BANK_ACCOUNT_NUMBER = "" if _acct in (None, "") else str(_acct)
        cls.BANK_ACCOUNT_NAME = row.get("BANK_ACCOUNT_NAME")
        cls.CODE_BOOKING = row.get("CODE_BOOKING")
        # --- account that books (only the cross-country rows fill these; the
        # rest of the sheet books with whoever the suite is already logged in as)
        cls.USER_COUNTRY = row.get("USER_COUNTRY")
        cls.PHONE_NUMBER = _str_or_empty(row.get("PHONE_NUMBER"))
        cls.VERIFICATION_METHOD = (
            str(row.get("VERIFICATION_METHOD") or "whatsapp").strip().lower()
        )
        cls.OTP = _str_or_empty(row.get("OTP"))
        # --- documentation only (never read by a step) ---
        cls.PRECONDITION = row.get("PRECONDITION")
        cls.EXPECTED_RESULT = row.get("EXPECTED_RESULT")
        return cls


DrivingRangeData.load()
