from models.company import Company
from repositories import company_repository


def get_company_information() -> Company:
    return company_repository.get_company_information()
