from sys import maxsize
from bcrypt import hashpw
from eve.auth import BasicAuth
from flask import current_app as app


class BCryptAuth(BasicAuth):
    def check_auth(self, email, password, allowed_roles, resource, method):
        # use Eve's own db driver; no additional connections/resources are used
        users = app.data.driver.db['user']
        logging_user = users.find_one({'email': email})
        if logging_user and '_id' in logging_user:
            self.set_request_auth_value(logging_user['_id'])
        return user and hashpw(password, logging_user['password']) == logging_user['password']


MONGO_HOST = 'localhost'
MONGO_PORT = 27017

# Skip these if your db has no auth. But it really should.
# MONGO_USERNAME = '<your username>'
# MONGO_PASSWORD = '<your password>'

MONGO_DBNAME = 'snippet_sniper'

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH) and deletes of
# individual items  (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']

user = {
    'item_title': 'user',
    'cache_control': '',
    'cache_expires': 0,
    'item_methods': ['GET', 'PATCH', 'PUT'],
    'resource_methods': ['POST'],
    'authentication': BCryptAuth,
    'additional_lookup': {
        'url': 'regex("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")',
        'field': 'email'
    },
    'schema': {
        # Schema definition, based on Cerberus grammar. Check the Cerberus project
        # (https://github.com/nicolaiarocci/cerberus) for details.
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
            'allowed': ["user", "admin", "superuser"],
            'required': True,
        }
    }
}

snippet = {
    'item_title': 'snippet',
    'cache_control': '',
    'cache_expires': 0,
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PATCH', 'PUT'],
    'authentication': None,
    'schema': {
        'title': {
            'type': 'string',
            'minlength': 5,
            'maxlength': 60,
            'required': True
        },
        'body': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'language': {'type': 'string'},  # Choices
                    'body': {'type': 'string'}
                }
            },
            'minlength': 1,
            'maxlength': maxsize,  # ?
            'required': True
        },
        'owner': {
            'type': 'objectid',
            'required': True,
            # referential integrity constraint: value must exist in the
            # 'people' collection. Since we aren't declaring a 'field' key,
            # will default to `people._id` (or, more precisely, to whatever
            # ID_FIELD value is).
            'data_relation': {
                'resource': 'user',
                # make the owner embeddable with ?embedded={"owner":1}
                'embeddable': True
            },
        },
        'created': {'type': 'datetime'}
    }
}

SETTINGS = {
    'DOMAIN': {
        'user': user,
        'snippet': snippet,
    },
    'X_DOMAINS': '*',
    'X_HEADERS': '*',
    'XML': False
}
