import json
import requests
import config as cfg


def get_bearer_token():
    '''
    Gets OAuth v2 bearer token 
    '''
    auth_url = cfg.AUTH_URL
    data = {"grant_type": "client_credentials"}
    response = requests.post(
        auth_url,
        auth=(cfg.CONSUMER_KEY, cfg.CONSUMER_SECRET),
        data=data,
    )

    if response.status_code != 200:
        print('error')

    body = response.json()
    return body['access_token']


def get_rules():
    '''
    Lists all rules for the stream
    '''
    token = get_bearer_token()
    headers = {'Authorization': f'Bearer {token}'}
    url = f'{cfg.BASE_URL}/rules'
    response = requests.get(
        url,
        headers=headers,
    )
    if response.status_code != 200:
        code = response.status_code
        text = response.text
        raise Exception(
            f"Cannot get rules (HTTP {code}): {text}"
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(rules):
    '''
    Deletes all the rules attached to a stream
    '''
    url = f'{cfg.BASE_URL}/rules'
    token = get_bearer_token()
    headers = {'Authorization': f'Bearer {token}'}

    if rules is None or "data" not in rules:
        return None
    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        url,
        headers=headers,
        json=payload,
    )
    if response.status_code != 200:
        code = response.status_code
        text = response.text
        raise Exception(
            f"Cannot delete rules (HTTP {code}): {text}"
        )
    print(json.dumps(response.json()))


def create_rules():
    '''
    Create a rule for streaming the tweets
    '''
    url = f'{cfg.BASE_URL}/rules'
    token = get_bearer_token()
    headers = {'Authorization': f'Bearer {token}'}
    payload = {"add": cfg.ADD_RULES}
    response = requests.post(
        url,
        headers=headers,
        json=payload
    )
    if response.status_code != 201:
        code = response.status_code
        text = response.text
        raise Exception(
            f"Cannot create rules (HTTP {code}): {text}"
        )
    print(json.dumps(response.json()))
