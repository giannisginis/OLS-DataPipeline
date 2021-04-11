""" This module makes the get request to OLS API """
import requests
from utils.config import OntologyLookupService
from requests.exceptions import HTTPError, Timeout
import sys


class MakeRequest:
    def __init__(self):
        self.session = requests.Session()

    def get(self, ontology: str):
        try:
            response = self.session.get(f'{OntologyLookupService.API}{ontology}/terms')
            response.raise_for_status()

            if '_embedded' not in response.json():
                print('[ERROR] Invalid request. Check the ontology id')
                sys.exit(1)
            else:
                return response, self.session
        except HTTPError as http_err:
            print(f'[ERROR] HTTP error occurred: {http_err}')
            sys.exit(1)
        except Timeout as timeout_err:
            print(f'[ERROR] Timeout error occurred: {timeout_err}')
            sys.exit(1)
        except Exception as err:
            print(f'[ERROR] An error occurred: {err}')
            sys.exit(1)

