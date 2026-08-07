import os

from utils.excel_reader import get_rows_by_tc_id, read_row

_DATA_PATH = os.getenv(
    "TEST_DATA_MOBILE",
    os.path.join(os.path.dirname(__file__), "test_data_swing_mobile.xlsx"),
)
_SCENARIO_SHEET = os.getenv("TEE_TIME_SHEET", "Tee_Time")
_PLAYERS_SHEET = os.getenv("TEE_TIME_PLAYERS_SHEET", "Tee_Time_Player")


def load_players(tc_id: str) -> list[dict]:
    """Read the players for a test case from the Tee_Time_Player sheet (by TC_ID)
    and return them in the shape TeeTimeFlow.add_players() expects:

        {"method": "manual", "first_name", "last_name", "phone", ["email"], ["promo"]}
        {"method": "search", "name", ["promo"]}
    """
    rows = get_rows_by_tc_id(_DATA_PATH, tc_id, id_column="TC_ID", sheet=_PLAYERS_SHEET)
    players = []
    for r in rows:
        method = str(r.get("METHOD") or "manual").strip().lower()
        player = {"method": method}
        if method == "search":
            player["name"] = r.get("NAME")
        else:
            player["first_name"] = r.get("FIRST_NAME")
            player["last_name"] = r.get("LAST_NAME")
            phone = r.get("PHONE")
            player["phone"] = "" if phone in (None, "") else str(phone)
            if r.get("EMAIL"):
                player["email"] = r.get("EMAIL")
        if r.get("PROMO"):
            player["promo"] = r.get("PROMO")
        players.append(player)
    return players


class TeeTimeData:
    """Tee-time test data.

    Scenario-level fields (REGION, COURSE_NAME, CALENDAR_DATE, ...) are sourced
    from the ``Tee_Time`` sheet — call ``TeeTimeData.load(tc_id)`` to switch to a
    specific test case by its TC_ID column (the tee-time tests do this per test).
    Without a tc_id the first row is used, so ``D`` works even before a TC_ID is
    selected. Player rows live in the separate ``Tee_Time_Player`` sheet and are
    read via ``load_players(tc_id)``.

    The class attributes below are static fallbacks: they seed sensible values and
    keep fields the sheet doesn't carry (PLAYER_*, PAYMENT_EWALLET, PLAYERS)
    available; ``load()`` overrides the sheet-backed ones.
    """

    @classmethod
    def load(cls, tc_id: str | None = None):
        if tc_id:
            row = get_rows_by_tc_id(
                _DATA_PATH, tc_id, id_column="TC_ID", sheet=_SCENARIO_SHEET
            )[0]
        else:
            row = read_row(_DATA_PATH, sheet=_SCENARIO_SHEET)

        def _val(key, default=None):
            v = row.get(key)
            return default if v in (None, "") else v

        cls.TC_ID = _val("TC_ID")
        cls.TC_NAME = _val("TC_NAME")
        cls.REGION = _val("REGION", cls.REGION)
        cls.SEARCH_QUERY = _val("SEARCH_QUERY", cls.SEARCH_QUERY)
        cls.COURSE_NAME = _val("COURSE_NAME", cls.COURSE_NAME)
        cls.CALENDAR_DATE = _val("CALENDAR_DATE", cls.CALENDAR_DATE)
        cls.PREFERRED_TIME = _val("PREFERRED_TIME", cls.PREFERRED_TIME)
        cls.HOST_NAME = _val("HOST_NAME", cls.HOST_NAME)
        # HOST_PROMO: the promo expected/applied on the host card. Empty in a
        # "without promo" row -> "" so the flow removes the auto-applied one.
        cls.HOST_PROMO = _val("HOST_PROMO", "")
        # PROMO_NAME / PROMO_CODE: the promo the test applies. Fall back to
        # HOST_PROMO so existing tests that reference D.PROMO_NAME keep working.
        cls.PROMO_NAME = _val("PROMO_NAME", cls.HOST_PROMO)
        cls.PROMO_CODE = _val("PROMO_CODE", "")
        # The sheet carries one PAYMENT_METHOD; expose it under both names so
        # tests referencing either D.PAYMENT_METHOD or D.PAYMENT_CARD resolve.
        payment = _val("PAYMENT_METHOD", cls.PAYMENT_CARD)
        cls.PAYMENT_METHOD = payment
        cls.PAYMENT_CARD = payment
        cls.EXPECTED_RESULT = _val("EXPECTED_RESULT")
        return cls

    # Home > Select region bottom sheet
    REGION = "Indonesia"

    # Explore search
    SEARCH_QUERY = "Rainbow Hills"

    # Expected result / details title
    COURSE_NAME = "Rainbow Hills Golf"

    # Calendar: the day to pick inside the opened calendar (adjust to your run)
    CALENDAR_DATE = "01 August 2026"
    
    PREFERRED_TIME = "08:30 - 09:00"

    # Add a player — manual form
    PLAYER_FIRST_NAME = "Tam"
    PLAYER_LAST_NAME = "Lembong"
    PLAYER_PHONE = "82165162549"
    PLAYER_EMAIL = "tam.lembong@example.com"

    # Add a player — search an existing friend
    PLAYER_SEARCH_QUERY = "Tam"
    PLAYER_FRIEND_NAME = "Tam Lembong"

    # Add a player — a third player (manual)
    PLAYER3_FIRST_NAME = "Budi"
    PLAYER3_LAST_NAME = "Santoso"
    PLAYER3_PHONE = "81299887766"
    PLAYER3_EMAIL = "budi.santoso@example.com"

    # All players to add, looped by the flow. Each item has a "method":
    #   "manual" -> needs first_name, last_name, phone, (optional) email
    #   "search" -> needs name (the friend's full name to search + select)
    # Optional "promo": if set, the flow applies it after adding the player;
    # if omitted, the flow removes any promo that was auto-applied.
    PLAYERS = [
        {
            "method": "manual",
            "first_name": PLAYER_FIRST_NAME,
            "last_name": PLAYER_LAST_NAME,
            "phone": PLAYER_PHONE,
            "email": PLAYER_EMAIL,
            # no "promo" -> auto-applied promo (if any) is removed
        },
        {
            "method": "search",
            "name": PLAYER_FRIEND_NAME,
            "promo": "[Testing] Automation Tee time Promo",  # apply this promo
        },
        {
            "method": "manual",
            "first_name": PLAYER3_FIRST_NAME,
            "last_name": PLAYER3_LAST_NAME,
            "phone": PLAYER3_PHONE,
            "email": PLAYER3_EMAIL,
        },
    ]

    # Change payment method
    PAYMENT_CARD = "VISA 0014"
    PAYMENT_EWALLET = "Gopay"

    # Host (the logged-in user) — used for per-player promo on the host card
    HOST_NAME = "QA Auto Mation"

    # Change promo
    PROMO_NAME = "[Testing] Automation Tee time Promo"
    PROMO_CODE = "SWING123"


# default: first row of the Tee_Time sheet, so D.X works even before a TC_ID is
# selected (mirrors DrivingRangeData).
TeeTimeData.load()
