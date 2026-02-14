def parse_shiller_date(value) -> str:
    """Convert Shiller's YYYY.MM-style value (e.g. 2021.01, 2021.1) to YYYY-MM-01."""
    try:
        numeric_value = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid Shiller date value: {value!r}") from exc

    year = int(numeric_value)
    month = int(round((numeric_value - year) * 100))
    if not 1 <= month <= 12:
        raise ValueError(f"Invalid Shiller month parsed from {value!r}: {month}")

    return f"{year:04d}-{month:02d}-01"
