from functools import partial

from flask import Blueprint, g, current_app

from api.client import GraylogClient
from api.mapping import Sighting
from api.schemas import ObservableSchema
from api.utils import (
    get_json,
    get_credentials,
    jsonify_data,
    jsonify_result,
    filter_observables
)

enrich_api = Blueprint('enrich', __name__)

get_observables = partial(get_json, schema=ObservableSchema(many=True))


@enrich_api.route('/observe/observables', methods=['POST'])
def observe_observables():
    credentials = get_credentials()
    observables = filter_observables(get_observables())

    g.sightings = []
    client = GraylogClient(credentials)

    for observable in observables:
        messages = client.get_data(observable)
        mapping = Sighting(observable)

        for message in messages:
            sighting = mapping.extract(message['message'], message['index'])
            g.sightings.append(sighting)

    return jsonify_result()


@enrich_api.route('/refer/observables', methods=['POST'])
def refer_observables():
    _ = get_credentials()
    observables = get_observables()

    obs_types = current_app.config['SUPPORTED_TYPES']
    relay_output = [
        {
            'id': (f'ref-graylog-search-{observable["type"].replace("_", "-")}'
                   f'-{observable["value"]}'),
            'title': (
                'Search for this '
                f'{obs_types.get(observable["type"], observable["type"])}'
            ),
            'description': (
                'Search for this '
                f'{obs_types.get(observable["type"], observable["type"])} '
                'in the Graylog console'),
            'url': f'https://{current_app.config["HOST"]}/search?rangetype='
                   f'relative&relative=2592000&q={observable["value"]}',
            'categories': ['Graylog', 'Search'],
        }
        for observable in observables
    ]

    return jsonify_data(relay_output)
