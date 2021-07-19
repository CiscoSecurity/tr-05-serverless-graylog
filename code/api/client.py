from flask import current_app
import requests

from api.errors import AuthorizationError

INVALID_CREDENTIALS = 'wrong username or password'


class GraylogClient:
    def __init__(self, credentials):
        self._credentials = credentials
        self._headers = {
            'user-agent': current_app.config['USER_AGENT'],
            'X-Requested-By': current_app.config['REQUESTED_BY']
        }

    @property
    def _auth(self):
        return (self._credentials.get('username'),
                self._credentials.get('password'))

    @property
    def _url(self):
        url = current_app.config['GRAYLOG_API_ENDPOINT']
        return url.format(host=self._credentials.get('host'))

    def health(self):
        return self._request(path='cluster')

    def _request(self, path, method='GET', payload=None, params=None):
        url = '/'.join([self._url, path.lstrip('/')])

        try:
            response = requests.request(method, url, json=payload,
                                        params=params, auth=self._auth,
                                        headers=self._headers)
        except UnicodeEncodeError:
            raise AuthorizationError(INVALID_CREDENTIALS)

        if response.ok:
            return response.json()
