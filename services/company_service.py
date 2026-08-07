from models.company import Company
from observability.telemetry import traced
from repositories import company_repository
from utils.logger import get_logger

logger = get_logger(__name__)


@traced()
def get_company_information() -> Company:
    logger.info("Orchestrating Company lookup", extra={"entity": "Company"})
    return company_repository.get_company_information()
