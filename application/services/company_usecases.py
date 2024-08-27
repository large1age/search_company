from application.services.company_ports import (
    AddCompanyTagPort,
    AutocompleteCompanyNamePort,
    DeleteCompanyTagPort,
    SearchCompanyByNamePort,
    SearchCompaniesByTagPort,
    AddNewCompanyPort,
)
from application.services.services.command_service import CompanyCommandService
from application.services.services.query_service import CompanyQueryService
from application.services.units.company_unit import BranchUnit, TagUnit


class CompanyUsecase:
    def __init__(self):
        self.query_service = CompanyQueryService()
        self.command_service = CompanyCommandService()

    def autocomplete_company_name(
        self,
        key: AutocompleteCompanyNamePort.Key,
        input_port: AutocompleteCompanyNamePort.Input,
    ) -> AutocompleteCompanyNamePort.Output:
        if len(input_port.query) < 2:
            return AutocompleteCompanyNamePort.Output(
                status=AutocompleteCompanyNamePort.Status.INVALID_REQUEST,
                data=None,
            )

        try:
            company_units = self.query_service.search_companies_by_name(
                country=key.country, name=input_port.query
            )
            output_items = [
                AutocompleteCompanyNamePort.OutputItem(company_name=company_unit.name)
                for company_unit in company_units
            ]
            return AutocompleteCompanyNamePort.Output(
                status=AutocompleteCompanyNamePort.Status.SUCCESS,
                data=output_items,
            )

        except Exception as e:
            return AutocompleteCompanyNamePort.Output(
                status=AutocompleteCompanyNamePort.Status.SERVER_ERROR,
                data=None,
            )

    def search_company_by_name(
        self,
        key: SearchCompanyByNamePort.Key,
        input_port: SearchCompanyByNamePort.Input,
    ) -> SearchCompanyByNamePort.Output:
        try:
            company_unit = self.query_service.find_company_by_name(
                country=key.country, name=key.name
            )
            if not company_unit:
                return SearchCompanyByNamePort.Output(
                    status=SearchCompanyByNamePort.Status.NOT_FOUND,
                    data=None,
                )

            output_item = SearchCompanyByNamePort.OutputItem(
                company_name=company_unit.name,
                tags=[tag_unit.name for tag_unit in company_unit.tag_units_by_country],
            )
            return SearchCompanyByNamePort.Output(
                status=SearchCompanyByNamePort.Status.SUCCESS, data=output_item
            )
        except Exception as e:
            return SearchCompanyByNamePort.Output(
                status=SearchCompanyByNamePort.Status.SERVER_ERROR,
                data=None,
            )

    def search_companies_by_tag(
        self,
        key: SearchCompaniesByTagPort.Key,
        input_port: SearchCompaniesByTagPort.Input,
    ) -> SearchCompaniesByTagPort.Output:
        try:
            company_units = self.query_service.find_companies_by_tag(
                country=key.country, tag=input_port.query
            )
            data = [company_unit.name for company_unit in company_units]
            return SearchCompaniesByTagPort.Output(
                status=SearchCompaniesByTagPort.Status.SUCCESS,
                data=data,
            )
        except Exception as e:
            return SearchCompaniesByTagPort.Output(
                status=SearchCompaniesByTagPort.Status.SERVER_ERROR,
                data=None,
            )

    def add_new_company(
        self,
        key: AddNewCompanyPort.Key,
        input_port: AddNewCompanyPort.Input,
    ) -> AddNewCompanyPort.Output:
        try:
            branch_unit_list = [
                BranchUnit(country=country, name=name)
                for country, name in input_port.company_name.items()
            ]
            tag_unit_list = []
            for tag_dict in input_port.tags:
                tag_unit_list += [
                    TagUnit(country=country, name=name)
                    for country, name in tag_dict["tag_name"].items()
                ]

            self.command_service.register_company(
                branch_unit_list=branch_unit_list, tag_unit_list=tag_unit_list
            )

            company_name = ""
            tags = []

            for branch_unit in branch_unit_list:
                if branch_unit.country == key.country:
                    company_name = branch_unit.name
                    break
            for tag_unit in tag_unit_list:
                if tag_unit.country == key.country:
                    tags.append(tag_unit.name)

            return AddNewCompanyPort.Output(
                status=AddNewCompanyPort.Status.SUCCESS,
                data=AddNewCompanyPort.OutputItem(company_name=company_name, tags=tags),
            )
        except Exception as e:
            return AddNewCompanyPort.Output(
                status=AddNewCompanyPort.Status.SERVER_ERROR,
                data=None,
            )

    def add_company_tag(
        self,
        key: AddCompanyTagPort.Key,
        input_port: AddCompanyTagPort.Input,
    ) -> AddCompanyTagPort.Output:
        try:
            company_unit = self.query_service.find_company_by_name(
                country=key.country, name=key.name
            )
            if not company_unit:
                return AddCompanyTagPort.Output(
                    status=AddCompanyTagPort.Status.NOT_FOUND,
                    data=None,
                )

            tag_unit_list = []
            for tag_dict in input_port.tags:
                tag_unit_list += [
                    TagUnit(country=country, name=name)
                    for country, name in tag_dict["tag_name"].items()
                ]

            self.command_service.add_company_tag(
                company_unit=company_unit, tag_unit_list=tag_unit_list
            )

            tags = [
                tag_unit.name
                for tag_unit in tag_unit_list
                if tag_unit.country == key.country
            ] + [tag_unit.name for tag_unit in company_unit.tag_units_by_country]
            sorted_tags = sorted(tags, key=lambda x: int(x.split("_")[1]))

            return AddCompanyTagPort.Output(
                status=AddCompanyTagPort.Status.SUCCESS,
                data=AddCompanyTagPort.OutputItem(
                    company_name=company_unit.name, tags=sorted_tags
                ),
            )
        except Exception as e:
            return AddCompanyTagPort.Output(
                status=AddCompanyTagPort.Status.SERVER_ERROR,
                data=None,
            )

    def delete_company_tag(
        self,
        key: DeleteCompanyTagPort.Key,
        input_port: DeleteCompanyTagPort.Input,
    ) -> DeleteCompanyTagPort.Output:
        try:
            company_unit = self.query_service.find_company_by_name(
                country=key.country, name=key.name
            )
            if not company_unit:
                return AddCompanyTagPort.Output(
                    status=AddCompanyTagPort.Status.NOT_FOUND,
                    data=None,
                )

            tag_unit_list = [
                tag_unit
                for tag_unit in company_unit.tag_units
                if tag_unit.name == key.tag
            ]
            self.command_service.delete_company_tag(
                company_unit=company_unit, tag_unit_list=tag_unit_list
            )

            tags = [
                tag_unit.name
                for tag_unit in company_unit.tag_units
                if tag_unit.name != key.tag and tag_unit.country == key.country
            ]
            sorted_tags = sorted(tags, key=lambda x: int(x.split("_")[1]))

            return DeleteCompanyTagPort.Output(
                status=DeleteCompanyTagPort.Status.SUCCESS,
                data=DeleteCompanyTagPort.OutputItem(
                    company_name=company_unit.name, tags=sorted_tags
                ),
            )
        except Exception as e:
            return DeleteCompanyTagPort.Output(
                status=DeleteCompanyTagPort.Status.SERVER_ERROR,
                data=None,
            )
