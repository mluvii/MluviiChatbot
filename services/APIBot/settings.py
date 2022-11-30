import requests


class bot:
    def __init__(self, chatbot_id, client_id, client_secret):
        self.chatbot_id = chatbot_id
        self.client_id = client_id
        self.client_secret = client_secret

access_token = None
bots = []
#base_url = "https://appdev.mluvii.com"


botOne = bot(4005003, "c625e32d04813c82290b33125d062d57", "61f20aa808561b08d1e8773493f47935")
botTwo = bot(2005003, "99890faddf1774c488dbff34acb954d7", "04507eef6f2f799ed9c8ce47bf63a5fb")

#botOne = bot(2, "972aa50e18e55b8b145f893061c9d82f", "82d9e23bf2c72151ffcbdec413c6a50e")
#botTwo = bot(2005003, "99890faddf1774c488dbff34acb954d7", "04507eef6f2f799ed9c8ce47bf63a5fb")

bots.append(botOne)
bots.append(botTwo)

def set_base_url(url):
    global base_url
    base_url = url

def get_base_url():
    return base_url

def get_access_token(bot):
    global access_token

    url = f'{base_url}/login/connect/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    print("Url is: "+url+" with ci: " + bot.client_id + " and secret "+ bot.client_secret)
    payload = {
        'response_type': 'token',
        'grant_type': 'client_credentials',
        'client_id': bot.client_id,
        'client_secret': bot.client_secret
    }
    response = requests.post(url, headers=headers, data=payload, verify=False)

    if response.status_code == 200:
        access_token = response.json()['access_token']
        print("access token is: " + access_token)
        return access_token
    else:
        raise Exception("Could not retrieve access token.")

def get_headers(bot):
    return {
        'Authorization': f'Bearer {get_access_token(bot)}',
        'Content-Type': 'application/json'
    }
