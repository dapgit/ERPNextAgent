from dataclasses import dataclass


@dataclass
class Company:
    name: str
    country: str
    currency: str
    fiscal_year: str
    industry: str
