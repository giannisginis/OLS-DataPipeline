import psycopg2
from utils.config import DatabaseMetadata
from utils.logger import LogSystem


class Connection:

    def __init__(self):
        self.logger = LogSystem()

    def connect(self):
        """ Connect to the PostgreSQL database server """
        try:

            # connect to the PostgreSQL server
            self.logger.log_info('Connecting to the PostgreSQL database...')
            connection = psycopg2.connect(
                host=DatabaseMetadata.POSTGRES_HOST,
                database=DatabaseMetadata.db_name,
                user=DatabaseMetadata.POSTGRES_USER,
                password=DatabaseMetadata.POSTGRES_PASSWORD,
            )

            connection.autocommit = True

            # create a cursor
            cursor = connection.cursor()

            # execute a statement
            cursor.execute('SELECT version()')

            # display the PostgreSQL database server version
            db_version = cursor.fetchone()
            self.logger.log_info(f'PostgreSQL database version: {db_version[0]}')

            return connection, cursor
        except (Exception, psycopg2.DatabaseError) as error:
            self.logger.log_error(error)

    def close_connection(self, connection):
        # close the communication with the PostgreSQL
        connection.close()
        self.logger.log_info('Database connection closed.')





