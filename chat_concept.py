from oauth2client.tools import argparser
from oauth2client.file import Storage
import requests
from broadcast import get_authenticated_service, list_broadcasts
import sys
from pprint import pprint

VALID_BROADCAST_STATUSES = ("all", "active", "completed", "upcoming",)
CHAT_API_URL = "https://www.googleapis.com/youtube/v3/liveChat/messages"

argparser.add_argument("--broadcast-status", help="Broadcast status",
                       choices=VALID_BROADCAST_STATUSES, default=VALID_BROADCAST_STATUSES[0])
args = argparser.parse_args()
youtube = get_authenticated_service(args)

active_streams = list_broadcasts(youtube, 'active')

print(active_streams)
stream_id = active_streams[0]['id']
chat_id = active_streams[0]['snippet']['liveChatId']
assert (type(stream_id) is str), f"Fail to get stream id, found {stream_id}"
assert (type(chat_id) is str), f"Fail to get stream id, found {chat_id}"

storage = Storage("%s-oauth2.json" % sys.argv[0])
credentials = storage.get()


params = {
    'liveChatId': chat_id,
    'part':'authorDetails,snippet',
}

print(credentials.access_token)
headers = {
    'Authorization':f"Bearer {credentials.access_token}",


}

chat_response = requests.get('https://www.googleapis.com/youtube/v3/liveChat/messages', params=params, headers=headers)
chat=chat_response.json()['items']
cleaned_chat = [{'name':message['authorDetails']['displayName'],
                'text':message['snippet']['displayMessage'],}
                for message in chat]


pprint(cleaned_chat)
