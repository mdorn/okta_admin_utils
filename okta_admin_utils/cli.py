# -*- coding: utf-8 -*-

"""Console script for okta_admin_utils."""
import os
import sys

import click
from dotenv import load_dotenv

from okta_admin_utils.main import TASK_CONFIG


load_dotenv()
ORG_URL = os.environ.get('OKTA_ORG_URL')
API_KEY = os.environ.get('OKTA_API_TOKEN')


@click.command()
@click.argument('task')
def main(task, path=None):
    """Console script for okta_admin_utils."""
    try:
        api_client = TASK_CONFIG[task].Client(ORG_URL, API_KEY)
    except KeyError:
        click.echo('Task "{}" not found. Available tasks are:'.format(task))
        for key in TASK_CONFIG.keys():
            click.echo(key)
        return -1
    api_client.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
