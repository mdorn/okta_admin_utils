import logging

import click

from okta_admin_utils.logs import format_json_output
from okta_admin_utils.api import OktaAPIClient


class Client(OktaAPIClient):

    # See https://developer.okta.com/docs/reference/api/groups/#add-group

    def run(self):
        self.api.add_resource(resource_name='groups')
        name = click.prompt('Group name?', type=str)
        description = click.prompt(
            'Group description?', type=str, default='', show_default=False
        )
        response = self.api.groups.create(body={
            'profile': {
                'name': name,
                'description': description,
            }
        })
        logging.debug(format_json_output(response.body))
