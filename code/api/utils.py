import json
from json.decoder import JSONDecodeError

import jwt
import requests
from flask import request, jsonify, current_app, g
from jwt import InvalidSignatureError, DecodeError, InvalidAudienceError
from requests.exceptions import (
    ConnectionError,
    InvalidURL,
    HTTPError,
    SSLError
)

from api.errors import (
    AuthorizationError,
    InvalidArgumentError,
    GraylogSSLError
)

NO_AUTH_HEADER = 'Authorization header is missing'
WRONG_AUTH_TYPE = 'Wrong authorization type'
WRONG_PAYLOAD_STRUCTURE = 'Wrong JWT payload structure'
WRONG_JWT_STRUCTURE = 'Wrong JWT structure'
WRONG_AUDIENCE = 'Wrong configuration-token-audience'
KID_NOT_FOUND = 'kid from JWT header not found in API response'
WRONG_KEY = ('Failed to decode JWT with provided key. '
             'Make sure domain in custom_jwks_host '
             'corresponds to your SecureX instance region.')
JWKS_HOST_MISSING = ('jwks_host is missing in JWT payload. Make sure '
                     'custom_jwks_host field is present in module_type')
WRONG_JWKS_HOST = ('Wrong jwks_host in JWT payload. Make sure domain follows '
                   'the visibility.<region>.cisco.com structure')


def get_public_key(jwks_host, token):
    """
    Get public key by requesting it from specified jwks host.
    """

    expected_errors = (
        ConnectionError,
        InvalidURL,
        KeyError,
        JSONDecodeError,
        HTTPError,
    )
    try:
        response = requests.get(f"https://{jwks_host}/.well-known/jwks")
        response.raise_for_status()
        jwks = response.json()

        public_keys = {}
        for jwk in jwks['keys']:
            kid = jwk['kid']
            public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(
                json.dumps(jwk)
            )
        kid = jwt.get_unverified_header(token)['kid']
        return public_keys.get(kid)
    except expected_errors:
        raise AuthorizationError(WRONG_JWKS_HOST)


def get_auth_token():
    """
    Parse and validate incoming request Authorization header.
    """
    expected_errors = {
        KeyError: NO_AUTH_HEADER,
        AssertionError: WRONG_AUTH_TYPE
    }
    try:
        scheme, token = request.headers['Authorization'].split()
        assert scheme.lower() == 'bearer'
        return token
    except tuple(expected_errors) as error:
        raise AuthorizationError(expected_errors[error.__class__])


def get_credentials():
    """
    Get Authorization token and validate its signature
    against the public key from /.well-known/jwks endpoint.
    """

    expected_errors = {
        KeyError: JWKS_HOST_MISSING,
        AssertionError: WRONG_PAYLOAD_STRUCTURE,
        InvalidSignatureError: WRONG_KEY,
        DecodeError: WRONG_JWT_STRUCTURE,
        InvalidAudienceError: WRONG_AUDIENCE,
        TypeError: KID_NOT_FOUND
    }
    token = get_auth_token()
    try:
        jwks_host = jwt.decode(
            token, options={'verify_signature': False}
        )['jwks_host']
        key = get_public_key(jwks_host, token)
        aud = request.url_root
        payload = jwt.decode(
            token, key=key, algorithms=['RS256'], audience=[aud.rstrip('/')]
        )
        assert 'host' in payload
        assert 'username' in payload
        assert 'password' in payload

        current_app.config['HOST'] = payload['host']
        set_ctr_entities_limit(payload)

        return payload
    except tuple(expected_errors) as error:
        message = expected_errors[error.__class__]
        raise AuthorizationError(message)


def get_json(schema):
    """
    Parse the incoming request's data as JSON.
    Validate it against the specified schema.
    """

    data = request.get_json(force=True, silent=True, cache=False)

    message = schema.validate(data)

    if message:
        raise InvalidArgumentError(message)

    return data


def jsonify_data(data):
    return jsonify({'data': data})


def jsonify_errors(data):
    return jsonify({'errors': [data]})


def set_ctr_entities_limit(payload):
    try:
        ctr_entities_limit = int(payload['CTR_ENTITIES_LIMIT'])
        assert ctr_entities_limit > 0
    except (KeyError, ValueError, AssertionError):
        ctr_entities_limit = current_app.config['CTR_DEFAULT_ENTITIES_LIMIT']
    current_app.config['CTR_ENTITIES_LIMIT'] = ctr_entities_limit


def format_docs(docs):
    return {'count': len(docs), 'docs': docs}


def jsonify_result():
    result = {'data': {}}

    if g.get('sightings'):
        result['data']['sightings'] = format_docs(g.sightings)

    if g.get('errors'):
        result['errors'] = g.errors

        if not result.get('data'):
            result.pop('data', None)

    return jsonify(result)


def request_body(observable, query_id, search_type_id):
    return {
        'queries':
            [
                {
                    'id': f'{query_id}',
                    'timerange':
                        {
                            'type': 'relative',
                            'range': 2592000
                        },
                    'query':
                        {
                            'type': 'elasticsearch',
                            'query_string': f'\"{observable}\"'
                        },
                    'search_types':
                        [
                            {
                                'id': f'{search_type_id}',
                                'limit': int(
                                    current_app.config['CTR_ENTITIES_LIMIT']),
                                'offset': 0,
                                'sort':
                                    [
                                        {
                                            'field': 'timestamp',
                                            'order': 'DESC'
                                        }
                                    ],
                                'type': 'messages'
                            }
                        ]
                }
            ]
    }


def remove_duplicates(observables):
    return [dict(t) for t in {tuple(d.items()) for d in observables}]


def filter_observables(observables):
    supported_types = current_app.config['SUPPORTED_TYPES']
    observables = remove_duplicates(observables)
    return list(
        filter(lambda obs: (
                obs['type'] in supported_types.keys() and obs["value"] != "0"
                and not obs["value"].isspace()
        ), observables)
    )


def add_error(error):
    g.errors = [*g.get('errors', []), error.json]


def catch_ssl_errors(func):
    def wraps(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SSLError as error:
            raise GraylogSSLError(error)
    return wraps
