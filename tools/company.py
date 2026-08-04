from services import company_service


def get_company_information() -> str:
    """
    Return information about the company.

    Returns:
        str: A string containing the company information.
    """
    company = company_service.get_company_information()

    return f"""Company Name : {company.name}

Country : {company.country}

Currency : {company.currency}

Fiscal Year : {company.fiscal_year}

Industry : {company.industry}"""
