from dataflow.iterators import iter_terms_from_api, iter_synonyms_from_response, iter_parents_from_response, iter_xref_from_response
from database.base import Connection
from database.terms import Terms
from database.synonyms import Synonyms
from database.ontology import Ontology
from database.xref import Xref
from dataflow.make_request import MakeRequest

response, session = MakeRequest().get(ontology='efo')
# terms = requests.get('http://www.ebi.ac.uk/ols/api/ontologies/efo/terms').json()

connection, cursor = Connection.connect()

terms_iter = iter_terms_from_api(response=response)
terms_table = Terms(connection, cursor)
terms_table.create_table()
terms_table.bulk_insert(terms_iter, page_size=20)
del terms_iter

synonyms_iter = iter_synonyms_from_response(response=response)
synonyms_table = Synonyms(connection, cursor)
synonyms_table.create_table()
synonyms_table.bulk_insert(synonyms_iter, page_size=118)
del synonyms_iter

parents_iter = iter_parents_from_response(response=response, session=session)
ontology_table = Ontology(connection, cursor)
ontology_table.create_table()
ontology_table.bulk_insert(parents_iter, page_size=20)
del parents_iter

xref_iter = iter_xref_from_response(response=response)
xref_table = Xref(connection, cursor)
xref_table.create_table()
xref_table.bulk_insert(xref_iter, page_size=20)
del xref_iter


Connection.close_connection(connection)

