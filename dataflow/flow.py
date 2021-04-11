""" This module performs the high level functionality of the data flow"""

from dataflow.iterators import iter_terms_from_api, iter_synonyms_from_response, iter_parents_from_response, iter_xref_from_response
from database.base import Connection
from database.terms import Terms
from database.synonyms import Synonyms
from database.ontology import Ontology
from database.xref import Xref
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


def create(ontology: str):
    # connect to database and collect data from ols api for the specific ontology
    response, session, connection, cursor = configure_flow(ontology=ontology)

    # create an iterator, create a table and bulk insertion for terms metadata
    terms_iter = iter_terms_from_api(response=response)
    terms_table = Terms(connection, cursor)
    terms_table.create_table()
    logger.log_info("Created terms table")

    logger.log_info("Executing Bulk insert to terms table")
    terms_table.bulk_insert(terms_iter, page_size=20)
    logger.log_info("Bulk insert finished")

    del terms_iter

    # create an iterator, create a table and bulk insertion for synonyms metadata
    synonyms_iter = iter_synonyms_from_response(response=response)
    synonyms_table = Synonyms(connection, cursor)
    synonyms_table.create_table()
    logger.log_info("Created synonyms table")

    logger.log_info("Executing Bulk insert to synonyms table")
    synonyms_table.bulk_insert(synonyms_iter, page_size=118)
    logger.log_info("Bulk insert finished")
    del synonyms_iter

    # create an iterator, create a table and bulk insertion for parent links
    parents_iter = iter_parents_from_response(response=response, session=session)
    ontology_table = Ontology(connection, cursor)
    ontology_table.create_table()
    logger.log_info("Created ontology table")

    logger.log_info("Executing Bulk insert to ontology table")
    ontology_table.bulk_insert(parents_iter, page_size=20)
    logger.log_info("Bulk insert finished")
    del parents_iter

    # create an iterator, create a table and bulk insertion for MSH xref metadata
    xref_iter = iter_xref_from_response(response=response)
    xref_table = Xref(connection, cursor)
    xref_table.create_table()
    logger.log_info("Created xref table")

    logger.log_info("Executing Bulk insert to xref table")
    xref_table.bulk_insert(xref_iter, page_size=20)
    logger.log_info("Bulk insert finished")
    del xref_iter

    # close the communication with the PostgreSQL
    close_connection(connection)


def update(ontology: str):
    response, session, connection, cursor = configure_flow(ontology=ontology)
    close_connection(connection)
    pass

