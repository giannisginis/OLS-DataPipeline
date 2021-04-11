import psycopg2
from utils.config import DatabaseMetadata


class Connection:
    @staticmethod
    def connect():
        """ Connect to the PostgreSQL database server """
        try:

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
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
            print('PostgreSQL database version:')
            cursor.execute('SELECT version()')

            # display the PostgreSQL database server version
            db_version = cursor.fetchone()
            print(db_version)

            return connection, cursor
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    @staticmethod
    def close_connection(connection):
        connection.close()





