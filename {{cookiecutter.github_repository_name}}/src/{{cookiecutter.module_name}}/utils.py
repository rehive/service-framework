from decimal import Decimal


def to_cents(amount: Decimal, divisibility: int) -> int:
    return int(amount * Decimal('10')**Decimal(divisibility))


def from_cents(amount: int, divisibility: int) -> Decimal:
    return Decimal(amount) / Decimal('10')**Decimal(divisibility)
