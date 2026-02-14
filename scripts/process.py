import csv
from pathlib import Path

from date_utils import parse_shiller_date


BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_XLS = BASE_DIR / "archive" / "shiller.xls"
OUTPUT_CSV = BASE_DIR / "data" / "data.csv"
OUTPUT_HEADER = [
    "Date",
    "SP500",
    "Dividend",
    "Earnings",
    "Consumer Price Index",
    "Long Interest Rate",
    "Real Price",
    "Real Dividend",
    "Real Earnings",
    "PE10",
]


def _try_parse_shiller_date(value) -> str | None:
    try:
        return parse_shiller_date(value)
    except ValueError:
        return None


def _to_float(value) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def process() -> None:
    print("Loading data...")
    import xlrd

    workbook = xlrd.open_workbook(INPUT_XLS.as_posix())
    sheet = workbook.sheet_by_name("Data")
    rows = []

    # Header starts on row 8 in the workbook (1-indexed); data starts on row 9.
    for row_idx in range(8, sheet.nrows):
        date_str = _try_parse_shiller_date(sheet.cell_value(row_idx, 0))
        if date_str is None:
            continue

        rows.append(
            {
                "Date": date_str,
                "SP500": _to_float(sheet.cell_value(row_idx, 1)),
                "Dividend": _to_float(sheet.cell_value(row_idx, 2)),
                "Earnings": _to_float(sheet.cell_value(row_idx, 3)),
                "Consumer Price Index": round(_to_float(sheet.cell_value(row_idx, 4)), 2),
                "Long Interest Rate": round(_to_float(sheet.cell_value(row_idx, 6)), 2),
                "Real Price": round(_to_float(sheet.cell_value(row_idx, 7)), 2),
                "Real Dividend": round(_to_float(sheet.cell_value(row_idx, 8)), 2),
                "Real Earnings": round(_to_float(sheet.cell_value(row_idx, 10)), 2),
                "PE10": round(_to_float(sheet.cell_value(row_idx, 12)), 2),
            }
        )

    print(f"Shape of the data: ({len(rows)}, {len(OUTPUT_HEADER)})")
    print("Saving data...")
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_HEADER, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print("Data saved successfully")


if __name__ == "__main__":
    process()
