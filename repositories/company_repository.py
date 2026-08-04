from models.company import Company

_COMPANY = Company(
    name="ABC Traders Pvt Ltd",
    country="India",
    currency="INR",
    fiscal_year="2026-2027",
    industry="Distribution",
)


def get_company_information() -> Company:
    return _COMPANY
