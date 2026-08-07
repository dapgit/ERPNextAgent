from services import company_service
from utils.tool_execution import execute_tool


def get_company_information() -> str:
    """
    Return information about the company.

    Returns:
        str: A string containing the company information.
    """
    def _get_company_information() -> str:
        company = company_service.get_company_information()

        return f"""Company Name : {company.name}

Country : {company.country}

Currency : {company.currency}

Fiscal Year : {company.fiscal_year}

Industry : {company.industry}"""

    return execute_tool(_get_company_information)
