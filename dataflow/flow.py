""" This module performs the high level functionality of the data flow"""

from dataflow.iterators import iter_terms_from_api, iter_synonyms_from_response, \
    iter_parents_from_response, iter_xref_from_response, iter_terms_ontology_from_response
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


class Flow:
    """
    This class performs the high level procedures of the data flow.
    */ Connection to DB
    */ Data collection from OLS API
    */ Table creation and data insertion or only data insertion based on the mode that client chosen
    */ Closes connections to DB
    """

    def __init__(self, ontology: str):
        self.ontology_value = ontology
        self._configure_flow()
        # instantiate class tables
        self.terms = Terms(self.connection, self.cursor)
        self.synonyms = Synonyms(self.connection, self.cursor)
        self.terms_synonyms = TermsSynonyms(self.connection, self.cursor)
        self.ontology = Ontology(self.connection, self.cursor)
        self.terms_ontology = TermsOntology(self.connection, self.cursor)
        self.xref = Xref(self.connection, self.cursor)

    @staticmethod
    def _make_connection():
        """ connect to database"""
        return Connection().connect()

    def _close_connection(self):
        """ close the communication with the PostgreSQL"""
        Connection().close_connection(self.connection)

    def _collect_data(self):
        """ collect data from ols api for the specific ontology """
        return MakeRequest().get(ontology=self.ontology_value)

    def _configure_flow(self):
        """ wraps up the initial procedures """
        self.connection, self.cursor = self._make_connection()
        self.response, self.session = self._collect_data()

    def _create_tables(self):
        """ Creates the proper tables """
        self.terms.create_table()
        logger.log_info("Created terms table")

        self.synonyms.create_table()
        logger.log_info("Created synonyms table")

        self.terms_synonyms.create_table()
        logger.log_info("Created terms-synonyms table")

        self.ontology.create_table()
        logger.log_info("Created ontology table")

        self.terms_ontology.create_table()
        logger.log_info("Created terms_ontology table")

        self.xref.create_table()
        logger.log_info("Created xref table")

    def _insert(self):
        """ Builds the proper data generators and executes the bulk inserts"""

        # create an iterator, create a table and bulk insertion for terms metadata
        terms_iter = iter_terms_from_api(response=self.response)

        logger.log_info("Executing Bulk insert to terms table")
        self.terms.bulk_insert(terms_iter, page_size=20)
        logger.log_info("Bulk insert finished")

        del terms_iter

        # create an iterator, create a table and bulk insertion for synonyms metadata
        synonyms_iter = iter_synonyms_from_response(response=self.response)

        logger.log_info("Executing Bulk insert to synonyms table")
        self.synonyms.bulk_insert(synonyms_iter, page_size=118)
        logger.log_info("Bulk insert finished")
        del synonyms_iter

        terms_synonyms_iter = iter_synonyms_from_response(response=self.response)
        logger.log_info("Executing Bulk insert to terms-synonyms table")
        self.terms_synonyms.bulk_insert(terms_synonyms_iter, page_size=118)
        logger.log_info("Bulk insert finished")
        del terms_synonyms_iter

        # create an iterator, create a table and bulk insertion for parent links
        parents_iter = iter_parents_from_response(response=self.response, session=self.session)

        logger.log_info("Executing Bulk insert to ontology table")
        self.ontology.bulk_insert(parents_iter, page_size=20)
        logger.log_info("Bulk insert finished")
        del parents_iter

        # create an iterator, create a table and bulk insertion for terms_ontology
        terms_ontology_iter = iter_terms_ontology_from_response(response=self.response,
                                                                session=self.session)

        logger.log_info("Executing Bulk insert to Terms-Ontology table")
        self.terms_ontology.bulk_insert(terms_ontology_iter, page_size=20)
        logger.log_info("Bulk insert finished")
        del terms_ontology_iter

        # create an iterator, create a table and bulk insertion for MSH xref metadata
        xref_iter = iter_xref_from_response(response=self.response)

        logger.log_info("Executing Bulk insert to xref table")
        self.xref.bulk_insert(xref_iter, page_size=20)
        logger.log_info("Bulk insert finished")
        del xref_iter

    def create(self):
        """ This mode creates tables and make insertions for a specific ontology"""
        self._create_tables()
        self._insert()
        # close the communication with the PostgreSQL
        self._close_connection()

    def update(self):
        """ This mode updates the existing tables with data for a specific ontology"""
        self._insert()
        # close the communication with the PostgreSQL
        self._close_connection()
