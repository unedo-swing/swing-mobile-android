"""Field-by-field comparison of a booking summary across screens.

The same booking is rendered three times — booking confirmation (before
payment), confirmed booking (after payment) and booking details — with small
wording differences ("2 bays" vs "2 bay", "RM 140" vs "RM 140.00"). Text
fields are matched as a substring of what the screen shows, amounts by value.
"""

import re

from utils.amounts import amounts_equal


AMOUNT_FIELDS = {"Total", "Subtotal", "Processing fee"}


def summary_failures(expected: dict, actual: dict) -> list[str]:
    failures = []
    for key, exp in expected.items():
        # a field the caller did not ask about, or one the screen never showed
        if exp is None or exp == "":
            continue
        act = actual.get(key, "")
        if key in AMOUNT_FIELDS:
            if not amounts_equal(str(exp), str(act)):
                failures.append(f"{key}: expected {exp!r}, got {act!r}")
        elif str(exp) not in str(act):
            failures.append(f"{key}: expected {exp!r} in actual {act!r}")
    return failures


def assert_summary(screen: str, expected: dict, actual: dict):
    failures = summary_failures(expected, actual)
    assert not failures, f"{screen} mismatch -> " + "; ".join(failures)


# ---------------------------------------------------------------------------
# the same booking read on two screens
# ---------------------------------------------------------------------------
def compare_summary(before: dict, after: dict, number_fields: tuple = (),
                    amount_fields: tuple = ()) -> dict:
    """Diff one booking across two screens: ``{field: (before, after)}``.

    Unlike :func:`summary_failures`, which checks a screen against what the
    test expected, this compares two screens against each other and neither
    side is the authority — so it reports every field that drifted at once
    instead of stopping at the first.

    ``amount_fields`` are compared by value ("Rp. 150.000" == "Rp 150,000"),
    ``number_fields`` by their first number ("1" == "1 Player"), and the rest
    as text where one side containing the other counts as a match: the two
    screens introduce the same value differently ("31 August 2026" against
    "Sunday, 31 August 2026").

    A field the first screen left blank counts as a mismatch — an empty value
    means it could not be read, not that the two screens agree.
    """
    return {
        field: (value, after.get(field, ""))
        for field, value in before.items()
        if not _matches(field, value, after.get(field, ""), number_fields, amount_fields)
    }


def _matches(field: str, before, after, number_fields: tuple, amount_fields: tuple) -> bool:
    if field in amount_fields:
        return amounts_equal(str(before), str(after))
    if field in number_fields:
        left, right = _first_number(before), _first_number(after)
        return bool(left) and left == right
    left, right = _norm(before), _norm(after)
    return bool(left) and bool(right) and (left in right or right in left)


def _norm(value) -> str:
    return " ".join(str(value or "").split()).casefold()


def _first_number(value) -> str:
    match = re.search(r"\d+", str(value or ""))
    return match.group() if match else ""
