import os

from utils.excel_reader import get_rows_by_tc_id, read_row

_DATA_PATH = os.getenv(
    "TEST_DATA_MOBILE",
    os.path.join(os.path.dirname(__file__), "test_data_swing_mobile.xlsx"),
)
_SHEET = os.getenv("EVENTS_SHEET", "Events")


class EventsData:
    TC_ID = ""
    TC_NAME = ""
    EVENT_NAME = ""
    BOOKING_TYPE = ""
    REGISTRATION_TIME = ""
    PLAYER_NAME = ""
    PAYMENT_METHOD = ""
    SWITCH_REGISTRATION_TYPE = ""

    @classmethod
    def _assign(cls, row: dict):
        cls.TC_ID = row.get("TC_ID", "")
        cls.TC_NAME = row.get("TC_NAME", "")
        cls.EVENT_NAME = row.get("EVENT_NAME", "")
        cls.BOOKING_TYPE = row.get("BOOKING_TYPE", "")
        cls.REGISTRATION_TIME = row.get("REGISTRATION_TIME", "")
        cls.PLAYER_NAME = row.get("PLAYER_NAME", "")
        cls.PAYMENT_METHOD = row.get("PAYMENT_METHOD", "")
        cls.SWITCH_REGISTRATION_TYPE = row.get("SWITCH_REGISTRATION_TYPE", "")

    @classmethod
    def load(cls, tc_id: str | None = None):
        try:
            if tc_id:
                row = get_rows_by_tc_id(_DATA_PATH, tc_id, id_column="TC_ID", sheet=_SHEET)[0]
            else:
                row = read_row(_DATA_PATH, sheet=_SHEET)
        except (FileNotFoundError, KeyError, ValueError) as e:
            print(f"[events_data] WARNING: empty data ({e}). "
                  f"Create sheet '{_SHEET}' in {_DATA_PATH}.")
            cls._assign({})
            return cls
        cls._assign(row)
        return cls


EventsData.load()
