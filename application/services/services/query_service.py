from typing import Optional

from application.models.db.connection import session
from application.repositories.db.company_repository import CompanyQuery

from ..units.company_unit import CompanyUnit


class CompanyQueryService:

    def __init__(self):
        self.company_query = CompanyQuery(session=session)

    def find_company_by_name(self, name: str, country: str) -> Optional[CompanyUnit]:
        company_orm = self.company_query.find_one_by_branch_info(name)
        if not company_orm:
            return None
        company_unit = CompanyUnit.convert_from_orm(
            company_orm=company_orm, country=country
        )
        return company_unit

    def search_companies_by_name(self, name: str, country: str) -> list[CompanyUnit]:
        company_orm_list = self.company_query.search_list_by_branch_info(name=name)
        company_unit_list = []
        for company_orm in company_orm_list:
            company_unit_list.append(
                CompanyUnit.convert_from_orm(company_orm=company_orm, country=country)
            )
        return company_unit_list

    def find_companies_by_tag(self, tag: str, country: str) -> list[CompanyUnit]:
        company_orm_list = self.company_query.find_list_by_tag_info(name=tag)
        company_unit_list = []
        for company_orm in company_orm_list:
            company_unit_list.append(
                CompanyUnit.convert_from_orm(company_orm=company_orm, country=country)
            )
        return company_unit_list
