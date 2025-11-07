from abc import ABC, abstractmethod
from typing import List, Dict

from models.product import Product

ALLOWED_REPORTS = {"average-rating": "Average rating", "average-price-in-brand": "Average price in brand"}

class Report(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def calculate_average_values(self, rows: List[Product]) -> Dict[str, float]:
        pass


class AverageReport(Report):
    def __init__(self, report_type: str):
        self.report_type = report_type

    @property
    def name(self) -> str:
        return f"Brand {ALLOWED_REPORTS[self.report_type]}"

    def calculate_average_values(self, rows: List[Product]) -> Dict[str, float]:
        """Calculates averages depending on report type."""
        brand_data: dict[str, list[float]] = {}

        field_getters = {
            "average-rating": lambda p: p.rating,
            "average-price-in-brand": lambda p: p.price,
        }

        if self.report_type not in field_getters:
            raise ValueError(f"Unknown report type: {self.report_type}")

        get_value = field_getters[self.report_type]

        for product in rows:
            if not product or not getattr(product, "brand", None):
                continue
            try:
                value = get_value(product)
            except (ValueError, TypeError):
                continue

            brand_data.setdefault(product.brand, []).append(value)

        return {
            brand: round(sum(values) / len(values), 1) for brand, values in brand_data.items() if values
        }
