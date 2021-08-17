import requests

base_url = '<Insert your mluvii URL>'
identity_server = '<Same as base_url unless you using localhost>'
chatbot_id = 2 #Insert your chatbot ID
client_id = '<Insert your API key id>'
client_secret = '<Isert your API secret>'

access_token = None

def get_access_token():
    global access_token
    if access_token is not None:
        return access_token

    url = f'{identity_server}/login/connect/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {
        'response_type': 'token',
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(url, headers=headers, data=payload, verify=False)

    if response.status_code == 200:
        access_token = response.json()['access_token']
        return access_token
    else:
        raise Exception("Could not retrieve access token.")

def get_headers():
    return {
        'Authorization': f'Bearer {get_access_token()}',
        'Content-Type': 'application/json'
    }
