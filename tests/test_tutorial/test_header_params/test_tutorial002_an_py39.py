import pytest
from fastapi.testclient import TestClient

from ...utils import needs_py39


@pytest.fixture(name="client")
def get_client():
    from docs_src.header_params.tutorial002_an_py39 import app

    client = TestClient(app)
    return client


@needs_py39
@pytest.mark.parametrize(
    "path,headers,expected_status,expected_response",
    [
        ("/items", None, 200, {"strange_header": None}),
        ("/items", {"X-Header": "notvalid"}, 200, {"strange_header": None}),
        (
            "/items",
            {"strange_header": "FastAPI test"},
            200,
            {"strange_header": "FastAPI test"},
        ),
        (
            "/items",
            {"strange-header": "Not really underscore"},
            200,
            {"strange_header": None},
        ),
    ],
)
def test(path, headers, expected_status, expected_response, client: TestClient):
    response = client.get(path, headers=headers)
    assert response.status_code == expected_status
    assert response.json() == expected_response


@needs_py39
def test_openapi_schema():
    from docs_src.header_params.tutorial002_an_py39 import app

    client = TestClient(app)
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        },
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                    },
                    "summary": "Read Items",
                    "operationId": "read_items_items__get",
                    "parameters": [
                        {
                            "required": False,
                            "schema": {"title": "Strange Header", "type": "string"},
                            "name": "strange_header",
                            "in": "header",
                        }
                    ],
                }
            }
        },
        "components": {
            "schemas": {
                "ValidationError": {
                    "title": "ValidationError",
                    "required": ["loc", "msg", "type"],
                    "type": "object",
                    "properties": {
                        "loc": {
                            "title": "Location",
                            "type": "array",
                            "items": {
                                "anyOf": [{"type": "string"}, {"type": "integer"}]
                            },
                        },
                        "msg": {"title": "Message", "type": "string"},
                        "type": {"title": "Error Type", "type": "string"},
                    },
                },
                "HTTPValidationError": {
                    "title": "HTTPValidationError",
                    "type": "object",
                    "properties": {
                        "detail": {
                            "title": "Detail",
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/ValidationError"},
                        }
                    },
                },
            }
        },
    }
