from ipaddress import ip_address

from flask import current_app

CTIM_DEFAULTS = {
    'schema_version': '1.1.6'
}

SIGHTING = 'sighting'

SOURCE = 'Graylog'
CONFIDENCE = 'High'

SIGHTING_DEFAULTS = {
    'count': 1,
    'internal': True,
    'confidence': CONFIDENCE,
    'type': SIGHTING,
    'source': SOURCE,
    'title': 'Log message received by Graylog in'
             ' last 30 days contains observable',
}

IP_VERSION = {
    4: 'IP',
    6: 'IPv6',
}


class Sighting:
    def __init__(self, observable):
        self.observable = observable

    @staticmethod
    def _short_description(message):
        return f'Node {message.get("gl2_source_node").split("-")[0]} ' \
               f'received a log from {message.get("gl2_remote_ip")} ' \
               f'containing the observable'

    @staticmethod
    def _source_uri(index, _id):
        return f'https://{current_app.config["HOST"]}/messages/{index}/{_id}'

    @staticmethod
    def _make_data_table(message):
        data = {
            'columns': [],
            'rows': [[]]
        }

        for key, value in message.items():
            if not (key.startswith(
                    ('_', 'gl2_', 'message', 'streams', 'timestamp'))) \
                    and value:
                data['columns'].append({'name': key, 'type': 'string'})
                data['rows'][0].append(str(value))

        return data

    @staticmethod
    def _make_relations(message):
        source_ip = message.get('source_ip')
        destination_ip = message.get('destination_ip')
        return {
            'origin': message.get('source'),
            'relation': 'Connected_To',
            'source': {
                'value': source_ip,
                'type': IP_VERSION[ip_address(source_ip).version]
            },
            'related': {
                'value': destination_ip,
                'type': IP_VERSION[ip_address(destination_ip).version]
            },
        }

    def extract(self, message, index):
        sighting = {
            'id': message.get('gl2_message_id'),
            'observed_time': {'start_time': message.get('timestamp')},
            'description': f'```\n{message.get("message")} \n```',
            'observables': [self.observable],
            'short_description': self._short_description(message),
            'source_uri': self._source_uri(index, message['_id']),
            'external_ids':
                [message.get('gl2_message_id'), message.get('_id')],
            'data': self._make_data_table(message),
            **CTIM_DEFAULTS,
            **SIGHTING_DEFAULTS,
        }

        if message.get('source_ip') and message.get('destination_ip'):
            sighting['relations'] = self._make_relations(message)

        return sighting
