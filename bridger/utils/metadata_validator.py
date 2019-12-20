import json
from jsonschema import validate

schema = {
    "type": "object",
    "properties": {
        "identifier": {"type": "string"},
        "type": {"type": "string", "enum": ["list", "instance", "chart"]},
        "endpoints": {
            "type": "object",
            "properties": {
                "list": {
                    "type": "string",
                    "format": "uri",
                    "pattern": "^(https?|http?|wss?|ws?|ftp)://",
                },
                "instance": {
                    "type": "string",
                    "format": "uri",
                    "pattern": "^(https?|http?|wss?|ws?|ftp)://",
                },
                "new": {
                    "type": "string",
                    "format": "uri",
                    "pattern": "^(https?|http?|wss?|ws?|ftp)://",
                },
                "delete": {
                    "type": "string",
                    "format": "uri",
                    "pattern": "^(https?|http?|wss?|ws?|ftp)://",
                },
            },
            "anyOf": [{"required": ["list"]}, {"required": ["instance"]},],
        },
        "buttons": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": [
                    "save",
                    "saveandnew",
                    "saveandclose",
                    "refresh",
                    "new",
                    "delete",
                ],
            },
        },
        "custom_buttons": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": ["hyperlink", "widget", "dropdown", "action"],
                    },
                    "key": {"type": "string"},
                    "label": {"type": "string"},
                    "icon": {"type": "string"},
                    "title": {"type": "string"},
                },
                "anyOf": [
                    {"required": ["type", "key", "label"]},
                    {"required": ["type", "key", "icon"]},
                ],
            },
        },
    },
    "required": ["identifier", "type"],
}

example_dict = {
    "identifier": "portfolio:strategy",
    "messages": [],
    "type": "list",
    "endpoints": {
        "list": "http://localhost:5000/api/portfolio/strategy/",
        "instance": "http://localhost:5000/api/portfolio/strategy/",
    },
    "buttons": ["save", "refresh"],
    "custom_buttons": [{"type": "widget", "key": "some_key", "label": "Some Label"}],
    "instance_display": [
        {"fields": ["title", ["isin", "ticker"], ["currency", "is_cash"]]}
    ],
    "list_display": [
        {"key": "title", "label": "Title"},
        {"key": "ticker", "label": "Ticker"},
        {"key": "currency", "label": "Currency"},
        {"key": "is_cash", "label": "Cash"},
    ],
    "list_formatting": None,
    "cell_formatting": None,
    "legends": None,
    "instance_buttons": ["refresh", "save", "delete"],
    "list_buttons": ["refresh", "new"],
    "custom_list_buttons": [],
    "custom_instance_buttons": [
        {"key": "strategyposition", "label": "Positions", "icon": "wb-icon-stats"},
        {
            "_buttons": [
                {
                    "key": "portfoliorole",
                    "label": "Portfolio Roles",
                    "icon": "wb-icon-person",
                }
            ]
        },
    ],
    "custom_list_instance_buttons": [
        {"key": "strategyposition", "label": "Positions", "icon": "wb-icon-stats"},
        {
            "_buttons": [
                {
                    "key": "portfoliorole",
                    "label": "Portfolio Roles",
                    "icon": "wb-icon-person",
                }
            ]
        },
    ],
    "list_widget_title": "Strategies",
    "instance_widget_title": "Strategy: {{title}}",
    "new_instance_widget_title": "New Strategy",
    "pagination_type": "cursor",
    "fields": {
        "id": {
            "key": "id",
            "label": "Id",
            "type": "primary_key",
            "required": False,
            "read_only": True,
        },
        "title": {
            "key": "title",
            "label": "Title",
            "type": "text",
            "required": True,
            "read_only": False,
        },
        "ticker": {
            "key": "ticker",
            "label": "Ticker",
            "type": "text",
            "required": True,
            "read_only": False,
        },
        "isin": {
            "key": "isin",
            "label": "ISIN",
            "type": "text",
            "required": True,
            "read_only": False,
        },
        "currency": {
            "key": "currency",
            "label": "Currency",
            "type": "select",
            "required": True,
            "read_only": False,
            "representation_key": "_currency",
            "endpoint": {
                "url": "http://localhost:5000/api/currency/currencyrepresentation/",
                "value_key": "id",
                "label_key": "{{key}} ({{symbol}})",
            },
        },
        "is_cash": {
            "key": "is_cash",
            "label": "Is cash",
            "type": "boolean",
            "required": True,
            "read_only": False,
        },
        "_additional_resources": {
            "key": "_additional_resources",
            "label": " additional resources",
            "type": "field",
            "required": False,
            "read_only": True,
        },
    },
    "filter_fields": {
        "title": {
            "label": "Title",
            "type": "text",
            "key": "title",
            "visible": False,
            "required": False,
        },
        "isin": {
            "label": "ISIN",
            "type": "text",
            "key": "isin",
            "visible": False,
            "required": False,
        },
        "ticker": {
            "label": "Ticker",
            "type": "text",
            "key": "ticker",
            "visible": False,
            "required": False,
        },
        "currency": {
            "label": "Currency",
            "type": "select",
            "key": "currency",
            "visible": False,
            "required": False,
            "multiple": True,
            "endpoint": {
                "url": "http://localhost:5000/api/currency/currency/",
                "value_key": "id",
                "label_key": "{{key}} ({{symbol}})",
            },
        },
        "is_cash": {
            "label": "Cash",
            "type": "boolean",
            "key": "is_cash",
            "visible": False,
            "required": False,
        },
        "parent_strategy": {
            "label": "Parent Strategy",
            "type": "select",
            "key": "parent_strategy",
            "visible": False,
            "required": False,
            "multiple": True,
            "endpoint": {
                "url": "http://localhost:5000/api/portfolio/strategyrepresentation/",
                "value_key": "id",
                "label_key": "{{title}} {{ticker}}",
            },
        },
    },
    "ordering_fields": ["title", "ticker"],
    "search_fields": ["title", "ticker"],
}
# example = json.dumps(example_dict)
# print(example)

validate(instance=example_dict, schema=schema)
