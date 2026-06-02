
def advisory_fee(hours, rate=150):
    """Merlin's fee: hours x rate, plus a 10% surcharge over 40 hours."""
    base = hours * rate
    if hours > 40:
        base = base * 1.10
    return round(base, 2)
