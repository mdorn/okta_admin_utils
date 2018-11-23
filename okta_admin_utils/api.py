from simple_rest_client.api import API


class OktaAPIClient(object):
    def __init__(self, org_url, api_key):
        self.api = API(
            api_root_url='{}/api/v1'.format(org_url),
            headers={
                'Accept': 'application/json',
                'Content-type': 'application/json',
                'Authorization': 'SSWS {}'.format(api_key),
            },
            timeout=10,
            json_encode_body=True,
        )


# FIXME: determine how to dynamically get default actions from
#   simple_rest_client
def get_default_actions(resource):
    return {
      'create': {
        'method': 'POST',
        'url': resource
      },
      'destroy': {
        'method': 'DELETE',
        'url': '%s/{}' % resource
      },
      'list': {
        'method': 'GET',
        'url': resource
      },
      'partial_update': {
        'method': 'PATCH',
        'url': '%s/{}' % resource
      },
      'retrieve': {
        'method': 'GET',
        'url': '%s/{}' % resource
      },
      'update': {
        'method': 'PUT',
        'url': '%s/{}' % resource
      }
    }
