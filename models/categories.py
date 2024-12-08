from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Categories:
    expenses: Dict[str, List[float]] = field(
        default_factory=lambda: {
            "rent": [],
            "groceries": [],
            "travel": [],
            "going_out": [],
            "shopping": [],
            "subscriptions": [],
            "investments": [],
            "savings": [],
            "uncategorized": [],
        }
    )
    income: Dict[str, List[float]] = field(
        default_factory=lambda: {
            "salary": [],
            "payments": [],
        }
    )
