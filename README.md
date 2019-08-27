The purpose of this library is to provide an easy way to program common tasks in Python against the [Okta REST API](https://developer.okta.com/docs/reference/). For example, in addition to wrapping the API to perform simple tasks like creating a group (`create-group`), you might have a task like `create-fake-users` to create a given number of example users in your Okta tenant.

Currently available tasks:

```
create-fake-users
remove-deactivated-users
get-users
deactivate-duplicate-apps
delete-inactive-apps
create-oidc-app
create-group
```

## Development

For development, first clone the repo and install dependencies into a virtualenv:

    git clone https://github.com/mdorn/okta_admin_utils.git
    cd okta_admin_utils
    python3 -m venv env/
    . env/bin/activate
    pip install -r requirements_dev.txt

Set up your `.env` with your Okta domain and API token in the current directory as follows:

    OKTA_ORG_URL=https://yoursubdomain.okta.com
    OKTA_API_TOKEN=
    STAGE=dev

Run an example command:

    export PYTHONPATH=.
    python okta_admin_utils/cli.py get-users

## Installation

This library has not yet been published to PyPI, but you can install from source to run the `okta-admin` command, e.g.:

    python setup.py install
    okta-admin get-users

## Contributng

To contribute, create new tasks in `okta_admin_utils/tasks`, and add a reference in `okta_admin_utils/main.py`

Creating a task is as simple as subclassing `OktaAPIClient` and populating the `run` method with an API call and any other code for input and output. An example for getting a formatted JSON list of users:

```python
class Client(OktaAPIClient):

    def run(self):
        self.api.add_resource(resource_name='users')
        limit = click.prompt('How many users?', type=int)
        response = self.api.users.list(params={'limit': limit})
        logging.info(format_json_output(response.body))
```
