""" This module creates all the corresponding data generators needed for the pipeline"""
from typing import Iterator, Dict, Any


def iter_terms_from_api(response) -> Iterator[Dict[str, Any]]:
    """ A data generator for all the response from OLS API
    :param response: the initial response of the OLS API
    """
    data = response.json()['_embedded']['terms']

    yield from data


def iter_synonyms_from_response(response) -> Iterator[Dict[str, Any]]:
    """ A data generator which collects the info for the synonyms.
        More specifically, it collects the synonyms and the corresponding term id.
    :param response: the initial response of the OLS API
    """
    metadata = []
    for index, term in enumerate(response.json()['_embedded']['terms']):
        try:
            for synonym in term['synonyms']:
                metadata.append({'terms_id': term['short_form'], 'synonyms': synonym})
        except TypeError:
            pass

    yield from metadata


def iter_parents_from_response(response, session) -> Iterator[Dict[str, Any]]:
    """ A data generator which collects metadata for the parents per term.
        More specifically, it loops the initial response of the OLS API collects the parent
        links per term and make again the proper request to API to collect all the available
        metadata per parent.
    :param response: the initial response of the OLS API
    :param session: the session of the requests library
    """
    metadata = []
    for index, term in enumerate(response.json()['_embedded']['terms']):
        temp_response = session.get(term['_links']['parents']['href']).json()['_embedded']['terms'][0]
        temp_response['child_terms_id'] = term['short_form']
        metadata.append(temp_response)

    yield from metadata


def iter_terms_ontology_from_response(response, session) -> Iterator[Dict[str, Any]]:
    """
    A data generator which collects metadata for the many to many reference between the terms and
    ontology (parents) tables.
    :param response: the initial response of the OLS API
    :param session: the session of the requests library
    """
    metadata = []
    for index, term in enumerate(response.json()['_embedded']['terms']):
        temp_response = session.get(term['_links']['parents']['href']).json()['_embedded']['terms'][0]
        metadata.append({'parent_name': temp_response['short_form'], 'child_terms_id': term['short_form']})

    yield from metadata


def iter_xref_from_response(response) -> Iterator[Dict[str, Any]]:
    """
    A data generator which collects metadata for the MeSH term
    references (xref with MSH database)
    :param response: the initial response of the OLS API
    """
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
