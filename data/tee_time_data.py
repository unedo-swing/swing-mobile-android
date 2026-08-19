import os

from utils.excel_reader import get_rows_by_tc_id, read_row

# Where the test data lives — file path + worksheets (all overridable by env).
# One row per test case on the scenario sheet, and zero or more player rows
# sharing that TC_ID on the players sheet.
_DATA_PATH = os.getenv(
    "TEST_DATA_MOBILE",
    os.path.join(os.path.dirname(__file__), "test_data_swing_mobile.xlsx"),
)
_SHEET = os.getenv("TEE_TIME_SHEET", "Tee_Time")
_PLAYERS_SHEET = os.getenv("TEE_TIME_PLAYERS_SHEET", "Tee_Time_Player")


def _str_or_empty(value):
    """str(value), but an empty cell stays empty — a phone read from Excel can
    come back as a number, and a blank must not become the text "None"."""
    return "" if value in (None, "") else str(value)


def load_players(tc_id: str) -> list[dict]:
    rows = get_rows_by_tc_id(_DATA_PATH, tc_id, id_column="TC_ID", sheet=_PLAYERS_SHEET)
    players = []
    for row in rows:
        method = str(row.get("METHOD") or "manual").strip().lower()
        player = {"method": method}
        if method == "search":
            player["name"] = row.get("NAME")
        else:
            player["first_name"] = row.get("FIRST_NAME")
            player["last_name"] = row.get("LAST_NAME")
            player["phone"] = _str_or_empty(row.get("PHONE"))
            if row.get("EMAIL"):
                player["email"] = row.get("EMAIL")
        if row.get("PROMO"):
            player["promo"] = row.get("PROMO")
        players.append(player)
    return players


class TeeTimeData:
    @classmethod
    def load(cls, tc_id: str | None = None):
        if tc_id:
            row = get_rows_by_tc_id(_DATA_PATH, tc_id, id_column="TC_ID", sheet=_SHEET)[0]
        else:
            row = read_row(_DATA_PATH, sheet=_SHEET)
        cls.TC_ID = row.get("TC_ID")
        cls.TC_NAME = row.get("TC_NAME")
        cls.REGION = row.get("REGION")
        # what to type into Explore search, vs. the course title it should open
        cls.SEARCH_QUERY = row.get("SEARCH_QUERY")
        cls.COURSE_NAME = row.get("COURSE_NAME")
        cls.CALENDAR_DATE = row.get("CALENDAR_DATE")    # e.g. "19 August 2026"
        cls.PREFERRED_TIME = row.get("PREFERRED_TIME")  # slot, e.g. "09:30 - 10:00"
        # the logged-in user — promo rows are addressed by player name
        cls.HOST_NAME = row.get("HOST_NAME")
        # --- promo ---
        # HOST_PROMO is what the app applies on its own; PROMO_NAME is the one
        # the test asks for, and falls back to it when the cell is blank.
        cls.HOST_PROMO = row.get("HOST_PROMO") or ""
        cls.PROMO_NAME = row.get("PROMO_NAME") or cls.HOST_PROMO
        cls.PROMO_CODE = row.get("PROMO_CODE") or ""
        cls.PAYMENT_METHOD = row.get("PAYMENT_METHOD")
        cls.PAYMENT_CARD = cls.PAYMENT_METHOD
        cls.EXPECTED_RESULT = row.get("EXPECTED_RESULT")
        return cls


# default: first row, so D.X works even before a TC_ID is selected
TeeTimeData.load()
