import logging

import click

from okta_admin_utils.api import OktaAPIClient


class Client(OktaAPIClient):
    def __init__(self, org_url, api_key):
        super().__init__(org_url, api_key)
        self.api.add_resource(resource_name='users')

    def run(self):
        users_response = self.api.users.list(params={'filter': 'status eq "DEPROVISIONED"'})
        total_to_remove = len(users_response.body)
        if total_to_remove == 0:
            logging.info('No users to remove.')
            return
        click.echo(
            click.style(
                '{} users will be deleted!'.format(total_to_remove),
                bold=True, fg='blue'
            )
        )
        click.confirm('Do you want to continue?', abort=True)
        ct = 0
        for user in users_response.body:
            self.api.users.destroy(user['id'])
            ct += 1
        logging.info('{} users deleted'.format(ct))
