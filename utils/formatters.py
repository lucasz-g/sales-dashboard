MONTH_ORDER = [
    "Jan",
    "Fev",
    "Mar",
    "Abr",
    "Mai",
    "Jun",
    "Jul",
    "Ago",
    "Set",
    "Out",
    "Nov",
    "Dez",
]


def format_currency(value: float) -> str:
    return format_compact_number(value, prefix="R$")


def format_compact_number(value: float, prefix: str = "") -> str:
    if value >= 1_000_000_000:
        return f"{prefix}{value / 1_000_000_000:.1f}B"
    elif value >= 1_000_000:
        return f"{prefix}{value / 1_000_000:.1f}M"
    elif value >= 1_000:
        return f"{prefix}{value / 1_000:.1f}K"
    else:
        return f"{prefix}{value:.2f}"


def month_name(month_number: int) -> str:
    return MONTH_ORDER[month_number - 1]
