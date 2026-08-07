import os

from utils.excel_reader import get_rows_by_tc_id, read_row

# Where the test data lives — file path + worksheet (both overridable by env).
_DATA_PATH = os.getenv(
    "TEST_DATA_MOBILE",
    os.path.join(os.path.dirname(__file__), "test_data_swing_mobile.xlsx"),
)
_SHEET = os.getenv("DRIVING_RANGE_SHEET", "Driving_Range")


def _int_or_empty(value):
    """int(value), but an empty cell stays empty (no crash) — some rows (e.g. a
    cancellation TC) don't fill NUMBER_OF_BAYS / ADDON_QTY."""
    return "" if value in (None, "") else int(value)


class DrivingRangeData:
    """Driving-range test data, sourced from the Driving_Range sheet.

    Attributes (D.REGION, D.DRIVING_RANGE_NAME, ...) are populated from one row.
    Call load(tc_id) to switch to a specific test case by its TC_ID column — the
    TC_ID fixture in conftest does this per test. Without a tc_id the first row
    is used, so D works even when no TC_ID is selected.
    """

    @classmethod
    def load(cls, tc_id: str | None = None):
        if tc_id:
            row = get_rows_by_tc_id(_DATA_PATH, tc_id, id_column="TC_ID", sheet=_SHEET)[0]
        else:
            row = read_row(_DATA_PATH, sheet=_SHEET)
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
        return cls


# default: first row, so D.X works even before a TC_ID is selected
DrivingRangeData.load()
