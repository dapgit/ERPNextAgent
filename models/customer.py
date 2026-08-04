from dataclasses import dataclass


@dataclass
class Customer:
    name: str
    customer_group: str
    territory: str
    customer_type: str
