from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKeyConstraint, String, TypeDecorator
from sqlalchemy.dialects.mysql import INTEGER as MySQLInteger
from sqlalchemy.orm import relationship

from application.models.db.connection import Base


class UnsignedInteger(TypeDecorator):
    impl = MySQLInteger
    cache_ok = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.impl = MySQLInteger(unsigned=True)


# 테이블 정의
class CompanyORM(Base):
    __tablename__ = "companies"

    id = Column(UnsignedInteger, primary_key=True)
    external_key = Column(String, unique=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    company_branch_orm_list = relationship(
        "CompanyBranchORM",
        back_populates="company_orm",
        cascade="all, delete-orphan",
        lazy="select",
    )
    company_tag_orm_list = relationship(
        "CompanyTagORM",
        back_populates="company_orm",
        cascade="all, delete-orphan",
        lazy="select",
    )


class CompanyBranchORM(Base):
    __tablename__ = "company_branches"

    id = Column(UnsignedInteger, primary_key=True)
    company_id = Column(UnsignedInteger, nullable=False)
    name = Column(
        String
    )  # FULL TEXT INDEX 조건 가정 (SQLite3는 별도 테이블 에서 FULL TEXT INDEX 걸수 있음)
    country = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    company_orm = relationship(
        "CompanyORM", back_populates="company_branch_orm_list", lazy="select"
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ["company_id"],
            ["companies.id"],
            name="FK_COMPANY_ID",
            use_alter=True,
            deferrable=True,
            initially="DEFERRED",
        ),
    )


class CompanyTagORM(Base):
    __tablename__ = "company_tags"

    id = Column(UnsignedInteger, primary_key=True)
    company_id = Column(UnsignedInteger, nullable=False)
    name = Column(String)
    country = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    company_orm = relationship(
        "CompanyORM", back_populates="company_tag_orm_list", lazy="select"
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ["company_id"],
            ["companies.id"],
            name="FK_COMPANY_ID",
            use_alter=True,
            deferrable=True,
            initially="DEFERRED",
        ),
    )
