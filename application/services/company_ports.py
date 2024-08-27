from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class AutocompleteCompanyNamePort:
    @dataclass(frozen=True)
    class Key:
        country: str

    @dataclass(frozen=True)
    class Input:
        query: str

    @dataclass(frozen=True)
    class Output:
        data: Optional[list[AutocompleteCompanyNamePort.OutputItem]]
        status: AutocompleteCompanyNamePort.Status

    class Status(tuple, Enum):
        SUCCESS = (200, "OK")
        INVALID_REQUEST = (400, "INVALID REQUEST ERROR")
        SERVER_ERROR = (500, "INTERNAL SERVER ERROR")

    @dataclass(frozen=True)
    class OutputItem:
        company_name: str


class SearchCompanyByNamePort:
    @dataclass(frozen=True)
    class Key:
        country: str
        name: str

    @dataclass(frozen=True)
    class Input:
        pass

    @dataclass(frozen=True)
    class Output:
        data: Optional[SearchCompanyByNamePort.OutputItem]
        status: SearchCompanyByNamePort.Status

    class Status(tuple, Enum):
        SUCCESS = (200, "OK")
        INVALID_REQUEST = (400, "INVALID REQUEST ERROR")
        NOT_FOUND = (404, "NOT FOUND ERROR")
        SERVER_ERROR = (500, "INTERNAL SERVER ERROR")

    @dataclass(frozen=True)
    class OutputItem:
        company_name: str
        tags: list[str]


class SearchCompaniesByTagPort:
    @dataclass(frozen=True)
    class Key:
        country: str

    @dataclass(frozen=True)
    class Input:
        query: str

    @dataclass(frozen=True)
    class Output:
        data: Optional[list[str]]
        status: SearchCompaniesByTagPort.Status

    class Status(tuple, Enum):
        SUCCESS = (200, "OK")
        INVALID_REQUEST = (400, "INVALID REQUEST ERROR")
        SERVER_ERROR = (500, "INTERNAL SERVER ERROR")


class AddNewCompanyPort:
    @dataclass(frozen=True)
    class Key:
        country: str

    @dataclass(frozen=True)
    class Input:
        company_name: dict[str, str]
        tags: list[dict[str, str]]

    @dataclass(frozen=True)
    class Output:
        data: Optional[AddNewCompanyPort.OutputItem]
        status: AddNewCompanyPort.Status

    class Status(tuple, Enum):
        SUCCESS = (201, "CREATED")
        INVALID_REQUEST = (400, "INVALID REQUEST ERROR")
        SERVER_ERROR = (500, "INTERNAL SERVER ERROR")

    @dataclass(frozen=True)
    class OutputItem:
        company_name: str
        tags: list[str]


class AddCompanyTagPort:
    @dataclass(frozen=True)
    class Key:
        country: str
        name: str

    @dataclass(frozen=True)
    class Input:
        tags: list[dict[str, str]]

    @dataclass(frozen=True)
    class Output:
        data: Optional[AddCompanyTagPort.OutputItem]
        status: AddCompanyTagPort.Status

    class Status(tuple, Enum):
        SUCCESS = (200, "OK")
        INVALID_REQUEST = (400, "INVALID REQUEST ERROR")
        NOT_FOUND = (404, "NOT FOUND ERROR")
        SERVER_ERROR = (500, "INTERNAL SERVER ERROR")

    @dataclass(frozen=True)
    class OutputItem:
        company_name: str
        tags: list[str]


class DeleteCompanyTagPort:
    @dataclass(frozen=True)
    class Key:
        country: str
        name: str
        tag: str

    @dataclass(frozen=True)
    class Input:
        pass

    @dataclass(frozen=True)
    class Output:
        data: Optional[AddCompanyTagPort.OutputItem]
        status: AddCompanyTagPort.Status

    class Status(tuple, Enum):
        SUCCESS = (200, "OK")
        INVALID_REQUEST = (400, "INVALID REQUEST ERROR")
        NOT_FOUND = (404, "NOT FOUND ERROR")
        SERVER_ERROR = (500, "INTERNAL SERVER ERROR")

    @dataclass(frozen=True)
    class OutputItem:
        company_name: str
        tags: list[str]
