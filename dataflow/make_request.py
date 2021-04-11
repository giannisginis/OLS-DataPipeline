""" This module makes the get request to OLS API """
import requests
from utils.config import OntologyLookupService


class MakeRequest:
    def __init__(self):
        self.session = requests.Session()

    def get(self, ontology: str):
        response = self.session.get(f'{OntologyLookupService.API}{ontology}/terms')
        response.raise_for_status()

        return response, self.session
