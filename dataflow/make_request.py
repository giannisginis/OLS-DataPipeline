import requests
from utils.config import OntologyLookupService


class MakeRequest:
    def __init__(self):
        self.session = requests.Session()

    def get(self, ontology: str = 'efo'):
        response = self.session.get(f'{OntologyLookupService.API}{ontology}/terms')
        response.raise_for_status()

        return response, self.session
