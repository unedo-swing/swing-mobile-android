"""Field-by-field comparison of a booking summary across screens.

The same booking is rendered three times — booking confirmation (before
payment), confirmed booking (after payment) and booking details — with small
wording differences ("2 bays" vs "2 bay", "RM 140" vs "RM 140.00"). Text
fields are matched as a substring of what the screen shows, amounts by value.
"""

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
