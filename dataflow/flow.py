""" This module performs the high level functionality of the data flow"""

from dataflow.iterators import iter_terms_from_api, iter_synonyms_from_response, iter_parents_from_response, iter_xref_from_response, iter_terms_ontology_from_response
from database.base import Connection
from database.terms import Terms
from database.synonyms import Synonyms
from database.ontology import Ontology
from database.xref import Xref
from database.terms_synonyms import TermsSynonyms
from database.terms_ontology import TermsOntology
from dataflow.make_request import MakeRequest
from utils.logger import LogSystem
logger = LogSystem()


def make_connection():
    return Connection().connect()


def close_connection(connection):
    Connection().close_connection(connection)


def collect_data(ontology: str):
    return MakeRequest().get(ontology=ontology)


def configure_flow(ontology: str):
    connection, cursor = make_connection()
    response, session = collect_data(ontology=ontology)

    return response, session, connection, cursor


def create_tables(connection, cursor):
    terms = Terms(connection, cursor)
    terms.create_table()
    logger.log_info("Created terms table")

    synonyms = Synonyms(connection, cursor)
    synonyms.create_table()
    logger.log_info("Created synonyms table")

    terms_synonyms = TermsSynonyms(connection, cursor)
    terms_synonyms.create_table()
    logger.log_info("Created terms-synonyms table")

    ontology = Ontology(connection, cursor)
    ontology.create_table()
    logger.log_info("Created ontology table")

    terms_ontology = TermsOntology(connection, cursor)
    terms_ontology.create_table()
    logger.log_info("Created terms_ontology table")

    xref = Xref(connection, cursor)
    xref.create_table()
    logger.log_info("Created xref table")

    return terms, synonyms, terms_synonyms, ontology, terms_ontology, xref


def create(ontology: str):
    # connect to database and collect data from ols api for the specific ontology
    response, session, connection, cursor = configure_flow(ontology=ontology)

    # create an iterator, create a table and bulk insertion for terms metadata
    terms_iter = iter_terms_from_api(response=response)

    terms, synonyms, terms_synonyms, ontology, terms_ontology, xref = create_tables(connection, cursor)
    logger.log_info("Executing Bulk insert to terms table")
    terms.bulk_insert(terms_iter, page_size=20)
    logger.log_info("Bulk insert finished")

    del terms_iter

    # create an iterator, create a table and bulk insertion for synonyms metadata
    synonyms_iter = iter_synonyms_from_response(response=response)

    logger.log_info("Executing Bulk insert to synonyms table")
    synonyms.bulk_insert(synonyms_iter, page_size=118)
    logger.log_info("Bulk insert finished")
    del synonyms_iter

    terms_synonyms_iter = iter_synonyms_from_response(response=response)
    logger.log_info("Executing Bulk insert to terms-synonyms table")
    terms_synonyms.bulk_insert(terms_synonyms_iter, page_size=118)
    logger.log_info("Bulk insert finished")
    del terms_synonyms_iter

    # create an iterator, create a table and bulk insertion for parent links
    parents_iter = iter_parents_from_response(response=response, session=session)

    logger.log_info("Executing Bulk insert to ontology table")
    ontology.bulk_insert(parents_iter, page_size=20)
    logger.log_info("Bulk insert finished")
    del parents_iter

    # create an iterator, create a table and bulk insertion for terms_ontology
    terms_ontology_iter = iter_terms_ontology_from_response(response=response, session=session)

    logger.log_info("Executing Bulk insert to Terms-Ontology table")
    terms_ontology.bulk_insert(terms_ontology_iter, page_size=20)
    logger.log_info("Bulk insert finished")
    del terms_ontology_iter

    # create an iterator, create a table and bulk insertion for MSH xref metadata
    xref_iter = iter_xref_from_response(response=response)

    logger.log_info("Executing Bulk insert to xref table")
    xref.bulk_insert(xref_iter, page_size=20)
    logger.log_info("Bulk insert finished")
    del xref_iter

    # close the communication with the PostgreSQL
    close_connection(connection)


def update(ontology: str):
    response, session, connection, cursor = configure_flow(ontology=ontology)
    # create an iterator, create a table and bulk insertion for terms metadata
    terms_iter = iter_terms_from_api(response=response)
    terms_table = Terms(connection, cursor)
    logger.log_info("Executing Bulk insert to terms table")
    terms_table.bulk_insert(terms_iter, page_size=20)
    logger.log_info("Bulk insert finished")

    del terms_iter

    # create an iterator, create a table and bulk insertion for synonyms metadata
    synonyms_iter = iter_synonyms_from_response(response=response)
    synonyms_table = Synonyms(connection, cursor)
    logger.log_info("Executing Bulk insert to synonyms table")
    synonyms_table.bulk_insert(synonyms_iter, page_size=118)
    logger.log_info("Bulk insert finished")
    del synonyms_iter

    # create an iterator, create a table and bulk insertion for terms_synonyms
    terms_synonyms_table = TermsSynonyms(connection, cursor)
    terms_synonyms_iter = iter_synonyms_from_response(response=response)
    logger.log_info("Executing Bulk insert to terms-synonyms table")
    terms_synonyms_table.bulk_insert(terms_synonyms_iter, page_size=118)
    logger.log_info("Bulk insert finished")
    del terms_synonyms_iter

    # create an iterator, create a table and bulk insertion for parent links
    parents_iter = iter_parents_from_response(response=response, session=session)
    ontology_table = Ontology(connection, cursor)
    logger.log_info("Executing Bulk insert to ontology table")
    ontology_table.bulk_insert(parents_iter, page_size=20)
    logger.log_info("Bulk insert finished")
    del parents_iter

    # create an iterator, create a table and bulk insertion for terms_ontology
    terms_ontology_iter = iter_terms_ontology_from_response(response=response, session=session)
    terms_ontology = TermsOntology(connection, cursor)
    logger.log_info("Executing Bulk insert to Terms-Ontology table")
    terms_ontology.bulk_insert(terms_ontology_iter, page_size=20)
    logger.log_info("Bulk insert finished")
    del terms_ontology_iter

    # create an iterator, create a table and bulk insertion for MSH xref metadata
    xref_iter = iter_xref_from_response(response=response)
    xref_table = Xref(connection, cursor)
    logger.log_info("Executing Bulk insert to xref table")
    xref_table.bulk_insert(xref_iter, page_size=20)
    logger.log_info("Bulk insert finished")
    del xref_iter

    # close the communication with the PostgreSQL
    close_connection(connection)


