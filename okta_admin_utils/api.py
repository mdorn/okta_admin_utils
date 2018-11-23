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
