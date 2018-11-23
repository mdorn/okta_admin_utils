import logging

import click
from ..logs import format_json_output
from ..api import OktaAPIClient


class Client(OktaAPIClient):
    def __init__(self, org_url, api_key):
        super().__init__(org_url, api_key)
        self.api.add_resource(resource_name='users')

    def run(self):
        limit = click.prompt('How many users?', type=int)
        response = self.api.users.list(params={'limit': limit})
        logging.debug(format_json_output(response.body))
