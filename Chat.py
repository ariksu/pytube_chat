import requests
from pprint import pprint, pformat
from oauth_pile import oauth_wrapper
import pendulum, time, json


class Chat:

    def __init__(self):
        self.name = 'youtube_stream'
        self.generate_auth()
        self.init_stream()
        self.chat = {}

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
        self.offset = 0
        stream_url = f"https://www.youtube.com/watch?v={self.id}"
        chat_send([("SYS", stream_url)])

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

    # TODO refactor
    def chat_update(self, raw_chat):
        cleaned_chat = [{'name': entry['authorDetails']['displayName'],
                         'text': entry['snippet']['displayMessage'],
                         'timestamp': pendulum.parse(entry['snippet']['publishedAt'])}
                        for entry in raw_chat]
        for entry in cleaned_chat:
            if entry['timestamp'] not in self.chat:
                self.chat[entry['timestamp']] = {'sent': False,
                                                 'entry': (entry['name'], entry['text'])}
        unsent = [val['entry'] for val in self.chat.values() if not val['sent']]
        if len(unsent) > 5:
            self.chat = {k: {"sent": True, 'entry': v['entry']} for k, v in self.chat.items()}
            return None
        chat_send(unsent)
        self.chat = {k: {"sent": True, 'entry': v['entry']} for k, v in self.chat.items()}
        pass

    def update_offset(self, timestamp, chat):
        pass


def chat_send(cleaned_chat):
    bot_token = '571655900:AAEeOOOw5Uhr7MEmyUr1t0O1tmf_uZpYbI8'
    url = 'https://api.telegram.org/bot' + bot_token + '/sendMessage'
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

    with open('chat.json', 'w') as chat_file:
        json.dump(chat, chat_file, indent=2)
    cleaned_chat = [{'name': message['authorDetails']['displayName'],
                     'text': message['snippet']['displayMessage'], }
                    for message in chat]
    pprint(cleaned_chat)
    while True:
        chat = yt_chat.list_all()
        yt_chat.chat_update(chat)
        time.sleep(2)
