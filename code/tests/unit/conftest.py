from http import HTTPStatus
from unittest.mock import MagicMock

import jwt
from pytest import fixture

from api.errors import INVALID_ARGUMENT
from app import app
from tests.unit.payloads_for_tests import PRIVATE_KEY


@fixture(scope='session')
def client():
    app.rsa_private_key = PRIVATE_KEY

    app.testing = True

    with app.test_client() as client:
        yield client


@fixture(scope='session')
def valid_jwt(client):
    def _make_jwt(
            jwks_host='visibility.amp.cisco.com',
            aud='http://localhost',
            kid='02B1174234C29F8EFB69911438F597FF3FFEE6B7',
            username='username',
            password='password',
            host='host',
            wrong_structure=False,
            missing_jwks_host=False,
            limit=False,
    ):
        payload = {
            'jwks_host': jwks_host,
            'aud': aud,
            'username': username,
            'password': password,
            'host': host,
        }

        if missing_jwks_host:
            payload.pop('jwks_host')

        if wrong_structure:
            payload.pop('username')

        if limit:
            payload['CTR_ENTITIES_LIMIT'] = '1'

        return jwt.encode(
            payload, client.application.rsa_private_key, algorithm='RS256',
            headers={
                'kid': kid
            }
        )

    return _make_jwt


@fixture(scope='module')
def invalid_json_expected_payload():
    def _make_message(message):
        return {
            'errors': [{
                'code': INVALID_ARGUMENT,
                'message': message,
                'type': 'fatal'
            }]
        }

    return _make_message


@fixture
def mock_api_response(status_code=HTTPStatus.OK):
    def _make_mock(payload=None, status_code=status_code):
        mock_response = MagicMock()
        mock_response.status_code = status_code
        mock_response.ok = status_code == HTTPStatus.OK
        mock_response.json = lambda: payload
        return mock_response
    return _make_mock


@fixture(scope='module')
def ssl_error_expected_relay_response():
    return {
        'errors':
            [
                {
                    'code': 'unknown',
                    'message':
                        'Unable to verify SSL certificate: '
                        'self signed certificate',
                    'type': 'fatal'
                }
            ]
    }


@fixture(scope='module')
def connection_error_expected_relay_response():
    return {
        'errors':
            [
                {
                    'code': 'connection error',
                    'message':
                        'Unable to connect to Graylog, validate the '
                        'configured API endpoint: '
                        'https://host/api',
                    'type': 'fatal'
                }
            ]
    }


@fixture
def mock_exception_for_ssl_error():
    mock_response = MagicMock()
    mock_response.reason.args.__getitem__().verify_message = 'self signed' \
                                                             ' certificate'
    return mock_response


@fixture(scope='module')
def authorization_error_expected_relay_response():
    return {
        'errors':
            [
                {
                    'code': 'authorization error',
                    'message': 'Authorization failed: wrong '
                               'username or password',
                    'type': 'fatal'
                }
            ]
    }
