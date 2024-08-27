from typing import Optional

from sqlalchemy import asc

from application.models.db.company_model import (
    CompanyBranchORM,
    CompanyORM,
    CompanyTagORM,
)


class CompanyQuery:
    def __init__(self, session):
        self.session = session
        self.base_orm_type = CompanyORM

    def get_one_by_name(self, name: str) -> CompanyORM:
        query = self.session.query(self.base_orm_type).filter(
            CompanyBranchORM.name == name
        )
        return query.one()

    def find_one_by_branch_info(self, name: str) -> Optional[CompanyORM]:
        query = (
            self.session.query(self.base_orm_type)
            .join(
                CompanyBranchORM, self.base_orm_type.id == CompanyBranchORM.company_id
            )
            .filter(CompanyBranchORM.name == name)
            .distinct()
        )
        return query.first()

    def search_list_by_branch_info(self, name: str) -> list[CompanyORM]:
        query = (
            self.session.query(self.base_orm_type)
            .join(
                CompanyBranchORM, self.base_orm_type.id == CompanyBranchORM.company_id
            )
            .filter(
                CompanyBranchORM.name.like(f"%{name}%")
            )  # SQLite3에서는 동일 테이블의 FTS 연산 지원이 되지 않아서 부득이하게 like 연산을 함 (풀스캔 이슈 인지)
            .order_by(asc(self.base_orm_type.id))
            .distinct()
        )
        return query.all()

    def find_list_by_tag_info(self, name: str) -> list[CompanyORM]:
        query = (
            self.session.query(self.base_orm_type)
            .join(CompanyTagORM, self.base_orm_type.id == CompanyTagORM.company_id)
            .filter(CompanyTagORM.name == name)
            .order_by(asc(self.base_orm_type.id))
            .distinct()
        )
        return query.all()


class CompanyCommand:
    def __init__(self, session):
        self.session = session

    def save_company(self, company_orm: CompanyORM) -> None:
        self.session.add(company_orm)
        self.session.flush()

    def save_company_branches(
        self, company_orm: CompanyORM, company_branch_orm_list: list[CompanyBranchORM]
    ) -> None:
        for company_branch_orm in company_branch_orm_list:
            company_orm.company_branch_orm_list.append(company_branch_orm)
        self.session.add(company_orm)
        self.session.flush()

    def save_company_tags(
        self, company_orm: CompanyORM, company_tag_orm_list: list[CompanyTagORM]
    ):
        for company_tag_orm in company_tag_orm_list:
            company_orm.company_tag_orm_list.append(company_tag_orm)
        self.session.add(company_orm)
        self.session.flush()

    def delete_company_tags(
        self, company_orm: CompanyORM, company_tag_orm_list: list[CompanyTagORM]
    ):
        for company_tag_orm in company_tag_orm_list:
            company_orm.company_tag_orm_list.remove(company_tag_orm)
        self.session.add(company_orm)
        self.session.flush()
