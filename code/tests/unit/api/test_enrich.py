from http import HTTPStatus
from unittest.mock import patch

from pytest import fixture

from .utils import get_headers
from ..conftest import mock_api_response
from ..payloads_for_tests import (
    EXPECTED_RESPONSE_OF_JWKS_ENDPOINT,
    EXPECTED_RESPONSE_FROM_GRAYLOG
)


def routes():
    yield '/deliberate/observables'
    yield '/observe/observables'
    yield '/refer/observables'


@fixture(scope='module', params=routes(), ids=lambda route: f'POST {route}')
def route(request):
    return request.param


@fixture(scope='module')
def invalid_json_value():
    return [{'type': 'ip', 'value': ''}]


@patch('requests.get')
def test_enrich_call_with_valid_jwt_but_invalid_json_value(
        mock_request,
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
    return [{'type': 'domain', 'value': '24.141.154.216'}]


@patch('api.client.GraylogClient.get_data')
@patch('requests.get')
def test_enrich_call_success(mock_get, mock_request,
                             route, client, valid_jwt, valid_json):
    mock_request.return_value = mock_api_response(
        payload=EXPECTED_RESPONSE_FROM_GRAYLOG)

    mock_get.return_value = \
        mock_api_response(payload=EXPECTED_RESPONSE_OF_JWKS_ENDPOINT)

    response = client.post(route, headers=get_headers(valid_jwt()),
                           json=valid_json)
    assert response.status_code == HTTPStatus.OK
