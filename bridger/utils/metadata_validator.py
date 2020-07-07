import json
import os

from jsonschema import Draft7Validator, validate

from bridger.buttons import Button

BASE_PATH = os.path.dirname(__file__)

schema = {
    "type": "object",
    "properties": {
        "identifier": {"type": "string"},
        "type": {"type": "string", "enum": ["list", "instance", "chart"]},
        "endpoints": {
            "type": "object",
            "properties": {
                "list": {"type": "string", "format": "uri", "pattern": "^((https)?|(http)?|(wss)?|(ws)?|(ftp))://",},
                "instance": {"type": "string", "format": "uri", "pattern": "^((https)?|(http)?|(wss)?|(ws)?|(ftp))://",},
                "create": {"type": "string", "format": "uri", "pattern": "^((https)?|(http)?|(wss)?|(ws)?|(ftp))://",},
                "delete": {"type": "string", "format": "uri", "pattern": "^((https)?|(http)?|(wss)?|(ws)?|(ftp))://",},
            },
            "anyOf": [{"required": ["list"]}, {"required": ["instance"]}],
        },
        "buttons": {"type": "array", "items": {"type": "string", "enum": Button.buttons()},},
        "create_buttons": {"type": "array", "items": {"type": "string", "enum": Button.create_buttons()},},
        "custom_instance_buttons": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "type": {"type": "string", "enum": Button.custom_buttons()},
                    "label": {"type": "string"},
                    "icon": {"type": "string"},
                    "title": {"type": "string"},
                },
                "anyOf": [{"required": ["label"]}, {"required": ["instance"]}],
                "required": ["key", "type"],
            },
        }
        # "custom_buttons": {
        #     "type": "array",
        #     "items": {
        #         "type": "object",
        #         "properties": {
        #             "type": {
        #                 "type": "string",
        #                 "enum": ["hyperlink", "widget", "dropdown", "action"],
        #             },
        #             "key": {"type": "string"},
        #             "label": {"type": "string"},
        #             "icon": {"type": "string"},
        #             "title": {"type": "string"},
        #         },
        #         "anyOf": [
        #             {"required": ["type", "key", "label"]},
        #             {"required": ["type", "key", "icon"]},
        #         ],
        #     },
        # },
    },
    "required": ["identifier", "type"],
}

with open(os.path.join(BASE_PATH, "options1.json")) as json_file:
    options1 = json.load(json_file)
    validator = Draft7Validator(schema)
    for error in sorted(validator.iter_errors(options1), key=lambda e: e.path):
        print(error)
