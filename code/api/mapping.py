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
        return {
            'origin': message.get('source'),
            'relation': 'Connected_To',
            'source': {'value': message.get('source_ip'), 'type': 'ip'},
            'related': {'value': message.get('destination_ip'), 'type': 'ip'},
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
