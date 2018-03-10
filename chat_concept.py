from oauth2client.tools import argparser
from oauth2client.file import Storage
import requests
import sys
from pprint import pprint
from oauth_pile import oauth_wrapper


def stream(token):
    params = {
        'broadcastStatus': 'active',
        'part': 'id,snippet',
    }
    headers = {
        'Authorization': f"Bearer {token}",

    }
    yt_response = requests.get('https://www.googleapis.com/youtube/v3/liveBroadcasts', params=params,
                               headers=headers)
    id = yt_response.json()['items'][0]['id']
    name = yt_response.json()['items'][0]['snippet']['title']
    chat_id = yt_response.json()['items'][0]['snippet']['liveChatId']
    return id, name, chat_id


def chat_items(id, token):
    params = {
        'liveChatId': chat_id,
        'part': 'authorDetails,snippet',
    }
    headers = {
        'Authorization': f"Bearer {token}",

    }
    chat_response = requests.get('https://www.googleapis.com/youtube/v3/liveChat/messages', params=params,
                                 headers=headers)
    return chat_response.json()['items']


# TODO refactor at least oauth call
storage_name = "%s-oauth2.json" % sys.argv[0]
credentials = oauth_wrapper(storage_name)
auth = credentials.access_token

stream, name, chat_id = stream(auth)
chat = chat_items(chat_id, auth)
cleaned_chat = [{'name': message['authorDetails']['displayName'],
                 'text': message['snippet']['displayMessage'], }
                for message in chat]

pprint(cleaned_chat)
