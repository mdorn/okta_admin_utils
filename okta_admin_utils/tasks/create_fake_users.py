import logging

import click
from faker import Faker
from ..logs import format_json_output
from ..api import OktaAPIClient


class Client(OktaAPIClient):
    def __init__(self, org_url, api_key):
        super().__init__(org_url, api_key)
        self.api.add_resource(resource_name='users')

    def _get_fake_user(self, domain, password):
        fake = Faker()
        first = fake.first_name()
        last = fake.last_name()
        email = '{}.{}@{}'.format(first.lower(), last.lower(), domain)
        user = {
            'profile': {
                'firstName': first,
                'lastName': last,
                'email': email,
                'login': email,
                'mobilePhone': fake.phone_number(),
            },
            'credentials': {
                'password': {
                    'value': password
                }
            }
        }
        return user

    def run(self):
        num_users = click.prompt('How many users?', type=int)
        domain = click.prompt('Domain name?', type=str)
        password = click.prompt('Password?', type=str)
        for i in range(num_users):
            user = self._get_fake_user(domain, password)
            response = self.api.users.create(
                body=user,
                params={'activate': True}
            )
            logging.debug(format_json_output(response.body))
