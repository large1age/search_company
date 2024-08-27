import json
from dataclasses import asdict

from flask import Flask, Response, request

from application.services.company_ports import (
    AutocompleteCompanyNamePort,
    SearchCompanyByNamePort,
    SearchCompaniesByTagPort,
    AddNewCompanyPort,
    AddCompanyTagPort, DeleteCompanyTagPort,
)
from application.services.company_usecases import CompanyUsecase

app = Flask(__name__)


@app.route("/search", methods=["GET"])
def get_api_for_autocomplete_company_name():
    try:
        key = AutocompleteCompanyNamePort.Key(
            country=request.headers.get("x-wanted-language", "ko")
        )
        input_port = AutocompleteCompanyNamePort.Input(
            query=request.args.get("query", "")
        )
    except (ValueError, TypeError):
        return Response(
            json.dumps(
                {
                    "message": AutocompleteCompanyNamePort.Status.INVALID_REQUEST[1],
                    "data": None,
                }
            ),
            status=AutocompleteCompanyNamePort.Status.INVALID_REQUEST[0],
            mimetype="application/json",
        )
    else:
        output = CompanyUsecase().autocomplete_company_name(
            key=key, input_port=input_port
        )
        return Response(
            json.dumps(
                {
                    "message": output.status.value[1],
                    "data": (
                        [asdict(data) for data in output.data] if output.data else []
                    ),
                }
            ),
            status=output.status.value[0],
            mimetype="application/json",
        )


@app.route("/companies/<string:name>", methods=["GET"])
def get_api_for_search_company_by_name(name: str):
    try:
        key = SearchCompanyByNamePort.Key(
            country=request.headers.get("x-wanted-language", "ko"), name=name
        )
        input_port = SearchCompanyByNamePort.Input()
    except (ValueError, TypeError):
        return Response(
            json.dumps(
                {
                    "message": SearchCompanyByNamePort.Status.INVALID_REQUEST[1],
                    "data": None,
                }
            ),
            status=SearchCompanyByNamePort.Status.INVALID_REQUEST[0],
            mimetype="application/json",
        )
    else:
        output = CompanyUsecase().search_company_by_name(key=key, input_port=input_port)
        return Response(
            json.dumps(
                {
                    "message": output.status.value[1],
                    "data": asdict(output.data) if output.data else None,
                }
            ),
            status=output.status.value[0],
            mimetype="application/json",
        )


@app.route("/tags", methods=["GET"])
def get_api_for_search_companies_by_tag():
    try:
        key = SearchCompaniesByTagPort.Key(
            country=request.headers.get("x-wanted-language", "ko")
        )
        input_port = SearchCompaniesByTagPort.Input(query=request.args.get("query", ""))
    except (ValueError, TypeError):
        return Response(
            json.dumps(
                {
                    "message": SearchCompaniesByTagPort.Status.INVALID_REQUEST[1],
                    "data": None,
                }
            ),
            status=SearchCompaniesByTagPort.Status.INVALID_REQUEST[0],
            mimetype="application/json",
        )
    else:
        output = CompanyUsecase().search_companies_by_tag(
            key=key, input_port=input_port
        )
        return Response(
            json.dumps(
                {
                    "message": output.status.value[1],
                    "data": output.data,
                }
            ),
            status=output.status.value[0],
            mimetype="application/json",
        )


@app.route("/companies", methods=["POST"])
def post_api_for_add_new_company():
    try:
        key = AddNewCompanyPort.Key(
            country=request.headers.get("x-wanted-language", "ko")
        )
        input_port = AddNewCompanyPort.Input(**request.json)
    except (ValueError, TypeError):
        return Response(
            json.dumps(
                {
                    "message": AddNewCompanyPort.Status.INVALID_REQUEST[1],
                    "data": None,
                }
            ),
            status=AddNewCompanyPort.Status.INVALID_REQUEST[0],
            mimetype="application/json",
        )
    else:
        output = CompanyUsecase().add_new_company(key=key, input_port=input_port)
        return Response(
            json.dumps(
                {
                    "message": output.status.value[1],
                    "data": asdict(output.data) if output.data else None,
                }
            ),
            status=output.status.value[0],
            mimetype="application/json",
        )


@app.route("/companies/<string:name>/tags", methods=["PUT"])
def put_api_for_add_company_tag(name: str):
    try:
        key = AddCompanyTagPort.Key(
            country=request.headers.get("x-wanted-language", "ko"), name=name
        )
        input_port = AddCompanyTagPort.Input(tags=request.json)
    except (ValueError, TypeError):
        return Response(
            json.dumps(
                {
                    "message": AddCompanyTagPort.Status.INVALID_REQUEST[1],
                    "data": None,
                }
            ),
            status=AddCompanyTagPort.Status.INVALID_REQUEST[0],
            mimetype="application/json",
        )
    else:
        output = CompanyUsecase().add_company_tag(key=key, input_port=input_port)
        return Response(
            json.dumps(
                {
                    "message": output.status.value[1],
                    "data": asdict(output.data) if output.data else None,
                }
            ),
            status=output.status.value[0],
            mimetype="application/json",
        )

@app.route("/companies/<string:name>/tags/<string:tag>", methods=["DELETE"])
def delete_api_for_delete_company_tag(name: str, tag: str):
    try:
        key = DeleteCompanyTagPort.Key(
            country=request.headers.get("x-wanted-language", "ko"),
            name=name,
            tag=tag
        )
        input_port = DeleteCompanyTagPort.Input()
    except (ValueError, TypeError):
        return Response(
            json.dumps(
                {
                    "message": DeleteCompanyTagPort.Status.INVALID_REQUEST[1],
                    "data": None,
                }
            ),
            status=DeleteCompanyTagPort.Status.INVALID_REQUEST[0],
            mimetype="application/json",
        )
    else:
        output = CompanyUsecase().delete_company_tag(key=key, input_port=input_port)
        return Response(
            json.dumps(
                {
                    "message": output.status.value[1],
                    "data": asdict(output.data) if output.data else None,
                }
            ),
            status=output.status.value[0],
            mimetype="application/json",
        )

