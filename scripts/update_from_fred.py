import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path


FRED_PATH = Path("archive/fred_sp500.csv")
DATA_PATH = Path("data/data.csv")
HEADER = [
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


def parse_date(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%d")


def load_existing_rows() -> list[dict[str, str]]:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Missing base dataset at {DATA_PATH}. Keep the historical Shiller CSV and only append via FRED."
        )

    with DATA_PATH.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        raise ValueError(f"No rows found in {DATA_PATH}.")
    return rows


def load_fred_monthly_average() -> dict[str, float]:
    if not FRED_PATH.exists():
        raise FileNotFoundError(f"Missing archived FRED CSV at {FRED_PATH}.")

    sums = defaultdict(float)
    counts = defaultdict(int)

    with FRED_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        date_col = None
        if "DATE" in reader.fieldnames:
            date_col = "DATE"
        elif "observation_date" in reader.fieldnames:
            date_col = "observation_date"
        if date_col is None or "SP500" not in reader.fieldnames:
            raise ValueError("FRED CSV must contain DATE/observation_date and SP500 columns.")

        for row in reader:
            date_raw = (row.get(date_col) or "").strip()
            sp500_raw = (row.get("SP500") or "").strip()
            if not date_raw or not sp500_raw or sp500_raw == ".":
                continue
            try:
                dt = parse_date(date_raw)
                sp500 = float(sp500_raw)
            except ValueError:
                continue
            month_key = dt.strftime("%Y-%m-01")
            sums[month_key] += sp500
            counts[month_key] += 1

    out = {}
    for month_key, total in sums.items():
        out[month_key] = total / counts[month_key]
    return out


def main() -> None:
    rows = load_existing_rows()
    last_date = max(parse_date(row["Date"]) for row in rows)
    fred_monthly = load_fred_monthly_average()

    def is_zero(value: str) -> bool:
        try:
            return float(value) == 0.0
        except (TypeError, ValueError):
            return False

    # Treat rows with non-zero fundamentals as historical Shiller-backed records.
    shiller_dates = []
    for row in rows:
        if (
            not is_zero(row.get("Dividend", "0"))
            or not is_zero(row.get("Earnings", "0"))
            or not is_zero(row.get("Consumer Price Index", "0"))
            or not is_zero(row.get("Long Interest Rate", "0"))
            or not is_zero(row.get("Real Price", "0"))
            or not is_zero(row.get("Real Dividend", "0"))
            or not is_zero(row.get("Real Earnings", "0"))
            or not is_zero(row.get("PE10", "0"))
        ):
            shiller_dates.append(parse_date(row["Date"]))
    last_shiller_date = max(shiller_dates) if shiller_dates else datetime.min

    new_rows = []
    for month_key in sorted(fred_monthly):
        month_dt = parse_date(month_key)
        if month_dt <= last_date:
            continue
        new_rows.append(
            {
                "Date": month_key,
                "SP500": f"{fred_monthly[month_key]:.2f}",
                "Dividend": "0.0",
                "Earnings": "0.0",
                "Consumer Price Index": "0.0",
                "Long Interest Rate": "0.0",
                "Real Price": "0.0",
                "Real Dividend": "0.0",
                "Real Earnings": "0.0",
                "PE10": "0.0",
            }
        )

    by_date = {row["Date"]: row for row in rows}
    for row in new_rows:
        by_date[row["Date"]] = row

    # Normalize all FRED-only extension rows to 2dp SP500 formatting.
    for month_key, month_sp500 in fred_monthly.items():
        month_dt = parse_date(month_key)
        if month_dt <= last_shiller_date:
            continue
        if month_key in by_date:
            by_date[month_key]["SP500"] = f"{month_sp500:.2f}"
            by_date[month_key]["Dividend"] = "0.0"
            by_date[month_key]["Earnings"] = "0.0"
            by_date[month_key]["Consumer Price Index"] = "0.0"
            by_date[month_key]["Long Interest Rate"] = "0.0"
            by_date[month_key]["Real Price"] = "0.0"
            by_date[month_key]["Real Dividend"] = "0.0"
            by_date[month_key]["Real Earnings"] = "0.0"
            by_date[month_key]["PE10"] = "0.0"

    ordered_rows = [by_date[d] for d in sorted(by_date)]
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DATA_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER, lineterminator="\n")
        writer.writeheader()
        writer.writerows(ordered_rows)

    print(f"Updated {DATA_PATH} with {len(new_rows)} new monthly rows from {FRED_PATH}.")


if __name__ == "__main__":
    main()
