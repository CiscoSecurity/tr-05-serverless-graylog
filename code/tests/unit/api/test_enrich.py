from http import HTTPStatus
from unittest.mock import patch

from pytest import fixture
from requests.exceptions import SSLError, ConnectionError

from tests.unit.api.utils import get_headers
from tests.unit.payloads_for_tests import (
    EXPECTED_RESPONSE_OF_JWKS_ENDPOINT,
    EXPECTED_RESPONSE_FROM_GRAYLOG,
    EXPECTED_RESPONSE_FROM_RELAY,
    EXPECTED_RESPONSE_FROM_RELAY_MORE_MESSAGES_AVAILABLE,
    EXPECTED_RESPONSE_FROM_REFER_ENDPOINT,
)


def routes():
    yield '/observe/observables'
    yield '/refer/observables'


def object_ids():
    yield '60f9b4c461bf9b2a8a999b85'
    yield '60f9b550a09a4d867ecd0169'


@fixture(scope='module', params=routes(), ids=lambda route: f'POST {route}')
def route(request):
    return request.param


@fixture(scope='module')
def invalid_json_value():
    return [{'type': 'ip', 'value': ''}]


@patch('requests.get')
def test_enrich_call_with_valid_jwt_but_invalid_json_value(
        mock_request, mock_api_response,
        route, client, valid_jwt, invalid_json_value,
        invalid_json_expected_payload
):
    mock_request.return_value = \
        mock_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT)
    response = client.post(route,
                           headers=get_headers(valid_jwt()),
                           json=invalid_json_value)
    assert response.status_code == HTTPStatus.OK
    assert response.json == invalid_json_expected_payload(
        "{0: {'value': ['Field may not be blank.']}}"
    )


@fixture(scope='module')
def valid_json():
    return [{'type': 'ip', 'value': '24.141.154.216'}]


@patch('api.client.GraylogClient._generate_object_id')
@patch('requests.request')
@patch('requests.get')
def test_enrich_call_success(mock_get, mock_request, mock_id, route, client,
                             mock_api_response, valid_jwt, valid_json):
    mock_request.return_value = \
        mock_api_response(EXPECTED_RESPONSE_FROM_GRAYLOG)
    mock_id.side_effect = object_ids()
    mock_get.return_value = \
        mock_api_response(EXPECTED_RESPONSE_OF_JWKS_ENDPOINT)

    response = client.post(route, headers=get_headers(valid_jwt()),
                           json=valid_json)
    assert response.status_code == HTTPStatus.OK
    if route == '/observe/observables':
        assert response.json == EXPECTED_RESPONSE_FROM_RELAY
    elif route == '/refer/observables':
        assert response.json == EXPECTED_RESPONSE_FROM_REFER_ENDPOINT


@patch('api.client.GraylogClient._generate_object_id')
@patch('requests.request')
@patch('requests.get')
def tests_enrich_call_with_more_messages_available(
        mock_get, mock_request, mock_id,
        client, valid_jwt, valid_json, mock_api_response):
    mock_request.return_value = \
        mock_api_response(EXPECTED_RESPONSE_FROM_GRAYLOG)
    mock_id.side_effect = object_ids()
    mock_get.return_value = \
        mock_api_response(EXPECTED_RESPONSE_OF_JWKS_ENDPOINT)

    response = client.post('/observe/observables', headers=get_headers(
        valid_jwt(limit=True)), json=valid_json)

    assert response.status_code == HTTPStatus.OK
    assert response.json == \
           EXPECTED_RESPONSE_FROM_RELAY_MORE_MESSAGES_AVAILABLE


@patch('api.client.GraylogClient._request')
@patch('requests.get')
def test_enrich_call_with_ssl_error(mock_get, mock_request, mock_api_response,
                                    mock_exception_for_ssl_error,
                                    client, valid_jwt, valid_json,
                                    ssl_error_expected_relay_response):

    mock_get.return_value = \
        mock_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT)
    mock_request.side_effect = [SSLError(mock_exception_for_ssl_error)]

    response = client.post('/observe/observables',
                           headers=get_headers(valid_jwt()), json=valid_json)
    assert response.status_code == HTTPStatus.OK
    assert response.json == ssl_error_expected_relay_response


@patch('requests.request')
@patch('requests.get')
def test_enrich_call_with_connection_error(
        mock_get, mock_request, mock_api_response,
        client, valid_jwt, valid_json,
        connection_error_expected_relay_response):

    mock_get.return_value = \
        mock_api_response(EXPECTED_RESPONSE_OF_JWKS_ENDPOINT)
    mock_request.side_effect = ConnectionError()

    response = client.post('/observe/observables',
                           headers=get_headers(valid_jwt()),
                           json=valid_json)
    assert response.status_code == HTTPStatus.OK
    assert response.json == connection_error_expected_relay_response


@patch('requests.request')
@patch('requests.get')
def test_enrich_call_with_unicode_encode_error(
        mock_get, mock_request, mock_api_response,
        client, valid_jwt, valid_json,
        authorization_error_expected_relay_response):

    mock_get.return_value = \
        mock_api_response(EXPECTED_RESPONSE_OF_JWKS_ENDPOINT)
    mock_request.side_effect = UnicodeEncodeError('codec', '\x00\x00',
                                                  1, 2, 'fake reason')

    response = client.post('/observe/observables',
                           headers=get_headers(valid_jwt()),
                           json=valid_json)
    assert response.status_code == HTTPStatus.OK
    assert response.json == authorization_error_expected_relay_response


@patch('requests.request')
@patch('requests.get')
def test_enrich_call_with_unauthorized_error(
        mock_get, mock_request, mock_api_response,
        client, valid_jwt, valid_json,
        authorization_error_expected_relay_response):

    mock_get.return_value = \
        mock_api_response(EXPECTED_RESPONSE_OF_JWKS_ENDPOINT)
    mock_request.return_value = mock_api_response(
        status_code=HTTPStatus.UNAUTHORIZED)

    response = client.post('/observe/observables',
                           headers=get_headers(valid_jwt()),
                           json=valid_json)
    assert response.status_code == HTTPStatus.OK
    assert response.json == authorization_error_expected_relay_response
