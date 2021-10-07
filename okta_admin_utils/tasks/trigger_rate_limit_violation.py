import logging
from concurrent.futures import ThreadPoolExecutor, wait
import click

from okta_admin_utils.logs import format_json_output
from okta_admin_utils.api import OktaAPIClient

REQUESTS = 1000
THREADS = 100


def job(num, api_resource):
    api_resource.list(params={'limit': 2})


class Client(OktaAPIClient):

    def run(self):
        resource = click.prompt(
            'Which endpoint would you like to flood with GET requests?',
            type=click.Choice(['users', 'groups', 'logs', 'apps']),
            default='users'
        )
        confirm = click.prompt(
            'This will flood the /api/{} endpoint with ~1,000 requests. Are you sure (y/n)?'.format(resource),
            type=bool,
            default='n'
        )
        if confirm:
            self.api.add_resource(resource_name=resource)
            api_resource = getattr(self.api, resource)
            args = range(REQUESTS)
            with ThreadPoolExecutor(max_workers=THREADS) as executor:
                futures = {executor.submit(job, arg, api_resource) for arg in args}
                wait(futures)
                print(len(futures))
                logging.info('Complete')
