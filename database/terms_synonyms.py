"""Create terms-synonyms class (table) and define a many to many reference with terms"""

from typing import Iterator, Dict, Any
import psycopg2.extras
from utils.profiler import time_profile
from database.queries import CreateQueries, InsertQueries


class TermsSynonyms:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    @staticmethod
    def _create_terms_synonyms_table(cursor) -> None:
        cursor.execute(CreateQueries.CREATE_TERMS_SYNONYMS)

    @staticmethod
    @time_profile
    def _insert_to_terms_synonyms_table(cursor, data: Iterator[Dict[str, Any]]) -> None:
        cursor.executemany(InsertQueries.INSERT_SYNONYMS, ({**value} for value in data))

    @staticmethod
    @time_profile
    def _insert_to_terms_synonyms_table_batch(cursor, data: Iterator[Dict[str, Any]],
                                        page_size: int = 20) -> None:
        psycopg2.extras.execute_batch(cursor, InsertQueries.INSERT_TERMS_SYNONYMS,
                                      ({**value} for value in data), page_size=page_size)

    def create_table(self):
        self._create_terms_synonyms_table(self.cursor)
        self.connection.commit()

    def bulk_insert(self, iterator: Iterator[Dict[str, Any]], page_size: int = 20) -> None:
        self._insert_to_terms_synonyms_table_batch(cursor=self.cursor, data=iterator, page_size=page_size)
