""" This module makes the get request to OLS API """
import requests
from utils.config import OntologyLookupService
from requests.exceptions import HTTPError, Timeout
import sys
from utils.logger import LogSystem


class MakeRequest:
    def __init__(self):
        self.session = requests.Session()
        self.logger = LogSystem()

    def get(self, ontology: str):
        try:
            response = self.session.get(f'{OntologyLookupService.API}{ontology}/terms')
            response.raise_for_status()

            if '_embedded' not in response.json():
                self.logger.log_error('Invalid request. Check the ontology id')
                self.logger.log_info('Process finished with exit code 1')
                sys.exit(1)
            else:
                return response, self.session
        except HTTPError as http_err:
            self.logger.log_error(f'HTTP error occurred: {http_err}')
            self.logger.log_info('Process finished with exit code 1')
            sys.exit(1)
        except Timeout as timeout_err:
            self.logger.log_error(f'Timeout error occurred: {timeout_err}')
            self.logger.log_info('Process finished with exit code 1')
            sys.exit(1)
        except Exception as err:
            self.logger.log_error(f'An error occurred: {err}')
            self.logger.log_info('Process finished with exit code 1')
            sys.exit(1)

