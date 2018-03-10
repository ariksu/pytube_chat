import os

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

VALID_BROADCAST_STATUSES = ("all", "active", "completed", "upcoming",)
CHAT_API_URL = "https://www.googleapis.com/youtube/v3/liveChat/messages"
args = argparser.parse_args()
# noinspection SpellCheckingInspection
CLIENT_SECRETS_FILE = "client_secret_442772825695-ahbo6d7aefbtlu81vr1kkdk011njth0v.apps.googleusercontent.com.json"
YOUTUBE_READONLY_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the {{ Cloud Console }}
{{ https://cloud.google.com/console }}

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))


def get_authenticated_service(sysargs, storage_name):
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
                                   scope=YOUTUBE_READONLY_SCOPE,
                                   message=MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage(storage_name)
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, sysargs)

    return credentials


def oauth_wrapper(storage_name):
    argparser.add_argument("--broadcast-status", help="Broadcast status",
                           choices=VALID_BROADCAST_STATUSES, default=VALID_BROADCAST_STATUSES[0])
    args = argparser.parse_args()

    credentials = get_authenticated_service(args, storage_name)
    return credentials
