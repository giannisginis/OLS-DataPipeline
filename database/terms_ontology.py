"""Create terms-ontology class (table) and define a many to many reference with terms"""

from typing import Iterator, Dict, Any
import psycopg2.extras
from utils.profiler import time_profile
from database.queries import CreateQueries, InsertQueries


class TermsOntology:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    @staticmethod
    def _create_terms_ontology_table(cursor) -> None:
        cursor.execute(CreateQueries.CREATE_TERMS_ONTOLOGY)

    @staticmethod
    @time_profile
    def _insert_to_terms_ontology_table_batch(cursor, data: Iterator[Dict[str, Any]],
                                        page_size: int = 20) -> None:
        psycopg2.extras.execute_batch(cursor, InsertQueries.INSERT_TERMS_ONTOLOGY, ({**term} for term in data), page_size=page_size)

    def create_table(self):
        self._create_terms_ontology_table(self.cursor)
        self.connection.commit()

    def bulk_insert(self, iterator: Iterator[Dict[str, Any]], page_size: int = 20) -> None:
        self._insert_to_terms_ontology_table_batch(cursor=self.cursor, data=iterator, page_size=page_size)