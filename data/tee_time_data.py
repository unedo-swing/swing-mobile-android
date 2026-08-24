import os

from utils.excel_reader import find_rows, get_rows_by_tc_id, read_row
_DATA_PATH = os.getenv(
    "TEST_DATA_MOBILE",
    os.path.join(os.path.dirname(__file__), "test_data_swing_mobile.xlsx"),
)
_SHEET = os.getenv("TEE_TIME_SHEET", "Tee_Time")
_PLAYERS_SHEET = os.getenv("TEE_TIME_PLAYERS_SHEET", "Tee_Time_Player")
_ADD_ONS_SHEET = os.getenv("TEE_TIME_ADDONS_SHEET", "Tee_Time_Add_Ons")


def _str_or_empty(value):
    """str(value), but an empty cell stays empty — a phone read from Excel can
    come back as a number, and a blank must not become the text "None"."""
    return "" if value in (None, "") else str(value)


def load_players(tc_id: str) -> list[dict]:
    rows = find_rows(_DATA_PATH, "TC_ID", tc_id, sheet=_PLAYERS_SHEET)
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


def load_add_ons(tc_id: str, player_name: str | None = None) -> list[dict]:
    rows = find_rows(_DATA_PATH, "TC_ID", tc_id, sheet=_ADD_ONS_SHEET)
    add_ons = []
    for row in rows:
        name = row.get("ADD_ONS_NAME")
        if name in (None, ""):
            continue
        owner = row.get("PLAYER_NAME") or ""
        if player_name and owner and owner != player_name:
            continue
        add_ons.append({
            "player_name": owner,
            "add_ons_name": name,
            "add_ons_qty": int(row.get("ADD_ONS_QTY") or 1),
        })
    return add_ons


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
        cls.COURSE_NAME = row.get("COURSE_NAME")
        cls.BOOKING_DATE = row.get("BOOKING_DATE")    
        cls.PREFERRED_TIME = row.get("PREFERRED_TIME")
        cls.HOST_NAME = row.get("HOST_NAME")
        cls.HOST_PROMO = row.get("HOST_PROMO") or ""
        cls.PROMO_NAME = row.get("PROMO_NAME") or cls.HOST_PROMO
        cls.PROMO_CODE = row.get("PROMO_CODE") or ""
        cls.PAYMENT_METHOD = row.get("PAYMENT_METHOD")
        cls.PAYMENT_CARD = cls.PAYMENT_METHOD
        cls.EXPECTED_RESULT = row.get("EXPECTED_RESULT")
        return cls

TeeTimeData.load()
