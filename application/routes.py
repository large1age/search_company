import json
from dataclasses import asdict

from flask import Flask, Response, request

from application.services.short_link_port import (
    ShortLinkGenerateInput,
    ShortLinkGenerateKey,
    ShortLinkRetrieveInput,
    ShortLinkRetrieveKey,
)
from application.services.short_link_usecase import ShortLinkUsecase

app = Flask(__name__)


@app.route("/short-links/<string:short_id>", methods=["GET"])
def get(short_id: str):
    try:
        key = ShortLinkRetrieveKey(shortId=short_id)
        input_port = ShortLinkRetrieveInput()
    except (ValueError, TypeError):
        return Response(
            json.dumps({"error": "client error"}),
            status=400,
            mimetype="application/json",
        )
    else:
        output_status, output = ShortLinkUsecase().retrieve(
            key=key, input_port=input_port
        )
        if output_status.SUCCESS and output:
            status = 302
            data = {"data": asdict(output)}
        elif output_status.VALIDATION_ERROR:
            status = 400
            data = {"error": "client error"}
        elif output_status.NOT_FOUND_ERROR:
            status = 404
            data = {"error": "client error"}
        elif output_status.RUNTIME_ERROR:
            status = 500
            data = {"error": "server error"}
        else:
            status = 500
            data = {"error": "server error"}

        return Response(
            json.dumps(data),
            status=status,
            mimetype="application/json",
        )


@app.route("/short-links", methods=["POST"])
def post():
    try:
        body_param = request.json
        key = ShortLinkGenerateKey()
        input_port = ShortLinkGenerateInput(url=body_param.get("url"))
    except (ValueError, TypeError):
        return Response(
            json.dumps({"error": "client error"}),
            status=400,
            mimetype="application/json",
        )
    else:
        output_status, output = ShortLinkUsecase().generate(
            key=key, input_port=input_port
        )
        if output_status.SUCCESS and output:
            status = 201
            data = {"data": asdict(output)}
        elif output_status.VALIDATION_ERROR:
            status = 400
            data = {"error": "client error"}
        elif output_status.CONFLICT_ERROR:
            status = 409
            data = {"error": "client error"}
        elif output_status.RUNTIME_ERROR:
            status = 500
            data = {"error": "server error"}
        else:
            status = 500
            data = {"error": "server error"}

        return Response(
            json.dumps(data),
            status=status,
            mimetype="application/json",
        )
