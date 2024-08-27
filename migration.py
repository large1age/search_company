import csv

from application.models.db.company_model import (
    CompanyBranchORM,
    CompanyORM,
    CompanyTagORM,
)
from application.models.db.connection import Base, engine, session

Base.metadata.create_all(engine)

csv_file_path = "company_tag_sample.csv"

with open(csv_file_path, mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    headers = next(reader)

    for row in reader:
        company_orm = CompanyORM()
        session.add(company_orm)
        session.flush()

        for header, value in zip(headers, row):
            if header == "company_ko" and value:
                company_orm.company_branch_orm_list.append(
                    CompanyBranchORM(name=value, country="ko")
                )
            elif header == "company_en" and value:
                company_orm.company_branch_orm_list.append(
                    CompanyBranchORM(name=value, country="en")
                )
            elif header == "company_ja" and value:
                company_orm.company_branch_orm_list.append(
                    CompanyBranchORM(name=value, country="ja")
                )
            elif header == "tag_ko" and value:
                for tag in value.split("|"):
                    company_orm.company_tag_orm_list.append(
                        CompanyTagORM(name=tag, country="ko")
                    )
            elif header == "tag_en" and value:
                for tag in value.split("|"):
                    company_orm.company_tag_orm_list.append(
                        CompanyTagORM(name=tag, country="en")
                    )
            elif header == "tag_ja" and value:
                for tag in value.split("|"):
                    company_orm.company_tag_orm_list.append(
                        CompanyTagORM(name=tag, country="ja")
                    )

        session.add(company_orm)
        session.flush()
        session.commit()
