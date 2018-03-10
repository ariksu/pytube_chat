import requests
from pprint import pprint
from oauth_pile import oauth_wrapper


class Chat:

    def __init__(self):
        self.name = 'youtube_stream'
        self.generate_auth()
        self.init_stream()

    def generate_auth(self):
        storage_name = "%s-oauth2.json" % self.name
        self.credentials = oauth_wrapper(storage_name)
        self.auth = self.credentials.access_token
        pass

    def init_stream(self):
        params = {
            'broadcastStatus': 'active',
            'part': 'id,snippet',
        }
        headers = {
            'Authorization': f"Bearer {self.auth}",

        }
        yt_response = requests.get('https://www.googleapis.com/youtube/v3/liveBroadcasts', params=params,
                                   headers=headers)
        self.id = yt_response.json()['items'][0]['id']
        self.name = yt_response.json()['items'][0]['snippet']['title']
        self.chat_id = yt_response.json()['items'][0]['snippet']['liveChatId']

    def list_all(self):
        params = {
            'liveChatId': self.chat_id,
            'part': 'authorDetails,snippet',
        }
        headers = {
            'Authorization': f"Bearer {self.auth}",

        }
        chat_response = requests.get('https://www.googleapis.com/youtube/v3/liveChat/messages', params=params,
                                     headers=headers)
        return chat_response.json()['items']


if __name__ == '__main__':
    yt_chat = Chat()
    chat = yt_chat.list_all()
    cleaned_chat = [{'name': message['authorDetails']['displayName'],
                     'text': message['snippet']['displayMessage'], }
                    for message in chat]

    pprint(cleaned_chat)
