def tier_dict(low: float, med: float, high: float) -> dict[str, float]:
    return {
        "<=500": low,
        "500-1000": med,
        ">1000": high,
    }
