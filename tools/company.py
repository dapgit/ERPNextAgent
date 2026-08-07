from observability.telemetry import get_tracer
from services import company_service
from utils.logger import get_logger
from utils.tool_execution import execute_tool

logger = get_logger(__name__)
tracer = get_tracer(__name__)


def get_company_information() -> str:
    """
    Return information about the company.

    Returns:
        str: A string containing the company information.
    """
    logger.info("Handling get_company_information request", extra={"entity": "Company"})

    def _get_company_information() -> str:
        with tracer.start_as_current_span("tools.company.get_company_information"):
            company = company_service.get_company_information()

            return f"""Company Name : {company.name}

Country : {company.country}

Currency : {company.currency}

Fiscal Year : {company.fiscal_year}

Industry : {company.industry}"""

    result = execute_tool(_get_company_information)
    logger.info("Completed get_company_information request", extra={"entity": "Company"})
    return result
