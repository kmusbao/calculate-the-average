from dataclasses import dataclass
from collections import defaultdict
from typing import List


@dataclass
class Product:
    brand: str
    rating: float
    price: float

    @classmethod
    def from_dict(cls, data: dict):
        try:
            return cls(
                brand=data.get("brand"),
                rating=float(data.get("rating")),
                price=float(data.get("price")),
            )
        except ValueError:
            return None


