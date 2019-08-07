import logging

import click

from okta_admin_utils.logs import format_json_output
from okta_admin_utils.api import OktaAPIClient

from okta_admin_utils.shared.users import get_fake_user


class Client(OktaAPIClient):

    def run(self):
        self.api.add_resource(resource_name='users')
        num_users = click.prompt('How many users?', type=int)
        domain = click.prompt('Domain name?', type=str)
        password = click.prompt('Password?', type=str)
        for i in range(num_users):
            user = get_fake_user(domain, password)
            response = self.api.users.create(
                body=user,
                params={'activate': True}
            )
            logging.debug(format_json_output(response.body))
