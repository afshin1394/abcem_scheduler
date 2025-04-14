from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def custom_openapi(app: FastAPI):
    # If the schema is already generated, just return it
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="ABCEM",
        version="1.0.0",
        description="ABCEM API",
        routes=app.routes,
    )

    # ----------------------------------------------------------------------
    # 1. Remove default validation error schemas if desired
    # ----------------------------------------------------------------------
    if "components" in openapi_schema:
        if "schemas" in openapi_schema["components"]:
            openapi_schema["components"]["schemas"].pop("HTTPValidationError", None)
            openapi_schema["components"]["schemas"].pop("ValidationError", None)

    # ----------------------------------------------------------------------
    # 2. Define your custom ErrorResponse schema
    # ----------------------------------------------------------------------
    custom_error_schema = {
        "type": "object",
        "properties": {
            "message": {"type": "string"},
            "code": {"type": "integer"},
            "errors": {
                "type": "array",
                "items": {"type": "string"}
            },
        },
        "required": ["message", "code", "errors"]
    }
    openapi_schema["components"]["schemas"]["MyCustomError"] = custom_error_schema

    # ----------------------------------------------------------------------
    # 3. Override the 422 response to reference MyCustomError
    # ----------------------------------------------------------------------
    for path, path_item in openapi_schema.get("paths", {}).items():
        for method, method_item in path_item.items():
            if "responses" in method_item:
                if "422" in method_item["responses"]:
                    method_item["responses"]["422"] = {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/MyCustomError"
                                },
                                "example": {
                                    "message": "Validation error",
                                    "code": 422,
                                    "errors": ["Missing field: name"]
                                }
                            }
                        },
                    }

    # ----------------------------------------------------------------------
    # 4. Define a base success response schema (BaseSuccessResponse) with latency
    # ----------------------------------------------------------------------
    custom_success_schema = {
        "type": "object",
        "properties": {
            "status_code": {"type": "integer"},
            "latency": {"type": "number", "format": "float", "description": "Response time in seconds"},
            "result": {}
        },
        "required": ["status_code", "latency", "result"]
    }
    openapi_schema["components"]["schemas"]["BaseSuccessResponse"] = custom_success_schema

    # ----------------------------------------------------------------------
    # 5. Override all 200 responses to reference BaseSuccessResponse
    # ----------------------------------------------------------------------
    for path, path_item in openapi_schema.get("paths", {}).items():
        for method, method_item in path_item.items():
            if "responses" in method_item:
                if "200" in method_item["responses"]:
                    method_item["responses"]["200"] = {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/BaseSuccessResponse"
                                },
                                "example": {
                                    "status_code": 200,
                                    "latency": 0.123,  # Example latency value
                                    "result": {}
                                }
                            }
                        },
                    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema
