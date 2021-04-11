from typing import Iterator, Dict, Any


def iter_terms_from_api(response) -> Iterator[Dict[str, Any]]:

    data = response.json()['_embedded']['terms']

    yield from data


def iter_synonyms_from_response(response) -> Iterator[Dict[str, Any]]:

    metadata = []
    for index, term in enumerate(response.json()['_embedded']['terms']):
        try:
            for synonym in term['synonyms']:
                metadata.append({'terms_id': term['short_form'], 'synonyms': synonym})
        except TypeError:
            pass

    yield from metadata


def iter_parents_from_response(response, session) -> Iterator[Dict[str, Any]]:

    metadata = []
    for index, term in enumerate(response.json()['_embedded']['terms']):
        temp_response = session.get(term['_links']['parents']['href']).json()['_embedded']['terms'][0]
        temp_response['child_id'] = term['short_form']
        metadata.append(temp_response)

    yield from metadata

