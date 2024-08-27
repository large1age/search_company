from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from application.models.db.company_model import CompanyORM


@dataclass(frozen=True)
class BranchUnit:
    name: str
    country: str


@dataclass(frozen=True)
class TagUnit:
    name: str
    country: str


@dataclass(frozen=True)
class CompanyUnit:
    external_key: str
    name: str
    country: str
    branch_units: list[BranchUnit]
    tag_units: list[TagUnit]
    tag_units_by_country: list[TagUnit]

    _orm: Optional[CompanyORM] = field(default=None)

    @classmethod
    def convert_from_orm(cls, company_orm: CompanyORM, country: str) -> CompanyUnit:
        company_name = ""
        company_country = ""
        branch_units = []
        for branch_orm in company_orm.company_branch_orm_list:
            branch_units.append(
                BranchUnit(name=branch_orm.name, country=branch_orm.country)
            )
            if branch_orm.country == country:
                company_name = branch_orm.name
                company_country = branch_orm.country

        tag_units = []
        tag_units_by_country = []
        for tag_orm in company_orm.company_tag_orm_list:
            tag_unit = TagUnit(name=tag_orm.name, country=tag_orm.country)
            if tag_orm.country == country:
                tag_units_by_country.append(tag_unit)
            tag_units.append(tag_unit)

        return CompanyUnit(
            _orm=company_orm,
            external_key=company_orm.external_key,
            name=company_name,
            country=company_country,
            branch_units=branch_units,
            tag_units=tag_units,
            tag_units_by_country=tag_units_by_country,
        )

    @property
    def orm(self) -> Optional[CompanyORM]:
        return self._orm
