import logging
from concurrent.futures import ThreadPoolExecutor, wait
import click

from okta_admin_utils.logs import format_json_output
from okta_admin_utils.api import OktaAPIClient


def job(num, api):
    api.groups.list(params={'limit': 2})


class Client(OktaAPIClient):

    def run(self):
        REQUESTS = 1000
        THREADS = 100
        confirm = click.prompt(
            'This will flood the /api/groups endpoint with ~1,000 requests. Are you sure (y/n)?',
            type=bool,
            default='n'
        )
        if confirm:
            self.api.add_resource(resource_name='groups')
            args = range(REQUESTS)
            with ThreadPoolExecutor(max_workers=THREADS) as executor:
                futures = {executor.submit(job, arg, self.api) for arg in args}
                wait(futures)
                print(len(futures))
                logging.info('Complete')
