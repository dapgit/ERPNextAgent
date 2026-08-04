from typing import Optional

from models.customer import Customer
from repositories import customer_repository


def get_customer(customer_name: str) -> Optional[Customer]:
    if not customer_name or not customer_name.strip():
        raise ValueError("customer_name must not be empty")

    return customer_repository.get_customer(customer_name)
