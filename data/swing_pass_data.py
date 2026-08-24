import os

from utils.excel_reader import get_rows_by_tc_id, read_row, read_rows

_DATA_PATH = os.getenv(
    "TEST_DATA_MOBILE",
    os.path.join(os.path.dirname(__file__), "test_data_swing_mobile.xlsx"),
)
_SHEET = os.getenv("SWING_PASS_SHEET", "Swing_Pass")

_TRUE = ("true", "yes", "y", "1", "run")
_FALSE = ("false", "no", "n", "0", "skip")


def _int_or_default(value, default: int = 1) -> int:
    return default if value in (None, "") else int(value)


def _str_or_empty(value) -> str:
    return "" if value in (None, "") else str(value)


def _bool_or_default(value, default: bool = True) -> bool:
    """TRUE/FALSE cells come back as bools from Excel but as text from CSV edits."""
    if value in (None, ""):
        return default
    if isinstance(value, bool):
        return value
    text = str(value).strip().casefold()
    if text in _TRUE:
        return True
    if text in _FALSE:
        return False
    raise ValueError(f"Cannot read '{value}' as TRUE/FALSE")


def _list(value) -> list[str]:
    return [part.strip() for part in _str_or_empty(value).split(",") if part.strip()]


def tc_ids(action: str = "run", module: str | None = None) -> list[str]:
    """Every TC id in the sheet for a given ACTION, e.g. to parametrize a suite."""
    return [
        row["TC_ID"] for row in read_rows(_DATA_PATH, sheet=_SHEET)
        if (not action or _str_or_empty(row.get("ACTION")).casefold() == action.casefold())
        and (not module or _str_or_empty(row.get("MODULE")).casefold() == module.casefold())
    ]


class SwingPassData:
    @classmethod
    def load(cls, tc_id: str | None = None):
        if tc_id:
            row = get_rows_by_tc_id(_DATA_PATH, tc_id, id_column="TC_ID", sheet=_SHEET)[0]
        else:
            row = read_row(_DATA_PATH, sheet=_SHEET)
        cls.TC_ID = row.get("TC_ID")
        cls.TC_NAME = row.get("TC_NAME")
        # --- run control / traceability (read by the suite, not by a step) ---
        cls.MODULE = row.get("MODULE")
        cls.TEST_FUNCTION = row.get("TEST_FUNCTION")
        cls.PRIORITY = row.get("PRIORITY")
        cls.MARKERS = _list(row.get("MARKERS"))
        cls.APP_STATE = _str_or_empty(row.get("APP_STATE")) or "clear"
        cls.ACTION = _str_or_empty(row.get("ACTION")) or "run"
        cls.RUN = cls.ACTION.casefold() != "skip"
        cls.SKIP_REASON = row.get("SKIP_REASON")
        cls.PRECONDITION = row.get("PRECONDITION")
        # --- login ---
        cls.COUNTRY = row.get("COUNTRY")
        cls.PHONE_NUMBER = _str_or_empty(row.get("PHONE_NUMBER"))
        cls.VERIFICATION_METHOD = (
            str(row.get("VERIFICATION_METHOD") or "whatsapp").strip().lower()
        )
        cls.OTP = _str_or_empty(row.get("OTP"))
        # --- membership / billing ---
        cls.PAYMENT_OPTION = row.get("PAYMENT_OPTION")
        cls.BILLING_PLAN = row.get("BILLING_PLAN")
        cls.NEW_PLAN = row.get("NEW_PLAN")
        cls.BILLING_METHOD = row.get("BILLING_METHOD")
        cls.CARD_INDEX = _int_or_default(row.get("CARD_INDEX"))
        cls.EWALLET = row.get("EWALLET")
        cls.PROMO_CODE = row.get("PROMO_CODE")
        cls.CANCEL_REASON = row.get("CANCEL_REASON")
        cls.FULL_NAME = row.get("FULL_NAME")
        # whether the flow goes through the final confirm/slide step
        cls.CONFIRM = _bool_or_default(row.get("CONFIRM"))
        cls.EXPECTED_RESULT = row.get("EXPECTED_RESULT")
        return row


SwingPassData.load()
