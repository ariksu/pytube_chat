import requests
from pprint import pprint, pformat
from oauth_pile import oauth_wrapper
import pendulum, time


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
        if yt_response.status_code != 200:
            error = f"""
            Youtube returns an error
            {pformat(yt_response.json())}
            """
            raise IOError(error)
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

    def get_updates(self, timestamp):
        chat = self.list_all()
        new_messages = [entry for entry in chat
                        if pendulum.parse(entry['snippet']['publishedAt']) >
                        timestamp]
        return pendulum.now(), new_messages

        pass


def chat_send(cleaned_chat):
    token = '571655900:AAEeOOOw5Uhr7MEmyUr1t0O1tmf_uZpYbI8'
    url = 'https://api.telegram.org/bot' + token + '/sendMessage'
    headers = {'Content-Type': 'application/json'}
    global_chat_id = '41535069'
    for name, message in cleaned_chat:
        fname = name.split(" ")[0]
        text = f"{fname}: {message}"
        print(text)
        message = {
            'chat_id': global_chat_id,
            'text': text,
        }
        requests.post(url, headers=headers, json=message)
    pass


if __name__ == '__main__':
    yt_chat = Chat()
    chat = yt_chat.list_all()
    import json

    with open('chat.json', 'w') as chat_file:
        json.dump(chat, chat_file, indent=2)
    cleaned_chat = [{'name': message['authorDetails']['displayName'],
                     'text': message['snippet']['displayMessage'], }
                    for message in chat]
    pprint(cleaned_chat)
    timestamp = pendulum.now()
    while True:
        timestamp, chat = yt_chat.get_updates(timestamp)
        if chat:
            cleaned_chat = [(message['authorDetails']['displayName'],
                             message['snippet']['displayMessage'])
                            for message in chat]
            chat_send(cleaned_chat)
        time.sleep(2)
