import os
# import sys
# import httplib2
# import uritemplate
# from googleapiclient.errors import HttpError, UnknownApiNameOrVersion
# from googleapiclient.http import HttpRequest, build_http
# from oauth2client._helpers import positional
# from six.moves import http_client

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

# from discovery import DISCOVERY_URI, V2_DISCOVERY_URI, _retrieve_discovery_doc, build_from_document

VALID_BROADCAST_STATUSES = ("all", "active", "completed", "upcoming",)
CHAT_API_URL = "https://www.googleapis.com/youtube/v3/liveChat/messages"
args = argparser.parse_args()
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


def get_authenticated_service(args, storage_name):
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
                                   scope=YOUTUBE_READONLY_SCOPE,
                                   message=MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage(storage_name)
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, args)

    return credentials

# # This OAuth 2.0 access scope allows for read-only access to the authenticated
# # user's account, but not other types of account access.
#
# # This variable defines a message to display if the CLIENT_SECRETS_FILE is
# # missing.
#
# @positional(2)
# def build(serviceName,
#           version,
#           http=None,
#           discoveryServiceUrl=DISCOVERY_URI,
#           developerKey=None,
#           model=None,
#           requestBuilder=HttpRequest,
#           credentials=None,
#           cache_discovery=True,
#           cache=None):
#   """Construct a Resource for interacting with an API.
#
#   Construct a Resource object for interacting with an API. The serviceName and
#   version are the names from the Discovery service.
#
#   Args:
#     serviceName: string, name of the service.
#     version: string, the version of the service.
#     http: httplib2.Http, An instance of httplib2.Http or something that acts
#       like it that HTTP requests will be made through.
#     discoveryServiceUrl: string, a URI Template that points to the location of
#       the discovery service. It should have two parameters {api} and
#       {apiVersion} that when filled in produce an absolute URI to the discovery
#       document for that service.
#     developerKey: string, key obtained from
#       https://code.google.com/apis/console.
#     model: googleapiclient.Model, converts to and from the wire format.
#     requestBuilder: googleapiclient.http.HttpRequest, encapsulator for an HTTP
#       request.
#     credentials: oauth2client.Credentials or
#       google.auth.credentials.Credentials, credentials to be used for
#       authentication.
#     cache_discovery: Boolean, whether or not to cache the discovery doc.
#     cache: googleapiclient.discovery_cache.base.CacheBase, an optional
#       cache object for the discovery documents.
#
#   Returns:
#     A Resource object with methods for interacting with the service.
#   """
#   params = {
#       'api': serviceName,
#       'apiVersion': version
#       }
#
#   if http is None:
#     discovery_http = build_http()
#   else:
#     discovery_http = http
#
#   for discovery_url in (discoveryServiceUrl, V2_DISCOVERY_URI,):
#     requested_url = uritemplate.expand(discovery_url, params)
#
#     try:
#       content = _retrieve_discovery_doc(
#         requested_url, discovery_http, cache_discovery, cache)
#       return build_from_document(content, base=discovery_url, http=http,
#           developerKey=developerKey, model=model, requestBuilder=requestBuilder,
#           credentials=credentials)
#     except HttpError as e:
#       if e.resp.status == http_client.NOT_FOUND:
#         continue
#       else:
#         raise e
#
#   raise UnknownApiNameOrVersion(
#         "name: %s  version: %s" % (serviceName, version))


def oauth_wrapper(storage_name):
    argparser.add_argument("--broadcast-status", help="Broadcast status",
                           choices=VALID_BROADCAST_STATUSES, default=VALID_BROADCAST_STATUSES[0])
    args = argparser.parse_args()

    credentials = get_authenticated_service(args, storage_name)
    return credentials