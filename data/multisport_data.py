import os

from utils.excel_reader import get_rows_by_tc_id

_DATA_PATH = os.getenv(
    "TEST_DATA_MOBILE",
    os.path.join(os.path.dirname(__file__), "test_data_swing_mobile.xlsx"),
)
_SHEET = os.getenv("MULTISPORT_SHEET", "Multisport")


class MultisportData:

    TC_ID: str = ""
    TC_NAME: str = ""
    SPORT_NAME: str = ""
    VENUE_NAME: str = ""
    TITLE_SCHEDULE: str = ""
    HOW_MUCH_SCHEDULE: int = 1
    PLAYER_NAME: str = ""
    PAYMENT_METHOD: str = ""

    @classmethod
    def _assign(cls, row: dict):
        cls.TC_ID = row.get("TC_ID", "")
        cls.TC_NAME = row.get("TC_NAME", "")
        cls.SPORT_NAME = row.get("SPORT_NAME", "")
        cls.VENUE_NAME = row.get("VENUE_NAME", "")
        cls.TITLE_SCHEDULE = row.get("TITLE_SCHEDULE", "")
        cls.HOW_MUCH_SCHEDULE = cls._int_or_empty(row.get("HOW_MUCH_SCHEDULE"))
        cls.PLAYER_NAME = row.get("PLAYER_NAME", "")
        cls.PAYMENT_METHOD = row.get("PAYMENT_METHOD", "")

    @staticmethod
    def _int_or_empty(value):
        return 1 if value in (None, "") else int(value)

    @classmethod
    def load(cls, tc_id: str | None = None):
        if tc_id:
            row = get_rows_by_tc_id(_DATA_PATH, tc_id,
                                     id_column="TC_ID", sheet=_SHEET)[0]
        else:
            from utils.excel_reader import read_row
            row = read_row(_DATA_PATH, sheet=_SHEET)
        cls._assign(row)
        return cls


MultisportData.load()
