import binascii
import os
import struct
import time
from random import SystemRandom

import requests
from flask import current_app

from api.errors import AuthorizationError, MoreMessagesAvailableWarning
from api.utils import request_body, add_error

INVALID_CREDENTIALS = 'wrong username or password'


class GraylogClient:
    def __init__(self, credentials):
        self._credentials = credentials
        self._headers = {
            'user-agent': current_app.config['USER_AGENT'],
            'X-Requested-By': current_app.config['REQUESTED_BY']
        }
        self.query_id = None
        self.search_type_id = None

    @property
    def _auth(self):
        return (self._credentials.get('username'),
                self._credentials.get('password'))

    @property
    def _url(self):
        url = current_app.config['GRAYLOG_API_ENDPOINT'].rstrip('/')
        return url.format(host=self._credentials.get('host'))

    @staticmethod
    def _generate_object_id():
        # 4 bytes current time
        oid = struct.pack(">I", int(time.time()))

        # 5 bytes random
        oid += os.urandom(5)

        # 3 bytes inc
        oid += struct.pack(">I", SystemRandom().randint(0, 0xFFFFFF))[1:4]

        return binascii.hexlify(oid).decode()

    def health(self):
        return self._request(path='cluster')

    def get_data(self, observable):
        self.query_id = self._generate_object_id()
        self.search_type_id = self._generate_object_id()
        body = request_body(observable['value'],
                            self.query_id, self.search_type_id)
        path = 'views/search/sync'
        params = {
            'timeout': 60,
        }

        messages = self._request(path, 'POST', payload=body, params=params)
        if (messages['results'][self.query_id]['search_types']
                    [self.search_type_id]['total_results']) \
                > current_app.config['CTR_ENTITIES_LIMIT']:
            add_error(MoreMessagesAvailableWarning(observable))
        return messages

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
