"""
Minimal Excel reader for test data.

Reads a workbook laid out as a single header row followed by one or more value
rows, and returns rows as dicts keyed by the header text. Used by data/*_data.py
so QA can maintain test data in Excel instead of editing Python.

Layout expected:

    | REGION    | RANGE_NAME              | DATE           | ... |   <- headers
    | Indonesia | Albatross Driving Range | 10 August 2026 | ... |   <- values

Column order does not matter — columns are matched by header name.
"""


def read_rows(path: str, sheet: str | None = None) -> list[dict]:
    """Return every value row of ``path`` as a list of ``{header: value}`` dicts.

    Blank rows are skipped. Cell values are returned as-is (numbers stay numbers)
    except strings, which are stripped of surrounding whitespace.
    """
    # imported lazily so pytest collection never fails just because openpyxl
    # isn't installed yet — the error only surfaces when data is actually read.
    import openpyxl

    try:
        wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Test data workbook not found: {path}\n"
            f"Create it with a header row of column names and a row of values."
        )

    try:
        ws = wb[sheet] if sheet else wb.active
        row_iter = ws.iter_rows(values_only=True)

        try:
            header_cells = next(row_iter)
        except StopIteration:
            return []
        headers = [str(h).strip() if h is not None else "" for h in header_cells]

        records = []
        for values in row_iter:
            values = list(values)
            if all(v is None or str(v).strip() == "" for v in values):
                continue  # skip blank rows
            record = {}
            for i, header in enumerate(headers):
                if not header:
                    continue
                value = values[i] if i < len(values) else None
                if value is None:
                    record[header] = ""
                elif isinstance(value, str):
                    record[header] = value.strip()
                else:
                    record[header] = value
            records.append(record)
        return records
    finally:
        wb.close()


def read_row(path: str, required_headers: list[str] | None = None,
             sheet: str | None = None, index: int = 0) -> dict:
    rows = read_rows(path, sheet=sheet)
    if not rows:
        raise ValueError(f"No data rows found in {path}")
    row = rows[index]
    if required_headers:
        missing = [h for h in required_headers if h not in row]
        if missing:
            raise KeyError(
                f"{path} is missing column(s): {', '.join(missing)}. "
                f"Expected headers: {', '.join(required_headers)}"
            )
    return row


def find_rows(path: str, match_column: str, match_value, sheet: str | None = None) -> list[dict]:
    """Return every row whose ``match_column`` equals ``match_value``.

    Matching is done on the trimmed string form, so 1 and "1" compare equal.
    """
    target = str(match_value).strip()
    return [
        r for r in read_rows(path, sheet=sheet)
        if str(r.get(match_column, "")).strip() == target
    ]


def get_rows_by_tc_id(path: str, tc_id, id_column: str = "TC_id",
                      sheet: str | None = None) -> list[dict]:
    """Return all rows for a given test-case id.

    Raises if no row matches, so a typo'd/absent TC id fails loudly instead of
    silently running with no data.
    """
    rows = find_rows(path, id_column, tc_id, sheet=sheet)
    if not rows:
        raise ValueError(f"No rows found in {path} for {id_column}={tc_id!r}")
    return rows


def get_column(rows: list[dict], column: str, default=None) -> list:
    """Pull one column out of a list of rows, e.g. every ADDON_NAME for a TC."""
    return [r.get(column, default) for r in rows]


def get_value(rows: list[dict], column: str, default=None, index: int = 0):
    """Pull one column from a single row (the first by default)."""
    if not rows:
        return default
    return rows[index].get(column, default)
