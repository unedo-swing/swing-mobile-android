"""Currency-aware money parsing shared by the booking screens.

The app renders the same field differently per country and per screen —
"RM 140" here and "RM 140.00" there, "Rp. 150.000" and "Rp. 150,000" — so
amounts are compared as numbers, never as text.

Separators are read by shape rather than by currency: the app writes prices
with either no decimals or exactly two, so the last separator is a decimal
point only when exactly two digits follow it. Everything else is a thousands
separator. That keeps "Rp. 150.000" (a hundred fifty thousand) apart from
"RM 140.00" (a hundred forty) without having to trust the currency symbol.
"""

import re
from decimal import Decimal, InvalidOperation


AMOUNT_RE = re.compile(r"\b(RM|Rp)\.?\s*([\d.,]*\d)")
_NUMBER_RE = re.compile(r"\d[\d.,]*")


def amounts(text: str) -> list[str]:
    """Every amount in a row, in order: "Subtotal\\nRM 150.00\\nRM 140.00"."""
    return [match.group() for match in AMOUNT_RE.finditer(text or "")]


def last_amount(text: str, default: str = "") -> str:
    """The amount actually charged — rows list the original price first."""
    found = amounts(text)
    return found[-1] if found else default


def parse_amount(text: str) -> Decimal | None:
    match = AMOUNT_RE.search(text or "")
    digits = match.group(2) if match else None
    if digits is None:
        match = _NUMBER_RE.search(text or "")
        if not match:
            return None
        digits = match.group()

    digits = digits.rstrip(".,")
    decimals = ""
    separator = max(digits.rfind("."), digits.rfind(","))
    if separator != -1 and len(digits) - separator - 1 == 2:
        decimals = digits[separator + 1:]
        digits = digits[:separator]

    whole = re.sub(r"\D", "", digits) or "0"
    try:
        return Decimal(f"{whole}.{decimals}" if decimals else whole)
    except InvalidOperation:
        return None


def amounts_equal(expected: str, actual: str) -> bool:
    left, right = parse_amount(expected), parse_amount(actual)
    return left is not None and left == right
