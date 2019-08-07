import logging

import click
from simple_rest_client.resource import Resource

from okta_admin_utils.logs import format_json_output
from okta_admin_utils.api import OktaAPIClient, get_default_actions


DEFAULT_SCOPES = [
    'openid',
    'profile ',
    'email',
    'address',
    'phone',
    'offline_access',
]


class AuthzSvrResource(Resource):
    # TODO: separate policies into its own resource?
    actions = {
        'scopesCreate': {'method': 'POST', 'url': 'authorizationServers/{}/scopes'},
        'policiesCreate': {
            'method': 'POST', 'url': 'authorizationServers/{}/policies'},
        'policiesRulesCreate': {
            'method': 'POST', 'url': 'authorizationServers/{}/policies/{}/rules'},
    }
    actions.update(get_default_actions('authorizationServers'))


class Client(OktaAPIClient):

    def run(self):
        self.api.add_resource(resource_name='apps')
        self.api.add_resource(
            resource_name='authorizationServers',
            resource_class=AuthzSvrResource
        )
        app_name = click.prompt(
            'Application name?',
            type=str, default='Okta Test OIDC Client')
        app_type = click.prompt(
            'Application type? (web, native, browser, service',
            type=str, default='web')
        app_url = click.prompt(
            'Your application\'s URL?',
            type=str, default='http://localhost:3000')
        redirect_uris = click.prompt(
            'Enter redirect URIs (comma-separated)',
            type=str, default='http://localhost:3000/implicit/callback')
        scopes = click.prompt(
            'Enter any custom scopes (comma-separated)', type=str, default=''
        )
        # app URL (to add as audience/trusted origins)
        # scopes
        # auth server, else create one, add client to auth server access policy
        # TODO: ^^^ data validation

        response_types = [
            'token',
            'id_token',
        ]
        if app_type == 'web':
            grant_types = ['authorization_code']
            response_types.append('code')
        elif app_type == 'browser':
            grant_types = ['implicit']
        elif app_type == 'native':
            # TODO: is this right?
            grant_types = ['implicit']
        elif app_type == 'service':
            grant_types = ['client_credentials']
        # TODO: native, service app types
        app_config = {
            'name': 'oidc_client',
            'label': app_name,
            'signOnMode': 'OPENID_CONNECT',
            'settings': {
                'oauthClient': {
                  'redirect_uris': redirect_uris.split(','),
                  'response_types': response_types,
                  'grant_types': grant_types,
                  'application_type': app_type,
                }
            }
        }
        response = self.api.apps.create(body=app_config)
        app_id = response.body['id']
        logging.info('Created OIDC client with app ID %s', app_id)
        # TODO: deal with the rest of the items in the response

        # create authz server
        auth_svr_config = {
            'name': '{} Authz Server'.format(app_name),
            'description': 'Authorization Server for {}'.format(app_name),
            'audiences': [app_url]
        }
        response = self.api.authorizationServers.create(body=auth_svr_config)
        auth_svr_id = response.body['id']
        logging.info('Created authorization server with ID %s', auth_svr_id)

        # create scopes
        scopes = list(filter(
            lambda scp: scp not in DEFAULT_SCOPES, scopes.split(',')
        ))
        for scope in scopes:
            scope_config = {
                'name': scope,
                'description': '[Created by Okta Admin Utils]',
            }
            self.api.authorizationServers.scopesCreate(
                auth_svr_id,
                body=scope_config
            )
            logging.info('Created scope %s', scope)

        # create authz server policy for oidc client
        policy_config = {
            'type': 'OAUTH_AUTHORIZATION_POLICY',
            'status': 'ACTIVE',
            'name': 'Default Policy',
            'description': '[Created by Okta Admin Utils]',
            'priority': 1,
            'conditions': {
                'clients': {
                    'include': [app_id]
                }
            }
        }
        response = self.api.authorizationServers.policiesCreate(
            auth_svr_id, body=policy_config)
        policy_id = response.body['id']
        logging.info('Created access policy with ID: %s', policy_id)

        # create access policy rule
        policy_rule_config = {
          'conditions': {
            'grantTypes': {'include': grant_types},
            'people': {'groups': {'exclude': [], 'include': ['EVERYONE']}},
            'scopes': {'include': ['*']}
          },
          'name': 'Default',
          'system': False,
          'type': 'RESOURCE_ACCESS'
        }
        response = self.api.authorizationServers.policiesRulesCreate(
            auth_svr_id, policy_id, body=policy_rule_config)
        rule_id = response.body['id']
        logging.info('Created access default policy rule with ID: %s', rule_id)

# curl -v -X GET \
# -H "Accept: application/json" \
# -H "Content-Type: application/json" \
# -H "Authorization: SSWS 00sw_vl0pg5xlgLRcQb-o9ln56Mf12ATc9QIRjFxpE" \
# "https://textmethod.oktapreview.com/api/v1/apps/0oaga21v77e1FW01j0h7"


# curl -v -X GET \
# -H "Accept: application/json" \
# -H "Content-Type: application/json" \
# -H "Authorization: SSWS 00sw_vl0pg5xlgLRcQb-o9ln56Mf12ATc9QIRjFxpE" \
# "https://textmethod.oktapreview.com/api/v1/authorizationServers/ausga58dgkFILNJip0h7/policies/"

# curl -v -X GET \
# -H "Accept: application/json" \
# -H "Content-Type: application/json" \
# -H "Authorization: SSWS 00sw_vl0pg5xlgLRcQb-o9ln56Mf12ATc9QIRjFxpE" \
# https://textmethod.oktapreview.com/api/v1/authorizationServers/ausga58dgkFILNJip0h7/policies/00pga5bi8pkF4cbLi0h7/rules
