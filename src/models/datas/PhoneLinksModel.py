from dataclasses import dataclass
from typing import List


@dataclass
class PhoneLinksModel:
    """PhoneLinksModel"""
    phone: str
    links: List[str]
