"""Create ontology class (table) and define its characteristics. Ontology refers to parent links"""

from typing import Iterator, Dict, Any
import psycopg2.extras
from utils.profiler import time_profile
from utils.utils import is_not_none
from database.queries import CreateQueries, InsertQueries


class Ontology:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    @staticmethod
    def _create_ontology_table(cursor) -> None:
        cursor.execute(CreateQueries.CREATE_ONTOLOGY)

    @staticmethod
    @time_profile
    def _insert_to_ontology_table_batch(cursor, data: Iterator[Dict[str, Any]],
                                        page_size: int = 20) -> None:
        psycopg2.extras.execute_batch(cursor, InsertQueries.INSERT_ONTOLOGY, ({**term,
                       'description': term['description'][0] if is_not_none(term['description']) else None,
                       'in_subset': term['in_subset'][0] if is_not_none(term['in_subset']) else None
                       } for term in data), page_size=page_size)

    def create_table(self):
        self._create_ontology_table(self.cursor)
        self.connection.commit()

    def bulk_insert(self, iterator: Iterator[Dict[str, Any]], page_size: int = 20) -> None:
        self._insert_to_ontology_table_batch(cursor=self.cursor, data=iterator, page_size=page_size)
