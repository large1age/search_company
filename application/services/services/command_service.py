from application.models.db.company_model import (
    CompanyBranchORM,
    CompanyORM,
    CompanyTagORM,
)
from application.models.db.connection import session
from application.repositories.db.company_repository import CompanyCommand, CompanyQuery
from application.services.units.company_unit import BranchUnit, CompanyUnit, TagUnit


class CompanyCommandService:
    def __init__(self):
        self.company_query = CompanyQuery(session=session)
        self.company_command = CompanyCommand(session=session)

    def register_company(
        self, branch_unit_list: list[BranchUnit], tag_unit_list: list[TagUnit]
    ) -> None:
        company_orm = CompanyORM()

        try:
            self.company_command.save_company(company_orm=company_orm)

            branch_orm_list = [
                CompanyBranchORM(
                    name=branch_unit.name,
                    country=branch_unit.country,
                )
                for branch_unit in branch_unit_list
            ]
            self.company_command.save_company_branches(
                company_orm=company_orm, company_branch_orm_list=branch_orm_list
            )

            tag_orm_list = [
                CompanyTagORM(
                    name=tag_unit.name,
                    country=tag_unit.country,
                )
                for tag_unit in tag_unit_list
            ]
            self.company_command.save_company_tags(
                company_orm=company_orm, company_tag_orm_list=tag_orm_list
            )

            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    def add_company_tag(
        self, company_unit: CompanyUnit, tag_unit_list: list[TagUnit]
    ) -> None:
        company_orm = (
            company_unit.orm
            if company_unit.orm
            else self.company_query.get_one_by_name(name=company_unit.name)
        )
        tag_orm_list = []
        for tag_unit in tag_unit_list:
            tag_orm_list.append(
                CompanyTagORM(
                    name=tag_unit.name,
                    country=tag_unit.country,
                )
            )

        try:
            self.company_command.save_company_tags(
                company_orm=company_orm, company_tag_orm_list=tag_orm_list
            )
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    def delete_company_tag(
        self, company_unit: CompanyUnit, tag_unit_list: list[TagUnit]
    ) -> None:
        company_orm = (
            company_unit.orm
            if company_unit.orm
            else self.company_query.get_one_by_name(name=company_unit.name)
        )
        exclude_tag_orm_list = []
        exclude_tag_info = [
            f"{tag_unit.name}|{tag_unit.country}" for tag_unit in tag_unit_list
        ]

        for tag_orm in company_orm.company_tag_orm_list:
            if f"{tag_orm.name}|{tag_orm.country}" in exclude_tag_info:
                exclude_tag_orm_list.append(tag_orm)

        try:
            self.company_command.delete_company_tags(
                company_orm=company_orm, company_tag_orm_list=exclude_tag_orm_list
            )
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
