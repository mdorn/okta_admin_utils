import logging

import click
from okta_admin_utils.logs import format_json_output
from okta_admin_utils.api import OktaAPIClient


class Client(OktaAPIClient):

    def run(self):
        self.api.add_resource(resource_name='users')
        limit = click.prompt('How many users?', type=int)
        response = self.api.users.list(params={'limit': limit})
        logging.info(format_json_output(response.body))
