import os

from utils.excel_reader import get_rows_by_tc_id, read_row

_DATA_PATH = os.getenv(
    "TEST_DATA_MOBILE",
    os.path.join(os.path.dirname(__file__), "test_data_swing_mobile.xlsx"),
)
_SHEET = os.getenv("SWING_CREDIT_SHEET", "Swing_Credit")


def _text(value) -> str:
    return "" if value in (None, "") else str(value).strip()


class SwingCreditData:
    @classmethod
    def load(cls, tc_id: str | None = None):
        if tc_id:
            row = get_rows_by_tc_id(_DATA_PATH, tc_id, id_column="TC_ID", sheet=_SHEET)[0]
        else:
            row = read_row(_DATA_PATH, sheet=_SHEET)
        cls.TC_ID = row.get("TC_ID")
        cls.TC_NAME = row.get("TC_NAME")
        # the credits-history entry is matched on the booking code, and its
        # amount is compared as text ("24,750"), so both stay strings
        cls.BOOKING_CODE = _text(row.get("BOOKING_CODE"))
        cls.TOTAL_CREDIT = _text(row.get("TOTAL_CREDIT"))
        return cls


SwingCreditData.load()
