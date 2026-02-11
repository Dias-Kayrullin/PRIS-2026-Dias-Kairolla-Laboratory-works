# src/models.py
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Store:
    """Магазин / торговая точка"""
    name: str
    common_categories: List[str] = None  # категории, которые чаще всего ассоциируются
    typical_items: List[str] = None      # типичные товары

    def __post_init__(self):
        if self.common_categories is None:
            self.common_categories = []
        if self.typical_items is None:
            self.typical_items = []

    def __str__(self):
        return f"{self.name} (категории: {', '.join(self.common_categories)})"


@dataclass
class Category:
    """Категория расходов"""
    name: str
    typical_stores: List[str] = None
    typical_items: List[str] = None

    def __post_init__(self):
        if self.typical_stores is None:
            self.typical_stores = []
        if self.typical_items is None:
            self.typical_items = []

    def __str__(self):
        return self.name


@dataclass
class Item:
    """Товар / позиция в чеке"""
    name: str
    default_category: Optional[str] = None

    def __str__(self):
        cat = f" → {self.default_category}" if self.default_category else ""
        return f"{self.name}{cat}"
