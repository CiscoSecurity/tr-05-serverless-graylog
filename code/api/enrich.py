from functools import partial

from flask import Blueprint, g

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


@enrich_api.route('/deliberate/observables', methods=['POST'])
def deliberate_observables():
    _ = get_credentials()
    _ = get_observables()
    return jsonify_data({})


@enrich_api.route('/observe/observables', methods=['POST'])
def observe_observables():
    credentials = get_credentials()
    observables = filter_observables(get_observables())

    g.sightings = []
    client = GraylogClient(credentials)

    for observable in observables:
        result = client.get_data(observable)
        messages = (result['results'][client.query_id]['search_types']
                    [client.search_type_id]['messages'])

        mapping = Sighting(observable)

        for message in messages:
            sighting = mapping.extract(message['message'], message['index'])
            g.sightings.append(sighting)

    return jsonify_result()


@enrich_api.route('/refer/observables', methods=['POST'])
def refer_observables():
    _ = get_credentials()
    _ = get_observables()
    return jsonify_data([])
