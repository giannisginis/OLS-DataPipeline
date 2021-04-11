"""Create terms class (table) and define its characteristics"""

from typing import Iterator, Dict, Any
import psycopg2.extras
from utils.profiler import time_profile
from utils.utils import is_not_none
from utils.config import CreateQueries, InsertQueries


class Terms:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    @staticmethod
    def _create_terms_table(cursor) -> None:
        cursor.execute(CreateQueries.CREATE_TERMS)

    @staticmethod
    @time_profile
    def _insert_to_terms_table(cursor, data: Iterator[Dict[str, Any]]) -> None:
        cursor.executemany(InsertQueries.INSERT_TERMS, ({**term,
                       'description': term['description'][0] if is_not_none(term['description']) else None,
                       'in_subset': term['in_subset'][0] if is_not_none(term['in_subset']) else None,
                       'parents': term['_links']['parents']['href']
                       } for term in data))

    @staticmethod
    @time_profile
    def _insert_to_terms_table_batch(cursor, data: Iterator[Dict[str, Any]],
                                     page_size: int = 20) -> None:
        psycopg2.extras.execute_batch(cursor, InsertQueries.INSERT_TERMS, ({**term,
                       'description': term['description'][0] if is_not_none(term['description']) else None,
                       'in_subset': term['in_subset'][0] if is_not_none(term['in_subset']) else None,
                       'parents': term['_links']['parents']['href']
                       } for term in data), page_size=page_size)

    def create_table(self):
        self._create_terms_table(self.cursor)
        self.connection.commit()

    def bulk_insert(self, iterator: Iterator[Dict[str, Any]], page_size: int = 20) -> None:
        self._insert_to_terms_table_batch(cursor=self.cursor, data=iterator, page_size=page_size)
