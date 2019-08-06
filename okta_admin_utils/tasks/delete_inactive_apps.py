import logging

import click

from okta_admin_utils.api import OktaAPIClient


class Client(OktaAPIClient):
    def __init__(self, org_url, api_key):
        super().__init__(org_url, api_key)
        self.api.add_resource(resource_name='apps')

    def run(self):
        # return
        apps_response = self.api.apps.list(params={
            'limit': 200,
            'filter': 'status eq "INACTIVE"',
        })
        app_ids = [app['id'] for app in apps_response.body]
        total_ct = len(app_ids)
        if total_ct == 0:
            logging.info('No apps to delete.')
            return
        click.echo(
            click.style(
                '{} apps will be deleted!'.format(total_ct),
                bold=True, fg='blue'
            )
        )
        click.confirm('Do you want to continue?', abort=True)
        ct = 0
        for app_id in app_ids:
            self.api.apps.destroy(app_id)
            ct += 1
        logging.info('{} apps deleted'.format(ct))
