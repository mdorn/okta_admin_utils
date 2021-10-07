import logging

import click

from simple_rest_client.resource import Resource

from okta_admin_utils.api import get_default_actions, OktaAPIClient


class AppResource(Resource):
    actions = {
        'deactivate': {'method': 'POST', 'url': '/apps/{}/lifecycle/deactivate'}
    }
    actions.update(get_default_actions('apps'))


class AppClient(OktaAPIClient):

    def __init__(self, *args, **kwargs):
        super(AppClient, self).__init__(*args, **kwargs)
        self.api.add_resource(resource_name='apps', resource_class=AppResource)

    def _get_app_ids(self):
        # override in subclass
        pass

    def run(self):
        app_ids = self._get_app_ids()
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
