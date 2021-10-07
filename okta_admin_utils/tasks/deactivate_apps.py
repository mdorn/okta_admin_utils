import click

from okta_admin_utils.shared.apps import AppClient


class Client(AppClient):

    def _get_app_ids(self):
        query = click.prompt('Name starts with?', type=str)
        apps_response = self.api.apps.list(params={
            'limit': 200,
            'q': query,
        })
        app_ids = []
        for app in apps_response.body:
            app_ids.append(app['id'])
        return app_ids
