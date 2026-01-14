from datetime import datetime

def current_month():
    return datetime.now().month

def month_from_date(date_str: str) -> int:
    return int(date_str.split("-")[1])

def print_table(rows: list[dict], headers: list[str]):
    if not rows:
        print("No data.")
        return

    # Calculate column widths
    widths = []
    for header in headers:
        max_width = max(
            len(str(header)),
            max(len(str(row.get(header, ""))) for row in rows)
        )
        widths.append(max_width)

    # Header row
    header_line = "  ".join(
        header.ljust(widths[i]) for i, header in enumerate(headers)
    )
    separator = "  ".join("-" * widths[i] for i in range(len(headers)))

    print(header_line)
    print(separator)

    # Data rows
    for row in rows:
        print("  ".join(
            str(row.get(header, "")).ljust(widths[i])
            for i, header in enumerate(headers)
        ))

