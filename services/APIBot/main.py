import flask
from flask import request
import json
from settings import *
from helpers import *
import html
import requests
import datetime
from urllib3.exceptions import InsecureRequestWarning

app = flask.Flask(__name__)
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

@app.route('/testbot', methods=['POST', 'GET'])
def chatbot():
    if request.method == 'GET':
        serverUrl = request.host
        print('serverUrl: ' + serverUrl)
        return 'OK'
    else:
        botToUse = None
        serverUrl = request.host
        if(serverUrl == "localhost:5001"):
            serverUrl = "local.mluvii.com"
        print('serverUrl: ' + serverUrl)
        if(request.args.get('botName') == "Bot1"):
            botToUse = bots[0]
        if (request.args.get('botName') == "Bot2"):
            botToUse = bots[1]
        if botToUse is None:
            chatbot_id = request.args.get('id')
            client_id = request.args.get('client_id')
            client_secret = request.args.get('client_secret')
            if chatbot_id is None or client_id is None or client_secret is None:
                return "Wrong chatbot or bad parameters", 400
            botToUse = bot(chatbot_id, client_id, client_secret)

        try:
            data = json.loads(request.data)
        except ValueError as e:
            activity_data = message_payload('Bad Request')
            send_request(activity_data, botToUse, serverUrl)

        print(data)

        if 'Activity' in data and 'Ping' in data['Activity']:
            return 'OK'

        if 'activity' in data and 'sessionId' in data:
            activity = data['activity']
            print("Activity is: " + activity)
            print("Datetime is: " + datetime.datetime.now().isoformat())
            if 'text' in data:
               if data['text'] == 'GetAvailableOperators':
                   req = message_get_available_operators(data.get('sessionId'))
                   send_request(req, botToUse, serverUrl)
                   return 'OK'

               if data['text'] == 'GetAvailableGroups':
                   req = message_get_available_groups(data.get('sessionId'))
                   send_request(req, botToUse, serverUrl)
                   return 'OK'

               if data['text'] == 'GetHeroCards':
                   req = message_get_hero_cards(data.get('sessionId'))
                   send_request(req, botToUse, serverUrl)
                   return 'OK'
               if data['text'] == 'GetCallParams':
                   req = message_get_call_params(data.get('sessionId'))
                   send_request(req, botToUse, serverUrl)
                   return 'OK'
               if 'SendHeroCard' in data['text']:
                   hcId = data['text'].split(' ', 1)[1]
                   req = message_send_hero_card(data.get('sessionId'), hcId)
                   send_request(req, botToUse, serverUrl)
                   return 'OK'
               if data['text'] == 'HandOff':
                   req = message_hand_off(data.get('sessionId'))
                   send_request(req, botToUse, serverUrl)
                   return 'OK'
               if data['text'] == 'EndConversation':
                   req = message_end_conversation(data.get('sessionId'))
                   send_request(req, botToUse, serverUrl)
                   return 'OK'
               if data['text'] == 'Typing':
                   req = message_typing(data.get('sessionId'), True)
                   send_request(req, botToUse, serverUrl)
                   return 'OK'
               if data['text'] == 'NotTyping':
                   req = message_typing(data.get('sessionId'), False)
                   send_request(req, botToUse, serverUrl)
                   return 'OK'
               if data['text'] == 'DisableGuestInput':
                   req = message_disable_guest_input(data.get('sessionId'))
                   send_request(req, botToUse, serverUrl)
                   return 'OK'
               if data['text'] == 'EnableGuestInput':
                   req = message_enable_guest_input(data.get('sessionId'))
                   send_request(req, botToUse, serverUrl)
                   return 'OK'
               if data['text'] == 'DisableGuestInput':
                   req = message_disable_guest_input(data.get('sessionId'))
                   send_request(req, botToUse, serverUrl)
                   return 'OK'
               if data['text'] == 'EnableGuestUpload':
                   req = message_enable_guest_upload(data.get('sessionId'))
                   send_request(req, botToUse, serverUrl)
                   return 'OK'
               if data['text'] == 'DisableGuestUpload':
                   req = message_disable_guest_upload(data.get('sessionId'))
                   send_request(req, botToUse, serverUrl)
                   return 'OK'
               if data['text'] == 'Carousel':
                   req = message_carousel(data.get('sessionId'))
                   send_request(req, botToUse, serverUrl)
                   return 'OK'
               if data['text'] == 'Buttons':
                   req = message_buttons(data.get('sessionId'))
                   send_request(req, botToUse, serverUrl)
                   return 'OK'
               if data['text'] == 'Hello':
                   req = message_hello(data.get('sessionId'))
                   send_request(req, botToUse, serverUrl)
                   return 'OK'
               if data['text'] == 'ChatbotOpenFileUploadPrompt':
                   req = message_chatbot_open_file_upload_prompt(data.get('sessionId'))
                   send_request(req, botToUse, serverUrl)
                   return 'OK'
               if data['text'] == 'SendImage':
                   req = send_image(data.get('sessionId'))
                   send_request(req, botToUse, serverUrl)
                   return 'OK'
               if data['text'] == 'SendYoutubeLink':
                   req = send_youtube_video(data.get('sessionId'))
                   send_request(req, botToUse, serverUrl)
                   return 'OK'
               if data['text'] == 'SendMp4Link':
                   req = send_mp4_video(data.get('sessionId'))
                   send_request(req, botToUse, serverUrl)
                   return 'OK'
               if data['text'] == 'GetMediaObjects':
                   req = get_media_objects(data.get('sessionId'))
                   send_request(req, botToUse, serverUrl)
                   return 'OK'

            payload = message_payload(json.dumps(data), data.get('sessionId'))
            send_request(payload, botToUse,serverUrl)
            return 'OK'

        raise NameError('Bad Request')


def message_payload(message, session_id):
    return {
        "activity": "Text",
        "timestamp": datetime_now_iso(),
        "text": message,
        "sessionId": session_id,
        "language": "cs",
        "source": "Default"
    }

def message_get_available_operators(session_id):
    return {
        "activity": "GetAvailableOperators",
        "sessionId": session_id
    }

def message_get_available_groups(session_id):
    return {
        "activity": "GetAvailableGroups",
        "sessionId": session_id
    }

def message_get_call_params(session_id):
    return {
        "activity": "GetCallParams",
        "sessionId": session_id
    }

def message_set_call_params(session_id, callParams):
    return {
        "activity": "SetCallParams",
        "sessionId": session_id,
        "callParams": callParams
    }

def message_get_guest_identity(session_id):
    return {
        "activity": "GetGuestIdentity",
        "sessionId": session_id
    }

def message_hand_off(session_id):
    return {
        "activity": "HandOff",
        "sessionId": session_id
    }

def message_end_conversation(session_id):
    return {
        "activity": "EndConversation",
        "sessionId": session_id
    }

def message_typing(session_id, show):
    return {
        "activity": "Typing",
        "sessionId": session_id,
        "show": show
    }

def message_disable_guest_input(session_id):
    return {
        "activity": "DisableGuestInput",
        "sessionId": session_id
    }

def message_enable_guest_input(session_id):
    return {
        "activity": "EnableGuestInput",
        "sessionId": session_id
    }

def message_get_hero_cards(session_id):
    return {
        "activity": "GetHeroCards",
        "sessionId": session_id,
    }

def message_send_hero_card(session_id, heroCardId):
    return {
        "activity": "SendHeroCard",
        "sessionId": session_id,
        "heroCardId": heroCardId
    }

def message_chatbot_open_file_upload_prompt(session_id):
    return {
        "activity": "ChatbotOpenFileUploadPrompt",
        "sessionId": session_id
    }

def message_enable_guest_upload(session_id):
    return {
        "activity": "EnableGuestUpload",
        "sessionId": session_id
    }

def message_disable_guest_upload(session_id):
    return {
        "activity": "DisableGuestUpload",
        "sessionId": session_id
    }

def message_carousel(session_id):
    return {
  "sessionId": session_id,
  "type": "message",
  "timestamp": datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat(),
  "attachmentLayout": "carousel",
  "attachments": [
    {
      "contentType": "application/vnd.microsoft.card.hero",
      "content": {
        "title": "Street #1",
        "subtitle": "1. Street Foo 254 Czechia",
        "images": [
          {
            "url": "https://dev.virtualearth.net/REST/V1/Imagery/Map/Road?form=BTCTRL&mapArea=49.7463607788086,13.1083498001099,49.7932815551758,13.1951398849487&mapSize=500,280&pp=49.7616882324219,13.1491804122925;1;1&dpi=1&logo=always&key=ApBn8xoItlENbFx-rr1kzt_JakWdFTH24taCasYxQCgit15NtDeYrztO4chDtrg5"
          }
        ],
        "buttons": [
          {
            "type": "imBack",
            "title": "Street Foo 254",
            "value": 1
          }
        ]
      }
    },
    {
      "contentType": "application/vnd.microsoft.card.hero",
      "content": {
        "title": "Street #2",
        "subtitle": "1. Ulice, Plzeň, Czechia",
        "images": [
          {
            "url": "https://dev.virtualearth.net/REST/V1/Imagery/Map/Road?form=BTCTRL&mapArea=49.7463607788086,13.1083498001099,49.7932815551758,13.1951398849487&mapSize=500,280&pp=49.7616882324219,13.1491804122925;1;1&dpi=1&logo=always&key=ApBn8xoItlENbFx-rr1kzt_JakWdFTH24taCasYxQCgit15NtDeYrztO4chDtrg5"
          }
        ],
        "buttons": [
          {
            "type": "imBack",
            "title": "Ulice, Plzeň, Czechia",
            "value": 1
          }
        ]
      }
    },
    {
      "contentType": "application/vnd.microsoft.card.hero",
      "content": {
        "title": "Street #2 again",
        "subtitle": "1. Ulice, Plzeň, Czechia",
        "images": [
          {
            "url": "https://dev.virtualearth.net/REST/V1/Imagery/Map/Road?form=BTCTRL&mapArea=49.7463607788086,13.1083498001099,49.7932815551758,13.1951398849487&mapSize=500,280&pp=49.7616882324219,13.1491804122925;1;1&dpi=1&logo=always&key=ApBn8xoItlENbFx-rr1kzt_JakWdFTH24taCasYxQCgit15NtDeYrztO4chDtrg5"
          }
        ],
        "buttons": [
          {
            "type": "imBack",
            "title": "Ulice, Plzeň, Czechia",
            "value": 1
          }
        ]
      }
    }
  ]
}

def message_buttons(session_id):
    return {
  "type": "message",
  "sessionId": session_id,
  "timestamp": datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat(),
  "attachments": [
    {
      "contentType": "application/vnd.microsoft.card.hero",
      "content": {
        "title": "Test buttons",
        "buttons": [
          {
            "type": "imBack",
            "title": "Title of the first button",
            "value": "Value of the first button"
          },
          {
            "type": "imBack",
            "title": "Title of the second button",
            "value": "Value of the second button"
          }
        ]
      }
    }
  ]
}

def message_hello(session_id):
    return {
        "sessionId": session_id,
        "activity": "Text",
        "text": "Hello world"
    }

def send_image(session_id):
    return {
        "sessionId": session_id,
        "activity": "Text",
        "text": "https://upload.wikimedia.org/wikipedia/commons/9/9a/Gull_portrait_ca_usa.jpg"
    }

def send_youtube_video(session_id):
    return {
        "sessionId": session_id,
        "activity": "Text",
        "text": "https://www.youtube.com/watch?v=DQFKmzUhQg8&ab_channel=mluvii"
    }

def send_mp4_video(session_id):
    return {
        "sessionId": session_id,
        "activity": "Text",
        "text": "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
    }

def get_media_objects(session_id):
    return {
        "sessionId": session_id,
        "activity": "GetMediaObjects",
    }

def send_request(payload, bot, serverUrl):
    print("bot id: " + str(bot.chatbot_id))
    response = requests.post(f'https://{serverUrl}/api/v1/Chatbot/{str(bot.chatbot_id)}/activity', headers=get_headers(bot,serverUrl), data=json.dumps(payload), verify=False)
    if response.status_code != 200 and response.status_code != 201:
        raise NameError('Response not successful')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
