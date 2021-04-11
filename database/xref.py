"""Create xref class (table) and define its characteristics"""

from typing import Iterator, Dict, Any
import psycopg2.extras
from utils.profiler import time_profile
from utils.config import CreateQueries, InsertQueries


class Xref:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

    @staticmethod
    def _create_xref_table(cursor) -> None:
        cursor.execute(CreateQueries.CREATE_XREF)

    @staticmethod
    @time_profile
    def _insert_to_xref_table(cursor, data: Iterator[Dict[str, Any]]) -> None:
        cursor.executemany(InsertQueries.INSERT_XREF, ({**value} for value in data))

    @staticmethod
    @time_profile
    def _insert_to_xref_table_batch(cursor, data: Iterator[Dict[str, Any]],
                                    page_size: int = 20) -> None:
        psycopg2.extras.execute_batch(cursor, InsertQueries.INSERT_XREF,
                                      ({**value} for value in data), page_size=page_size)

    def create_table(self):
        self._create_xref_table(self.cursor)
        self.connection.commit()

    def bulk_insert(self, iterator: Iterator[Dict[str, Any]], page_size: int = 20) -> None:
        self._insert_to_xref_table_batch(cursor=self.cursor, data=iterator, page_size=page_size)
