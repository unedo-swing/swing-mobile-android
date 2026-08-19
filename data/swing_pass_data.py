from locators.swing_pass.cancel_swing_pass_locators import CancelSwingPassLocators


class SwingPassData:
    # The plan to switch to. Matched as a substring of the plan card's duration
    # line, so it has to be a duration the account is NOT already on — the
    # current plan has no radio and cannot be picked.
    NEW_PLAN = '3 months'

    # Saved cards are picked by position, not by label: several of the test
    # account's cards read exactly "VISA 2503", so a label identifies nothing.
    CARD_INDEX = 1

    EWALLET = 'OVO'

    # A fragment, not the full label — the cancellation reasons mix curly
    # apostrophes, a missing one, and a duplicated word. Taken from the locators
    # class so there is one source of truth.
    CANCEL_REASON = CancelSwingPassLocators.REASON_TOO_EXPENSIVE
