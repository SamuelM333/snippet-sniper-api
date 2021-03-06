# -*- coding: utf-8 -*-
from auth import BCryptAuthUser, BCryptAuthSnippet

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
# MONGO_USERNAME = '<your username>'
# MONGO_PASSWORD = '<your password>'
MONGO_DBNAME = 'snippet_sniper'
# AUTH_FIELD = "ID_FIELD"
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']

user = {
    'item_title': 'user',
    'cache_control': '',
    'cache_expires': 0,
    'resource_methods': ['GET', 'POST'],
    'public_methods': ['POST'],
    'item_methods': ['GET', 'PATCH', 'PUT'],
    'public_item_methods': ['GET'],
    'authentication': BCryptAuthUser,
    'additional_lookup': {
        'url': 'regex("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")',
        'field': 'email'
    },
    'schema': {
        'first_name': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 120,
            'required': True,
        },
        'last_name': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 120,
        },
        'email': {
            'type': 'string',
            'minlength': 8,
            'maxlength': 120,
            'required': True,
            'unique': True,
            'regex': "[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
        },
        'password': {
            'type': 'string',
            'minlength': 8,
            'maxlength': 120,
            'required': True,
        },
        'role': {
            'type': 'string',
            'allowed': ['user', 'superuser', 'admin'],
            'required': True,  # Use default
        }
    }
}

snippet = {
    'item_title': 'snippet',
    'cache_control': '',
    'cache_expires': 0,
    'resource_methods': ['GET', 'POST'],
    'public_methods': ['POST', 'GET'],
    'item_methods': ['GET', 'PATCH', 'PUT', 'DELETE'],
    'public_item_methods': ['GET'],
    'authentication': BCryptAuthSnippet,
    'schema': {
        'title': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 60,
            'required': True
        },
        'fragments': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'language': {'type': 'string'},  # Add language choices
                    'body': {'type': 'string'}
                }
            },
            'minlength': 1,
            'maxlength': 12800,
            'required': True
        },
        'owner': {
            'type': 'objectid',
            'required': True,
            'data_relation': {
                'resource': 'user',
                # make the owner embeddable with ?embedded={"owner":1}
                'embeddable': True
            },
        },
        'allowed_users': {
            # Emails of other users
            # Public snippet: Empty
            # Private snippet: Only owner's email
            # Restricted snippet: Owner and others's email
            'type': 'list',
            'schema': {
                'type': 'string',
                'minlength': 8,
                'maxlength': 120,
                'unique': True,
                'regex': "[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
            }
        },
    }
}

SETTINGS = {
    'DOMAIN': {
        'user': user,
        'snippet': snippet,
    },
    'X_DOMAINS': '*',
    'X_HEADERS': '*',
    'MONGO_DBNAME': 'snippet_sniper',
    'XML': False
}
