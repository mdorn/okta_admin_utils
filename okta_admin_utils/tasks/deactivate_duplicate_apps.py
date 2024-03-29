import re

from okta_admin_utils.shared.apps import AppClient


class Client(AppClient):

    def _get_app_ids(self):
        apps_response = self.api.apps.list(params={
            'limit': 200,
            'filter': 'status eq "ACTIVE"',
        })
        app_ids = []
        for app in apps_response.body:
            if re.search('\(\d\)', app['label']):
                # find apps with name like "App Name (2)"
                app_ids.append(app['id'])
        return app_ids
