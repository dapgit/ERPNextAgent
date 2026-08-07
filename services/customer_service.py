from typing import Optional

from models.customer import Customer
from observability.telemetry import traced
from repositories import customer_repository
from utils.logger import get_logger

logger = get_logger(__name__)


@traced()
def get_customer(customer_name: str) -> Optional[Customer]:
    if not customer_name or not customer_name.strip():
        raise ValueError("customer_name must not be empty")

    logger.info("Orchestrating Customer lookup", extra={"entity": "Customer"})
    return customer_repository.get_customer(customer_name)
