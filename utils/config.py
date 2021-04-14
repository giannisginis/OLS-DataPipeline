""" The basic configuration of the pipeline """


class DatabaseMetadata:
    """ DB Configuration"""
    POSTGRES_USER = 'root'
    POSTGRES_PASSWORD = 'root'
    POSTGRES_HOST = 'localhost'
    POSTGRES_PORT = 5432
    db_name = 'DataPipeline'


class OntologyLookupService:
    """ The OLS API uri """
    API = 'http://www.ebi.ac.uk/ols/api/ontologies/'
