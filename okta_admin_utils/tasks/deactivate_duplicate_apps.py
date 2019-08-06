import logging
import re

import click
from simple_rest_client.resource import Resource

from okta_admin_utils.api import OktaAPIClient, get_default_actions


class AppResource(Resource):
    actions = {
        'deactivate': {'method': 'POST', 'url': '/apps/{}/lifecycle/deactivate'}
    }
    actions.update(get_default_actions('apps'))


class Client(OktaAPIClient):
    def __init__(self, org_url, api_key):
        super().__init__(org_url, api_key)
        self.api.add_resource(resource_name='apps', resource_class=AppResource)

    def run(self):
        # return
        apps_response = self.api.apps.list(params={
            'limit': 200,
            'filter': 'status eq "ACTIVE"',
        })
        app_ids = []
        for app in apps_response.body:
            if re.search('\(\d\)', app['label']):
                app_ids.append(app['id'])
        total_ct = len(app_ids)
        if total_ct == 0:
            logging.info('No apps to deactivate.')
            return
        click.echo(
            click.style(
                '{} apps will be deactivated!'.format(total_ct),
                bold=True, fg='blue'
            )
        )
        click.confirm('Do you want to continue?', abort=True)
        ct = 0
        for app_id in app_ids:
            self.api.apps.deactivate(app_id)
            ct += 1
        logging.info('{} apps deactivated'.format(ct))
