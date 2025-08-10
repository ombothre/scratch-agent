from pydantic import BaseModel
from typing import List, get_args, get_origin, Union
import json

# Helper: snake_case → camelCase
def to_camel(s: str) -> str:
    parts = s.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

# Helper: type → TYPE
def to_upper_type(t: str | None) -> str:
    if not t:
        return "UNKNOWN"
    return t.upper()


# Recursive transformer from pydantic-style JSON schema to Gemini-style
def transform_schema(schema: dict) -> dict:
    t = schema.get("type")

    if t == "object":
        props = schema.get("properties", {})
        new_props = {}
        ordering = []

        for key, val in props.items():
            camel = to_camel(key)
            new_props[camel] = transform_schema(val)
            ordering.append(camel)

        return {
            "type": "OBJECT",
            "properties": new_props,
            "propertyOrdering": ordering
        }

    elif t == "array":
        return {
            "type": "ARRAY",
            "items": transform_schema(schema["items"])
        }

    else:
        return {
            "type": to_upper_type(t)
        }

# Entrypoint to generate Gemini-style schema from model or list[model]
def generate_response_schema(model_or_list: type) -> dict:
    origin = get_origin(model_or_list)

    # list[BaseModel]
    if origin is list or origin is List:
        model = get_args(model_or_list)[0]
        if not issubclass(model, BaseModel):
            raise TypeError("List element is not a Pydantic model")
        base_schema = model.model_json_schema()
        transformed = transform_schema(base_schema)
        return {
            "responseSchema": {
                "type": "ARRAY",
                "items": transformed
            }
        }

    # single BaseModel
    elif isinstance(model_or_list, type) and issubclass(model_or_list, BaseModel):
        base_schema = model_or_list.model_json_schema()
        transformed = transform_schema(base_schema)
        return {
            "responseSchema": transformed
        }

    else:
        raise TypeError("Input must be a Pydantic model or list of models")

def get_response_schema(schema: type) -> str:
    response_schema = generate_response_schema(schema)
    return json.dumps(response_schema, indent=4)
