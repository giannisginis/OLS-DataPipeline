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
        temp_response['child_terms_id'] = term['short_form']
        metadata.append(temp_response)

    yield from metadata


def iter_terms_ontology_from_response(response, session) -> Iterator[Dict[str, Any]]:
    metadata = []
    for index, term in enumerate(response.json()['_embedded']['terms']):
        temp_response = session.get(term['_links']['parents']['href']).json()['_embedded']['terms'][0]
        metadata.append({'parent_name': temp_response['short_form'], 'child_terms_id': term['short_form']})

    return metadata


def iter_xref_from_response(response) -> Iterator[Dict[str, Any]]:
    metadata = []
    for index, term in enumerate(response.json()['_embedded']['terms']):
        try:
            for xref in term['obo_xref']:
                if xref['database'] == 'MSH':
                    xref.update({'terms_id': term['short_form']})
                    metadata.append(xref)
        except TypeError:
            pass
    yield from metadata
